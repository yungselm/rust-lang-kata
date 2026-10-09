"""Where card files live — shared by build.py, check_cards.py and lint_cards.py.

  cards/*.yaml                         core deck   -> output/CodeCards.apkg
  additional_cards/checked/*.yaml      std-only    -> compile/lint/test-checked
  additional_cards/unchecked/*.yaml    ext. crates / fragments -> never compiled
                                       (both)      -> output/AdditionalCards.apkg

Additional files starting with `_` are examples: checked and linted like any
other file, but left out of AdditionalCards.apkg unless passed explicitly.
"""
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(HERE, "cards")
ADDITIONAL_DIR = os.path.join(HERE, "additional_cards")
CHECKED_DIR = os.path.join(ADDITIONAL_DIR, "checked")
UNCHECKED_DIR = os.path.join(ADDITIONAL_DIR, "unchecked")


def _yaml(d):
    return sorted(glob.glob(os.path.join(d, "*.yaml")))


def is_example(path):
    return os.path.basename(path).startswith("_")


def core_files():
    return _yaml(CORE_DIR)


def checked_files():
    return _yaml(CHECKED_DIR)


def unchecked_files():
    return _yaml(UNCHECKED_DIR)


def deck_files():
    """Additional files that go into AdditionalCards.apkg (examples excluded)."""
    return [p for p in checked_files() + unchecked_files() if not is_example(p)]


def _inside(path, d):
    return os.path.commonpath([os.path.abspath(path), d]) == d


def is_core(path):
    return _inside(path, CORE_DIR)


def is_unchecked(path):
    return _inside(path, UNCHECKED_DIR)


def resolve(args):
    """CLI paths are relative to the repo root (as they always were)."""
    return [os.path.join(HERE, a) for a in args]
