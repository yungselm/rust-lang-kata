"""Build CodeCards.apkg (cards/) and AdditionalCards.apkg (additional_cards/).

Deck layout (root name set by DECK_ROOT below):
  - cards/<topic>.yaml            -> <DECK_ROOT>::Core::<Topic>      (concept/idiom decks)
  - cards/neetcode__<cat>.yaml    -> <DECK_ROOT>::Neetcode::<Cat>    (interview problems)
  - additional_cards/{checked,unchecked}/<topic>.yaml
                                  -> <DECK_ROOT>::Additional::<Topic> (personal topics,
                                     separate .apkg; same stem in both folders = one deck;
                                     `_`-prefixed example files are skipped, see card_paths.py)

Each card is a YAML list item:
  - type: code            # default
    instruction / starter / solution / notes / source / tags / tests
  - type: concept
    question / answer / code / source / tags

Text fields are HTML-escaped (so Vec<T> renders), `backticks` -> <code>, and
**double-asterisks** -> <strong> (bold, for a concept card's lead sentence).
After genanki writes the package, `postprocess()` injects two deck-options
presets and stamps the NeetCode new-card order (see SETTINGS below).

Usage:
    python build.py                  # all cards/*.yaml + additional_cards/*/*.yaml
    python build.py cards/x.yaml     # just one file (any path outside cards/ is
                                     # built into AdditionalCards.apkg)
"""
import base64
import html
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import zipfile
import zlib

import yaml
import genanki

import card_paths

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")
OUT = os.path.join(HERE, "output")
ASSETS = os.path.join(OUT, "_assets")

CODE_MODEL_ID = 1607392319
CONCEPT_MODEL_ID = 1607392321
ASSET_VER = "8"   # bump on any vendor/_cards.js change
DECK_ROOT = "Rust Language Kata"   # top-level deck name shown in Anki

# ---- shipped deck-options settings -------------------------------------------
# These apply under BOTH schedulers. The SM-2 fields (initial factor, easy bonus,
# interval modifier, hard factor, new interval) are simply ignored when FSRS is
# on; the daily limits, steps, leech threshold, and new-card order always apply.
CORE_CONF_ID = 1001
NEETCODE_CONF_ID = 1002
CORE_NEW_PER_DAY = 14
NEETCODE_NEW_PER_DAY = 1
MAX_REVIEWS = 9999
LEARNING_STEPS = [1.0, 10.0]   # minutes
GRADUATING_IVL = 1
EASY_IVL = 4
STARTING_EASE = 2500           # 2.50
EASY_BONUS = 1.3
INTERVAL_MODIFIER = 1.0
HARD_FACTOR = 1.2
NEW_INTERVAL = 0.1             # % of interval kept after a lapse
RELEARN_STEPS = [10.0]         # minutes
LEECH_FAILS = 5
LEECH_ACTION = 1               # 0 = suspend, 1 = tag only
MAX_INTERVAL = 36500
NEW_ORDER_SEQUENTIAL = 1       # 1 = order added (NeetCode easy->hard), 0 = random
NEW_ORDER_RANDOM = 0

# Canonical NeetCode topic order (deck names as produced by deck_for).
NEETCODE_ORDER = [f"{DECK_ROOT}::Neetcode::{t}" for t in [
    "Arrays Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Tries",
    "Heap",
    "Backtracking",
    "Graphs",
    "Advanced Graphs",
    "Dp 1D",
    "Dp 2D",
    "Greedy",
    "Intervals",
    "Math Geometry",
    "Bit Manipulation",
]]

# Anki positions new cards by IMPORT order, so we add the NeetCode files in
# canonical topic order (easy->hard) here; core files come first, alphabetical.
NEETCODE_FILE_ORDER = [
    "neetcode__arrays_hashing", "neetcode__two_pointers", "neetcode__sliding_window",
    "neetcode__stack", "neetcode__binary_search", "neetcode__linked_list",
    "neetcode__trees", "neetcode__tries", "neetcode__heap", "neetcode__backtracking",
    "neetcode__graphs", "neetcode__advanced_graphs", "neetcode__dp_1d",
    "neetcode__dp_2d", "neetcode__greedy", "neetcode__intervals",
    "neetcode__math_geometry", "neetcode__bit_manipulation",
]


def _path_order(p):
    stem = os.path.splitext(os.path.basename(p))[0]
    if stem in NEETCODE_FILE_ORDER:
        return (1, NEETCODE_FILE_ORDER.index(stem), "")
    return (0, 0, stem)   # core files first, alphabetical

SOURCES = {
    "_codemirror.js": "vendor/_codemirror.js",
    "_codemirror.css": "vendor/_codemirror.css",
    "_simple.js": "vendor/_simple.js",
    "_rust.js": "vendor/_rust.js",
    "_closebrackets.js": "vendor/_closebrackets.js",
    "_matchbrackets.js": "vendor/_matchbrackets.js",
    "_cards.js": "templates/_cards.js",
}


def versioned(name):
    return "_cc" + ASSET_VER + name


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def b64(s):
    return base64.b64encode((s or "").encode("utf-8")).decode("ascii")


def text(s):
    """HTML-escape, then turn `code` into <code>code</code> and **bold** into
    <strong>bold</strong> (used for a concept card's one-sentence lead answer,
    so it's easy to self-check before reading the rest of the explanation)."""
    s = html.escape(s or "", quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)


def stage_assets():
    if os.path.isdir(ASSETS):
        shutil.rmtree(ASSETS)
    os.makedirs(ASSETS)
    paths = []
    for name, rel in SOURCES.items():
        dst = os.path.join(ASSETS, versioned(name))
        shutil.copyfile(os.path.join(HERE, rel), dst)
        paths.append(dst)
    return paths


def versionize(tpl):
    for name in SOURCES:
        tpl = tpl.replace(name, versioned(name))
    return tpl


def build_models():
    code = genanki.Model(
        CODE_MODEL_ID, "Code Editor Card",
        fields=[{"name": n} for n in
                ("Instruction", "StarterCode", "Solution", "Lang", "Notes", "Source",
                 "Walkthrough")],
        templates=[{
            "name": "Code Card",
            "qfmt": versionize(read(os.path.join(TPL, "front.html"))),
            "afmt": versionize(read(os.path.join(TPL, "back.html"))),
        }],
        css=read(os.path.join(TPL, "style.css")),
        sort_field_index=0,
    )
    concept = genanki.Model(
        CONCEPT_MODEL_ID, "Rust Concept Card",
        fields=[{"name": n} for n in ("Question", "Answer", "Code", "Lang", "Source")],
        templates=[{
            "name": "Concept Card",
            "qfmt": versionize(read(os.path.join(TPL, "front_concept.html"))),
            "afmt": versionize(read(os.path.join(TPL, "back_concept.html"))),
        }],
        css=read(os.path.join(TPL, "style.css")),
        sort_field_index=0,
    )
    return code, concept


def titled(seg):
    return seg.replace("_", " ").replace("-", " ").title()


def deck_key(stem, additional):
    # Namespaces deck ids and note guids, so an additional `strings.yaml` can't
    # collide with the core one. Core keys stay the bare stem (stable guids).
    return f"additional__{stem}" if additional else stem


def deck_for(stem, additional=False):
    # NeetCode subdecks get a 2-digit topic-order prefix so alphabetical order
    # == NeetCode order under any gather setting. Core -> <DECK_ROOT>::Core::<Topic>.
    if additional:
        name = f"{DECK_ROOT}::Additional::" + "::".join(
            titled(s) for s in stem.lstrip("_").split("__"))
    elif stem in NEETCODE_FILE_ORDER:
        idx = NEETCODE_FILE_ORDER.index(stem) + 1
        name = f"{DECK_ROOT}::Neetcode::{idx:02d} {titled(stem.split('__', 1)[1])}"
    elif "__" in stem:
        name = DECK_ROOT + "::" + "::".join(titled(s) for s in stem.split("__"))
    else:
        name = f"{DECK_ROOT}::Core::" + titled(stem)
    deck_id = 1700000000 + (zlib.crc32(deck_key(stem, additional).encode()) % 100000000)
    return genanki.Deck(deck_id, name)


# Parent decks genanki doesn't create itself. Fixed ids for the known ones,
# name-derived for nested parents (e.g. Additional::Iced from iced__widgets.yaml).
PARENT_IDS = {DECK_ROOT: 1690000001, f"{DECK_ROOT}::Core": 1690000002,
              f"{DECK_ROOT}::Neetcode": 1690000003, f"{DECK_ROOT}::Additional": 1690000004}


def parent_id(name):
    return PARENT_IDS.get(name, 1600000000 + zlib.crc32(name.encode()) % 90000000)


# ---- deck-options preset (legacy dconf format genanki writes) ----------------
def make_conf(cid, name, new_per_day, new_order):
    return {
        "id": cid, "mod": 0, "name": name, "usn": -1, "maxTaken": 60,
        "autoplay": True, "timer": 0, "replayq": True, "dyn": False,
        "new": {
            "bury": False, "delays": LEARNING_STEPS, "initialFactor": STARTING_EASE,
            "ints": [GRADUATING_IVL, EASY_IVL, 7], "order": new_order,
            "perDay": new_per_day, "separate": True,
        },
        "rev": {
            "bury": False, "ease4": EASY_BONUS, "fuzz": 0.05, "ivlFct": INTERVAL_MODIFIER,
            "maxIvl": MAX_INTERVAL, "perDay": MAX_REVIEWS, "hardFactor": HARD_FACTOR,
            "minSpace": 1,
        },
        "lapse": {
            "delays": RELEARN_STEPS, "leechAction": LEECH_ACTION, "leechFails": LEECH_FAILS,
            "minInt": 1, "mult": NEW_INTERVAL,
        },
    }


def _deck_obj(deck_id, name, conf_id):
    return {
        "id": deck_id, "mod": 0, "name": name, "usn": -1,
        "lrnToday": [0, 0], "revToday": [0, 0], "newToday": [0, 0], "timeToday": [0, 0],
        "collapsed": False, "browserCollapsed": False, "desc": "", "dyn": 0,
        "conf": conf_id, "extendNew": 0, "extendRev": 0,
    }


def postprocess(apkg_path):
    """Inject the two presets, ensure parent decks exist, stamp NeetCode order."""
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(apkg_path) as z:
        names = z.namelist()
        z.extractall(tmp)
    db_name = next(n for n in names if n.startswith("collection.anki2"))
    con = sqlite3.connect(os.path.join(tmp, db_name))
    cur = con.cursor()

    decks = json.loads(cur.execute("select decks from col").fetchone()[0])
    dconf = json.loads(cur.execute("select dconf from col").fetchone()[0])

    dconf[str(CORE_CONF_ID)] = make_conf(CORE_CONF_ID, f"{DECK_ROOT} Core",
                                         CORE_NEW_PER_DAY, NEW_ORDER_RANDOM)
    dconf[str(NEETCODE_CONF_ID)] = make_conf(NEETCODE_CONF_ID, f"{DECK_ROOT} NeetCode",
                                             NEETCODE_NEW_PER_DAY, NEW_ORDER_SEQUENTIAL)

    # ensure parent decks exist (Anki would otherwise auto-create them with the
    # default preset, ignoring our daily limits); presets are assigned below.
    existing = {d["name"] for d in decks.values()}
    parents = sorted({"::".join(parts[:i])
                      for parts in (n.split("::") for n in existing)
                      for i in range(1, len(parts))} - existing)
    for pname in parents:
        pid = parent_id(pname)
        decks[str(pid)] = _deck_obj(pid, pname, CORE_CONF_ID)

    # assign every deck to a preset by name
    for did, d in decks.items():
        name = d.get("name", "")
        if did == "1" or name == "Default":
            continue
        if name == f"{DECK_ROOT}::Neetcode" or name.startswith(f"{DECK_ROOT}::Neetcode::"):
            d["conf"] = NEETCODE_CONF_ID
        else:
            d["conf"] = CORE_CONF_ID

    cur.execute("update col set decks = ?, dconf = ?",
                (json.dumps(decks), json.dumps(dconf)))

    # stamp NeetCode new-card order: topic order, then card order within a file
    name_by_id = {int(did): d.get("name", "") for did, d in decks.items()}
    order_index = {nm: i for i, nm in enumerate(NEETCODE_ORDER)}
    rows = cur.execute("select id, nid, did from cards").fetchall()
    nc = []
    for cid, nid, did in rows:
        nm = name_by_id.get(did, "")
        if nm.startswith(f"{DECK_ROOT}::Neetcode::"):
            nc.append((order_index.get(nm, 999), nid, cid))
    nc.sort()
    for pos, (_idx, _nid, cid) in enumerate(nc, start=1):
        cur.execute("update cards set due = ?, type = 0, queue = 0 where id = ?",
                    (pos, cid))

    con.commit()
    con.close()

    with zipfile.ZipFile(apkg_path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.write(os.path.join(tmp, n), n)
    shutil.rmtree(tmp)


def build_package(paths, dest, code_model, concept_model, media, additional):
    """Write one .apkg from `paths`; files sharing a stem share a deck."""
    decks, total = {}, 0
    for p in paths:
        stem = os.path.splitext(os.path.basename(p))[0]
        key = deck_key(stem, additional)
        deck = decks.setdefault(stem, deck_for(stem, additional))
        for c in (yaml.safe_load(read(p)) or []):
            kind = c.get("type", "code")
            tags = [str(t) for t in c.get("tags", [])]
            if kind == "concept":
                note = genanki.Note(
                    model=concept_model,
                    fields=[text(c["question"]), text(c.get("answer", "")),
                            b64(c.get("code", "")), c.get("lang", "rust"),
                            text(c.get("source", ""))],
                    guid=genanki.guid_for(key, "concept", c["question"]),
                    tags=tags,
                )
            else:
                note = genanki.Note(
                    model=code_model,
                    fields=[text(c["instruction"].rstrip("\n")),
                            b64(c.get("starter", "")), b64(c.get("solution", "")),
                            c.get("lang", "rust"), text(c.get("notes", "")),
                            text(c.get("source", "")), b64(c.get("walkthrough", ""))],
                    guid=genanki.guid_for(key, "code", c["instruction"]),
                    tags=tags,
                )
            deck.add_note(note)
            total += 1

    pkg = genanki.Package(list(decks.values()))
    pkg.media_files = media
    pkg.write_to_file(dest)
    postprocess(dest)
    print(f"Wrote {dest}: {total} cards in {len(decks)} deck(s), assets {ASSET_VER}.")


def main():
    args = sys.argv[1:]
    if args:
        paths = card_paths.resolve(args)
        core = [p for p in paths if card_paths.is_core(p)]
        additional = [p for p in paths if not card_paths.is_core(p)]
    else:
        core, additional = card_paths.core_files(), card_paths.deck_files()
    if not core and not additional:
        print("No card files found in cards/ or additional_cards/.")
        return

    media = stage_assets()
    code_model, concept_model = build_models()
    os.makedirs(OUT, exist_ok=True)
    if core:
        core = sorted(core, key=_path_order)   # NeetCode in canonical topic order
        build_package(core, os.path.join(OUT, "CodeCards.apkg"),
                      code_model, concept_model, media, additional=False)
        print(f"  Presets: Core ({CORE_NEW_PER_DAY}/day, random), "
              f"NeetCode ({NEETCODE_NEW_PER_DAY}/day, in order).")
    if additional:
        build_package(sorted(additional, key=lambda p: os.path.basename(p)),
                      os.path.join(OUT, "AdditionalCards.apkg"),
                      code_model, concept_model, media, additional=True)
        print(f"  Preset: Core ({CORE_NEW_PER_DAY}/day, random).")


if __name__ == "__main__":
    main()
