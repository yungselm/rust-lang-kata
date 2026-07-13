# rust-lang-kata

<figure class="epigraph" style="text-align: center; font-style: italic;">
  <blockquote>
    "Kata is a Japanese term meaning 'form' that refers to detailed choreographed patterns of movements practiced in martial arts. It serves as a training tool to memorize and perfect techniques."
  </blockquote>
</figure>

Anki decks for learning **Rust**, built from plain YAML. The idea is to create a set of cards containing the most important Rust concepts, that should be drilled over and over. The maximum number of cards should not exceed 2000 cards, this number is based on the idea of a basic vocabulary for languages typically containing 2000 words. Additionaly, the 150 Neetcode quesions are included, since this still represents a large part of job interviews. And who doesn't dream of writing Rust for a living😉...

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

## Current decks (602 cards)

**Core Rust (452)** — idiomatic patterns to drill to fluency (decks under `Rust::Core::…`), covering the full book front-to-back:

| File | Cards | Focus |
|------|-------|-------|
| `iterators.yaml` | 41 | map/filter/filter_map, collect into Result, fold, zip/unzip, flat_map, partition, scan, windows; `product`, capitalize, HashMap counting; reduce, peekable/peek; iter vs into_iter, laziness |
| `matching.yaml` | 28 | enums, `if let`/`while let`/`let else`, guards, `@` bindings (incl. combined with or-patterns), or/range/tuple/struct/slice patterns, match ergonomics, rich-enum dispatch, deep nested destructuring |
| `results.yaml` | 33 | `?`, unwrap_or family, map/map_err/and_then, ok_or, Option↔Result, transpose, or_else, zip, custom error enum, `Box<dyn Error>`, `Result<Vec>` vs `Vec<Result>` |
| `vectors.yaml` | 32 | build/access/mutate, sort/dedup/retain, slicing, windows/chunks, binary_search, drain, enum-in-Vec, rotate_left/right, split_at, sort_by; `&[T]` vs `&Vec<T>` |
| `hashmaps.yaml` | 30 | insert/get, entry API (or_insert/_with/_default/and_modify), literal construction, iteration, accumulate structs, HashSet & set ops (union/difference/intersection) |
| `traits.yaml` | 29 | implement Display/From/TryFrom/Default/PartialEq/Add/Ord/Iterator, custom traits, default methods, `derive`, `impl Trait`, `dyn` objects, supertraits, multiple bounds, blanket impls; Copy vs Clone & `.copied()`/`.cloned()` |
| `datastructures.yaml` | 27 | Big-O of Vec/VecDeque/HashMap/BTreeMap/BinaryHeap, search/sort complexity, recursion space, when-to-use cheat sheet, amortization |
| `closures.yaml` | 25 | Fn/FnMut/FnOnce, capture modes, `move`, returning closures, `Box<dyn Fn>`, closures in structs, fn pointers, choosing the right bound for APIs |
| `testing.yaml` | 21 | `#[test]`, assert!/assert_eq!/assert_ne!, custom failure messages, `#[should_panic]` (+ `expected`), tests returning `Result`, `#[ignore]`, unit vs integration tests, private-function testing, doc-tests, table-driven tests, `--nocapture` |
| `async.yaml` | 21 | async fns are lazy state machines, `Future`/`Poll`/`Waker`, hand-rolled `block_on`, chained/multi-poll futures, a join combinator, `#[tokio::main]`, `spawn`, `join!`/`select!`, blocking pitfalls, async-vs-threads tradeoffs, Pin/Unpin |
| `generics.yaml` | 23 | rewrite a concrete fn to generic: PartialOrd/Copy/Clone/PartialEq/Display/Sum bounds, `where` clauses, `Fn` bound, generic struct, const generics, generic methods; monomorphization |
| `lifetimes.yaml` | 22 | annotations vs elision (the three rules), structs/enums holding references, `'_`, `'static` vs `T: 'static`, `split_at_mut`, NLL, zero-copy parser shapes |
| `smartpointers.yaml` | 21 | Box (recursive types, `dyn`), Deref & coercion, Drop, Rc/`Rc::clone`/counts, RefCell & interior mutability, Cell vs RefCell, Weak & cycles, get_mut |
| `strings.yaml` | 22 | String vs &str, UTF-8 (bytes/chars/char_indices), building & joining, split/split_once/lines, find/replace/strip_prefix, parse pipelines, from_utf8 |
| `concurrency.yaml` | 20 | thread::spawn/join, `move`, scoped threads, mpsc (fan-in, pipelines, shutdown via drop), Mutex/MutexGuard, Arc, RwLock, atomics, Send/Sync |
| `modules.yaml` | 20 | packages/crates, module tree, `mod`, `pub`/`pub(crate)`/`pub(in path)`, `use`, re-exports, paths (`self`/`super`/`crate`), splitting modules across files |
| `oop.yaml` | 18 | encapsulation, trait objects (`dyn`), default methods, the state pattern (`Post`/`Draft`/`Published`), typestate pattern, object safety (`where Self: Sized`), builder pattern, trait objects vs enum match |
| `advanced.yaml` | 19 | unsafe superpowers (raw pointers, unsafe fn, FFI/`extern "C"`, statics, unsafe traits), `macro_rules!`, macro hygiene, newtype vs type alias, the never type `!`, fully-qualified syntax for disambiguation |

**NeetCode 150 (150)** — interview problems grouped by pattern, nested under `Rust::Neetcode::…`:

| File | Cards | Pattern |
|------|-------|---------|
| `neetcode__arrays_hashing.yaml` | 9 | hashing, prefix products, dedup |
| `neetcode__two_pointers.yaml` | 5 | opposite-end / fast-slow pointers |
| `neetcode__sliding_window.yaml` | 6 | fixed & variable windows |
| `neetcode__stack.yaml` | 7 | monotonic stacks, parsing |
| `neetcode__binary_search.yaml` | 7 | search-on-answer, rotated arrays |
| `neetcode__linked_list.yaml` | 11 | pointer rewiring, Floyd's cycle |
| `neetcode__trees.yaml` | 15 | DFS/BFS, BST, recursion |
| `neetcode__tries.yaml` | 3 | prefix trees |
| `neetcode__heap.yaml` | 7 | top-k, two-heap median |
| `neetcode__backtracking.yaml` | 9 | subsets, permutations, combinations |
| `neetcode__graphs.yaml` | 13 | grid BFS/DFS, topological sort, union-find |
| `neetcode__advanced_graphs.yaml` | 6 | Dijkstra, MST, Bellman-Ford, Euler |
| `neetcode__dp_1d.yaml` | 12 | 1-D dynamic programming |
| `neetcode__dp_2d.yaml` | 11 | grid & interval DP |
| `neetcode__greedy.yaml` | 8 | greedy strategies |
| `neetcode__intervals.yaml` | 6 | sort + sweep |
| `neetcode__math_geometry.yaml` | 8 | matrix ops, number theory |
| `neetcode__bit_manipulation.yaml` | 7 | XOR tricks, bit DP |

## Sources & attribution

Every card records where its content comes from in a `source:` field (shown small on the back).

- **Core Rust decks** are grounded in primary, openly-licensed material: the [Rust standard library docs](https://doc.rust-lang.org/std/), [*The Rust Programming Language* ("the book")](https://doc.rust-lang.org/book/), [Rustlings](https://github.com/rust-lang/rustlings), and [Rust by Example](https://doc.rust-lang.org/rust-by-example/). Solutions are checked against `clippy` so they reflect current idiomatic style rather than any one author's habits.
- **NeetCode 150 decks** follow the **[NeetCode 150](https://neetcode.io/practice)** list — a widely-used, pattern-organized index of common interview problems. We use that list **only as the index of which problems to cover and how to group them**. Every problem statement here is an **original paraphrase** written for this repo; LeetCode's problem text is copyrighted and is **not** reproduced, and nothing was scraped from LeetCode. Every solution is **original idiomatic Rust written and verified for this repo** (compiled, `clippy`-clean, and unit-tested via `check_cards.py`), implementing the standard well-known algorithm for each problem — not copied from LeetCode or NeetCode editorial solutions. A few problems are modeled to be testable in safe Rust (e.g. linked-list cycle and copy-with-random-pointer use index-based representations, binary trees use `Option<Box<TreeNode>>`, Clone Graph uses an adjacency list); each such card explains the modeling in its prompt.

## Recommended deck settings

This deck is designed for **FSRS** (Anki's modern scheduler — enable it once in any
Deck Options page, it applies collection-wide). FSRS schedules from a desired-retention
target, so the old SM-2 knobs (starting ease, easy bonus, interval modifier, hard/new
interval, graduating/easy interval) don't apply and aren't listed.

Set up two presets — one per study group:

| Setting | `Rust Core` | `Rust NeetCode` |
|---|---|---|
| New cards / day | 14 | 1 |
| Maximum reviews / day | 9999 | 9999 |
| Desired retention | 0.90 | 0.90 |
| Learning / relearning steps | 1m 10m / 10m | 1m 10m / 10m |
| Maximum interval | 36500d | 36500d |
| Leech threshold / action | 5 / tag only | 5 / tag only |
| New card gather order | **Random notes** | **Deck** (keeps `01`–`18` topic order) |
| New card sort order | Order gathered | Order gathered |

NeetCode order is guaranteed by the `01`–`18` topic-number prefixes on the subdecks
(`Rust::Neetcode::01 Arrays Hashing` … `18 Bit Manipulation`), so it stays correct
under any gather order — no position fiddling needed. Within a topic, cards are in
authored easy→hard order.

To apply: open Deck Options on **`Rust::Core`**, create a preset `Rust Core` with the
values above, then the preset menu → **Save to all subdecks** (the parent's 14/day cap
then bounds the daily total across the eighteen core subdecks). Repeat from **`Rust::Neetcode`**
with `Rust NeetCode` (1/day). Study the two groups as two separate daily sessions →
14 random core cards + 1 NeetCode card in topic order. Change any number anytime.

> **Core must use gather order "Random notes."** On the default **Deck** order you'd
> only see one subdeck at a time (e.g. all of `Datastructures`) until it empties.
> NeetCode is the opposite — keep it on **Deck** so the `01`–`18` topics feed in order.

(`build.py` also embeds these presets, but Anki's importer ignores embedded presets for
non-Anki-generated `.apkg`s, so set them once as above — see `RELEASE.md` for shipping
presets to others.)

## Adding / editing cards

```yaml
# code card (default) — you write the body; the diff checks it
- instruction: |
    What to write. Use `backticks` for inline code; generics like Vec<T> are fine.
  starter: |          # optional pre-filled scaffold (signature, `use` lines)
    fn add_one(n: i32) -> i32 {

    }
  solution: |
    fn add_one(n: i32) -> i32 {
        n + 1
    }
  notes: |            # optional, shown on the back
    Why it works.
  source: "std Iterator::map"   # optional provenance, shown on the back
  tags: [rust, iterators]
  tests: |            # optional asserts run by `cargo test` (see check_cards.py)
    assert_eq!(add_one(1), 2);

# concept card — recall
- type: concept
  question: |
    What is X?
  answer: |
    **X is, in one direct sentence, the actual answer.** Then the supporting
    detail, caveats, and "why" go here, in as many sentences as needed.
  code: |             # optional snippet shown highlighted on the back
    let x = 1;
  source: "book §8.3"  # optional
  tags: [rust, concept]
```

**Concept card answers should lead with one bolded (`**...**`) sentence that
directly answers the question**, then elaborate below. Anki is self-graded —
you decide "correct" or "wrong" yourself — and a long undifferentiated
paragraph makes that easy to fudge: you skim it, spot a half-matching phrase,
and let yourself off the hook instead of honestly checking what you actually
recalled. A short bolded lead sentence gives you one crisp claim to check
your recall against before you read the reasoning behind it. `**bold**` in
any text field (`question`/`answer`/`notes`/`instruction`/`source`) renders as
`<strong>` via `build.py`'s `text()` helper, the same way `` `backticks` ``
become `<code>`.

Rebuild with `python build.py` (or `python build.py cards/match.yaml` for one
file). Re-importing **updates** existing cards (guids are stable per instruction /
question); changing that text creates a new card.

## Compile-checking the Rust

`check_cards.py` extracts every code-card `solution` (plus concept `code`
snippets), wraps each in its own module in a generated crate, and runs two gates:

1. **`cargo clippy -- -D warnings`** — compile errors, ordinary warnings (unused
   vars, needless `mut`, unused imports, ...), and clippy's idiomatic lints
   (needless borrows, redundant clones, manual loops, ...), keeping solutions idiomatic.
2. **`cargo test`** — runs each card's `tests:` asserts, so a solution must be
   *correct*, not just compile. Dead-code from the wrapping is suppressed.

```bash
python check_cards.py                              # all cards (needs cargo; clippy via `rustup component add clippy`)
python check_cards.py cards/neetcode__trees.yaml   # just one file
```

A recent stable toolchain is assumed: a couple of solutions use newer std APIs
(`Option::is_none_or` needs Rust ≥ 1.82, `is_multiple_of` needs ≥ 1.87).

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
