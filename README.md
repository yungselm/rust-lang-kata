# rust-lang-kata

<figure class="epigraph" style="text-align: center; font-style: italic;">
  <blockquote>
    "Kata is a Japanese term meaning 'form' that refers to detailed choreographed patterns of movements practiced in martial arts. It serves as a training tool to memorize and perfect techniques."
  </blockquote>
</figure>

Anki decks for learning **Rust**, built from plain YAML. The idea is to create a set of cards containing the most important Rust concepts, that should be drilled over and over. The maximum number of cards should not exceed 2000 cards, this number is based on the idea of a basic vocabulary for languages typically containing 2000 words. Additionaly, a maximum of 500 algorithm cards should be included (based on Leetcode), since this still represents a large part of job interviews.

## Contributing

**The primary goal is building the best possible Rust card set together.**
If you want to help, the most valuable contribution is adding or improving cards in `cards/*.yaml`. No Rust toolchain is required just to edit YAML (though running `python check_cards.py` before a PR is appreciated so all solutions stay warning-free).

Improving the build system or templates is also welcome. The one hard requirement for code changes is that clippy passes without warnings to keep solutions idiomatic.

Quick card-contribution workflow:
1. Fork → edit a `cards/*.yaml` file (or add a new one)
2. `python check_cards.py` to verify solutions compile cleanly
3. `python build.py` to rebuild the `.apkg` and smoke-test in Anki
4. Open a PR

## The code base

Two card styles:

- **Code cards**: A small in-card editor (CodeMirror, VS Code-style dark theme,
  Tab to indent, auto-closing brackets, no autocomplete). You type the function
  body, on flip, lines that differ from the solution are washed transparent red,
  and the reference solution is shown below.
  ![Code Card](https://raw.githubusercontent.com/yungselm/rust-lang-kata/main/media/code_card.gif)
- **Concept cards**: Simple question / answer recall (used for Big-O and other
  facts), with an optional highlighted example and images on the back.

Cards live in `cards/*.yaml`. Each file becomes its own subdeck (`Rust::<Topic>`).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python check_cards.py           # checks that clippy runs without warnings
python build.py                 # writes output/CodeCards.apkg
```

Import `output/CodeCards.apkg` into Anki (keep "Update notetypes" checked).
Preview the look without Anki by opening `preview.html` in a browser.

## Current decks (157 cards)

| File | Cards | Focus |
|------|-------|-------|
| `iterators.yaml` | 29 | map/filter/filter_map, collect into Result, fold, zip, flat_map, partition, scan, windows; iter vs into_iter, laziness |
| `matching.yaml` | 24 | enums, `if let`/`while let`/`let else`, guards, `@` bindings, or/range/tuple/struct/slice patterns, match ergonomics |
| `results.yaml` | 27 | `?`, unwrap_or family, map/map_err/and_then, ok_or, Option↔Result, map_or(_else), `From` errors |
| `vectors.yaml` | 28 | build/access/mutate, sort/dedup/retain, slicing, windows/chunks, binary_search, drain; `&[T]` vs `&Vec<T>` |
| `hashmaps.yaml` | 25 | insert/get, entry API (or_insert/_with/_default/and_modify), iteration, HashSet & set ops |
| `datastructures.yaml` | 24 | Big-O of Vec/VecDeque/HashMap/BTreeMap, search/sort complexity, when-to-use, amortization |

## Adding / editing cards

```yaml
# code card (default) — you write the body; the diff checks it
- instruction: |
    What to write. Use `backticks` for inline code; generics like Vec<T> are fine.
  starter: |          # optional pre-filled scaffold (signature, `use` lines)
    fn foo() {

    }
  solution: |
    fn foo() {
        println!("hi");
    }
  notes: |            # optional, shown on the back
    Why it works.
  tags: [rust, iterators]

# concept card — recall
- type: concept
  question: |
    What is X?
  answer: |
    The answer.
  code: |             # optional snippet shown highlighted on the back
    let x = 1;
  tags: [rust, concept]
```

Rebuild with `python build.py` (or `python build.py cards/match.yaml` for one
file). Re-importing **updates** existing cards (guids are stable per instruction /
question); changing that text creates a new card.

## Compile-checking the Rust

`check_cards.py` extracts every code-card `solution` and concept `code` snippet,
wraps each in its own module/function in a generated crate, and builds it with
warnings denied, so it fails on compile errors **and** warnings (unused vars,
needless `mut`, unused imports, ...). Dead-code from the wrapping is suppressed.

```bash
python check_cards.py            # needs a local Rust toolchain (cargo)
```

On failure, each block is in a module named `sol_<topic>_<n>` / `ex_<topic>_<n>`
with a comment naming the card, so you can find the offending card fast. Run this
after editing solutions, before rebuilding the deck.

## How it works

- `build.py`: reads the YAML, builds two note types, one subdeck per file,
  HTML-escapes text fields (so `Vec<T>` renders) and turns `backticks` into
  `<code>`, version-stamps the JS/CSS assets, writes the `.apkg`.
- `templates/`: `front.html`/`back.html` (code), `front_concept.html`/
  `back_concept.html` (concept), `_cards.js` (editor + line diff), `style.css`
  (layout + the `vscdark` CodeMirror theme).
- `vendor/_*.js`, `_*.css`: CodeMirror 5 bundled offline (the leading `_` keeps
  Anki from deleting them). `_simple.js` must load before `_rust.js`.
- Typed code passes front → back via `sessionStorage`. The diff compares line by
  line, ignoring trailing whitespace.

## Credits

- **[CodeMirror 5](https://codemirror.net/5/)**: In-card code editor. Copyright © Marijn Haverbeke and contributors. [MIT License](https://codemirror.net/5/LICENSE).
- **[genanki](https://github.com/kerricklong/genanki)**: Python library for generating Anki `.apkg` files. MIT License.

The card content and build tooling in this repository are released under the [MIT License](LICENSE).

## Notes / gotchas

- Built for **modern Anki desktop**. When you change a **template** (not just cards),
  import with "Update notetypes" enabled. If it won't update, delete the note
  type once (Tools → Manage Note Types) and re-import.
- Bump `ASSET_VER` in `build.py` whenever you edit anything in `vendor/` or
  `templates/_cards.js`, so Anki reliably reloads the changed static files.
- `StarterCode`/`Solution`/`Code` fields are stored base64-encoded, so they look
  like gibberish in Anki's card browser. Edit cards via the YAML, not in Anki.
