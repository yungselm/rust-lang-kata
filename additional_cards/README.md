# Additional cards

Your own topics for a framework you're learning (`iced`, `axum`, `bevy`, …), patterns
from a project at work, all written in the same YAML format as `cards/`, built with
the same note types and editor, but shipped as a **separate**
`output/AdditionalCards.apkg` so the main deck stays general.

Put every file in exactly one of the two folders; the folder decides how it's
verified:

| Folder | Use for | `check_cards.py` | `lint_cards.py` | `build.py` |
|---|---|---|---|---|
| `checked/` | std-only code | compiled, `clippy -D warnings`, `tests:` run | ✓ | ✓ |
| `unchecked/` | external crates, code fragments (a single `match` arm, a builder chain) | skipped | ✓ | ✓ |

```bash
python check_cards.py     # cards/ + additional_cards/checked/
python lint_cards.py      # cards/ + both additional folders
python build.py           # CodeCards.apkg + AdditionalCards.apkg
```

## Decks

`<topic>.yaml` becomes the subdeck `Rust Language Kata::Additional::<Topic>`;
`a__b.yaml` nests as `Additional::A::B`. A file with the **same name in both
folders lands in one deck**, so `checked/iced.yaml` (std-only helpers) and
`unchecked/iced.yaml` (real `iced` code) study together as `Additional::Iced`.

Additional decks use the Core preset (14 new cards/day, random order); change it
in Anki's Deck Options if you want a different pace.

## Privacy

Your topic files are **gitignored** — only the `_example.yaml` files are tracked —
so project code you write cards about never ends up in a commit. If you fork the
repo and *want* your topics versioned, remove the `additional_cards/` lines from
`.gitignore`.

## Examples

`checked/_example.yaml` and `unchecked/_example.yaml` show one code card and one
concept card each. Files starting with `_` are examples: they're checked and
linted (so they stay valid), but **not** built into `AdditionalCards.apkg`. To
preview one in Anki anyway, build it explicitly:

```bash
python build.py additional_cards/checked/_example.yaml
```

Start your own topic by copying an example without the `_`:

```bash
cp additional_cards/checked/_example.yaml additional_cards/checked/my_topic.yaml
```
