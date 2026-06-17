"""Defines the Anki note type (model) for code-editor cards."""
import os
import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")

# Stable IDs so re-importing UPDATES the same note type / deck
# instead of creating duplicates. Do not change these.
MODEL_ID = 1607392319
DECK_ID = 2059400110

# Media files that must ship inside the .apkg. The leading "_" tells Anki
# never to treat them as unused and delete them. Order matters: simple.js
# must load before rust.js (the Rust mode is built on defineSimpleMode).
MEDIA_NAMES = [
    "vendor/_codemirror.js",
    "vendor/_codemirror.css",
    "vendor/_simple.js",
    "vendor/_rust.js",
    "vendor/_closebrackets.js",
    "vendor/_matchbrackets.js",
    "templates/_cards.js",
]


def _read(name):
    with open(os.path.join(TPL, name), "r", encoding="utf-8") as f:
        return f.read()


def build_model():
    return genanki.Model(
        MODEL_ID,
        "Code Editor Card",
        fields=[
            {"name": "Instruction"},
            {"name": "StarterCode"},
            {"name": "Solution"},
            {"name": "Lang"},
            {"name": "Notes"},
        ],
        templates=[{
            "name": "Code Card",
            "qfmt": _read("front.html"),
            "afmt": _read("back.html"),
        }],
        css=_read("style.css"),
        sort_field_index=0,
    )


def media_files():
    return [os.path.join(HERE, *n.split("/")) for n in MEDIA_NAMES]
