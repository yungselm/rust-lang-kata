"""Build CodeCards.apkg from the YAML card files in cards/.

Each cards/<topic>.yaml becomes its own subdeck (Rust::<Topic>) and may mix:

  - type: code            # default; can be omitted
    instruction: ...
    starter: ...          # optional pre-filled scaffold
    solution: ...
    notes: ...            # optional, shown on back
    source: ...           # optional provenance, shown on back
    tags: [...]

  - type: concept
    question: ...
    answer: ...
    code: ...             # optional rust snippet, highlighted on back
    source: ...           # optional provenance
    tags: [...]

Text fields are HTML-escaped (so generics like Vec<T> render) and `backticks`
become inline <code>.

Usage:
    python build.py                  # all cards/*.yaml
    python build.py cards/match.yaml # just one file
"""
import base64
import glob
import html
import os
import re
import shutil
import sys
import zlib

import yaml
import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")
OUT = os.path.join(HERE, "output")
ASSETS = os.path.join(OUT, "_assets")

CODE_MODEL_ID = 1607392319
CONCEPT_MODEL_ID = 1607392321
ASSET_VER = "4"   # bump on any vendor/_cards.js change

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
    """HTML-escape, then turn `code` into <code>code</code>."""
    s = html.escape(s or "", quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


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
                ("Instruction", "StarterCode", "Solution", "Lang", "Notes", "Source")],
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


def deck_for(stem):
    title = stem.replace("_", " ").replace("-", " ").title().replace(" ", "")
    deck_id = 1700000000 + (zlib.crc32(stem.encode()) % 100000000)
    return genanki.Deck(deck_id, "Rust::" + title)


def main():
    args = sys.argv[1:]
    paths = ([os.path.join(HERE, a) for a in args] if args
             else sorted(glob.glob(os.path.join(HERE, "cards", "*.yaml"))))
    if not paths:
        print("No card files found in cards/.")
        return

    media = stage_assets()
    code_model, concept_model = build_models()
    decks, total = [], 0

    for p in paths:
        stem = os.path.splitext(os.path.basename(p))[0]
        deck = deck_for(stem)
        for c in (yaml.safe_load(read(p)) or []):
            kind = c.get("type", "code")
            tags = [str(t) for t in c.get("tags", [])]
            if kind == "concept":
                note = genanki.Note(
                    model=concept_model,
                    fields=[text(c["question"]), text(c.get("answer", "")),
                            b64(c.get("code", "")), c.get("lang", "rust"),
                            text(c.get("source", ""))],
                    guid=genanki.guid_for(stem, "concept", c["question"]),
                    tags=tags,
                )
            else:
                note = genanki.Note(
                    model=code_model,
                    fields=[text(c["instruction"].rstrip("\n")),
                            b64(c.get("starter", "")), b64(c.get("solution", "")),
                            c.get("lang", "rust"), text(c.get("notes", "")),
                            text(c.get("source", ""))],
                    guid=genanki.guid_for(stem, "code", c["instruction"]),
                    tags=tags,
                )
            deck.add_note(note)
            total += 1
        decks.append(deck)

    os.makedirs(OUT, exist_ok=True)
    pkg = genanki.Package(decks)
    pkg.media_files = media
    dest = os.path.join(OUT, "CodeCards.apkg")
    pkg.write_to_file(dest)
    print(f"Wrote {dest}: {total} cards in {len(decks)} deck(s), assets {ASSET_VER}.")


if __name__ == "__main__":
    main()
