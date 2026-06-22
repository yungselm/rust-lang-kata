"""Flag cards that aren't self-contained — i.e. that can't be solved from the
instruction alone, or that reference another card.

Two checks per code card:
  1. Cross-reference phrases in the instruction ("like the previous", ...).
  2. String literals the SOLUTION produces whose words don't appear in the
     instruction/notes — the strongest sign the prompt omits a required output
     (e.g. a solution returning "empty" while the prompt never says "empty").

Comments and panic/expect/unreachable messages are stripped before the literal
check (the learner isn't expected to reproduce those from the prompt). Known
implementation-detail literals can be allow-listed below.

Run from the repo root:  python lint_cards.py
Exits non-zero if anything is flagged, so it can gate a commit; review flags —
some may be acceptable and belong in ALLOW.
"""
import glob, os, re, sys, yaml

COMMENT = re.compile(r"//[^\n]*")
MACROMSG = re.compile(r'(?:\.expect|panic!|unreachable!|unimplemented!|todo!)\s*\(\s*"(?:[^"\\]|\\.)*"\s*\)')
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
XREF = re.compile(r"\b(like the previous|the previous card|as (above|before)|like it|same as the previous|see the (other|previous))\b", re.I)
STOP = set("a an the to of in on at is are be it as and or for with into from by "
           "n x y z c e i j k v t s w h r m".split())
# (basename, literal) pairs that are fine even though their words aren't in the prompt
ALLOW = {("iterators.yaml", "aeiou")}


def words(s):
    s = re.sub(r"\{[^}]*\}", " ", s)          # drop format placeholders
    return [w.lower() for w in re.findall(r"[A-Za-z]{2,}", s)]


def norm(s):
    return " " + re.sub(r"\s+", " ", s.lower()) + " "


def main():
    flags = 0
    for f in sorted(glob.glob(os.path.join("cards", "*.yaml"))):
        base = os.path.basename(f)
        for c in (yaml.safe_load(open(f, encoding="utf-8")) or []):
            if c.get("type", "code") == "concept":
                continue
            instr = c.get("instruction", "") or ""
            sol = c.get("solution", "") or ""
            ctx = norm(instr + " " + (c.get("notes", "") or ""))
            title = (instr.strip().splitlines() or ["?"])[0][:64]
            if XREF.search(instr):
                print(f"[xref]    {base}: {title}")
                flags += 1
            clean = MACROMSG.sub("", COMMENT.sub("", sol))
            for lit in sorted(set(STR.findall(clean))):
                if (base, lit) in ALLOW:
                    continue
                sig = [w for w in words(lit) if w not in STOP]
                if sig and any(w not in ctx for w in sig):
                    print(f"[literal] {base}: {title}  -> solution emits \"{lit}\" "
                          f"(missing from prompt: {[w for w in sig if w not in ctx]})")
                    flags += 1
    print(f"\n{'OK — every card is self-contained.' if not flags else f'{flags} flag(s) to review.'}")
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
