# rust-lang-kata

<figure class="epigraph" style="text-align: center; font-style: italic;">
  <blockquote>
    "Kata is a Japanese term meaning 'form' that refers to detailed choreographed patterns of movements practiced in martial arts. It serves as a training tool to memorize and perfect techniques."
  </blockquote>
</figure>

Anki decks for learning **Rust**, built from plain YAML. The idea is to create a set of cards containing the most important Rust concepts, that should be drilled over and over. The maximum number of cards should not exceed 2000 cards, this number is based on the idea of a basic vocabulary for languages typically containing 2000 words. Additionaly, the 150 Neetcode quesions are included, since this still represents a large part of job interviews. And who doesn't dream of writing Rust for a living😉...

## Contributing

**The primary goal is building the best possible Rust card set together.**
The most valuable contribution is adding or improving cards in `cards/core/` and `cards/neetcode/` — no Rust toolchain is required just to edit YAML. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow (`asl fix` / `asl lint` / `asl check`) and how to report card issues or suggest new ones. CI runs the same checks on every PR.

The build system, editor card and checks now live in [agentic-studying-loop](https://github.com/yungselm/agentic-studying-loop); improvements to those are welcome there. This repo is only the cards.

## The code base

Two card styles:

- **Code cards**: A small in-card editor (CodeMirror, VS Code-style dark theme,
  Tab to indent, auto-closing brackets, no autocomplete). You type the function
  body, on flip, lines that differ from the solution are washed transparent red,
  and the reference solution is shown below.

![Code Card](https://raw.githubusercontent.com/yungselm/rust-lang-kata/main/media/code_card.gif)

- **Concept cards**: Simple question / answer recall (used for Big-O and other
  facts), with an optional highlighted example and images on the back.

Cards live in `cards/core/*.yaml` and `cards/neetcode/*.yaml`; each file becomes its own subdeck
(`Rust Language Kata::Core::<Topic>`, `Rust Language Kata::Neetcode::NN <Topic>`). The decks are built
with [agentic-studying-loop](https://github.com/yungselm/agentic-studying-loop) (`asl`), which
provides the editor card, the checks and the build.

## Quick start

```bash
uv tool install git+https://github.com/yungselm/agentic-studying-loop   # or: pipx install ...
asl check cards/core cards/neetcode       # clippy -D warnings + every card's tests (needs cargo + clippy)
asl build cards/core cards/neetcode -o output/CodeCards.apkg
```

Import `output/CodeCards.apkg` into Anki with **Update notetypes** and **Import any deck
presets** ticked. Re-importing updates existing cards in place.

## Current decks (690 cards)

**Core Rust (446)** — idiomatic patterns to drill to fluency (decks under `Rust Language Kata::Core::…`), covering the full book front-to-back:

| File | Cards | Focus |
|------|-------|-------|
| `iterators.yaml` | 40 | map/filter/filter_map, collect into Result, fold, zip/unzip, flat_map, partition, scan, windows; `product`, capitalize, HashMap counting; reduce; iter vs into_iter, laziness |
| `matching.yaml` | 28 | enums, `if let`/`while let`/`let else`, guards, `@` bindings (incl. combined with or-patterns), or/range/tuple/struct/slice patterns, match ergonomics, rich-enum dispatch, deep nested destructuring |
| `results.yaml` | 33 | `?`, unwrap_or family, map/map_err/and_then, ok_or, Option↔Result, transpose, or_else, zip, custom error enum, `Box<dyn Error>`, `Result<Vec>` vs `Vec<Result>` |
| `vectors.yaml` | 32 | build/access/mutate, sort/dedup/retain, slicing, windows/chunks, binary_search, drain, enum-in-Vec, rotate_left/right, split_at, sort_by; `&[T]` vs `&Vec<T>` |
| `hashmaps.yaml` | 29 | insert/get, entry API (or_insert/_with/_default/and_modify), literal construction, iteration, HashSet & set ops (union/difference/intersection) |
| `traits.yaml` | 29 | implement Display/From/TryFrom/Default/PartialEq/Add/Ord/Iterator, custom traits, default methods, `derive`, `impl Trait`, `dyn` objects, supertraits, multiple bounds, blanket impls; Copy vs Clone & `.copied()`/`.cloned()` |
| `datastructures.yaml` | 28 | Big-O of Vec/VecDeque/HashMap/BTreeMap/BinaryHeap, search/sort complexity, recursion space, when-to-use cheat sheet, amortization |
| `closures.yaml` | 25 | Fn/FnMut/FnOnce, capture modes, `move`, returning closures, `Box<dyn Fn>`, closures in structs, fn pointers, choosing the right bound for APIs |
| `testing.yaml` | 21 | `#[test]`, assert!/assert_eq!/assert_ne!, custom failure messages, `#[should_panic]` (+ `expected`), tests returning `Result`, `#[ignore]`, unit vs integration tests, private-function testing, doc-tests, table-driven tests, `--nocapture` |
| `async.yaml` | 18 | async fns are lazy state machines, `Future`/`Poll`/`Waker`, hand-rolled `block_on`, multi-poll futures, `#[tokio::main]`, `spawn`, `join!`/`select!`, blocking pitfalls, async-vs-threads tradeoffs, Pin/Unpin |
| `generics.yaml` | 23 | rewrite a concrete fn to generic: PartialOrd/Copy/Clone/PartialEq/Display/Sum bounds, `where` clauses, `Fn` bound, generic struct, const generics, generic methods; monomorphization |
| `lifetimes.yaml` | 21 | annotations vs elision (the three rules), structs/enums holding references, `'_`, `'static` vs `T: 'static`, `split_at_mut`, NLL, zero-copy tokenizing |
| `smartpointers.yaml` | 21 | Box (recursive types, `dyn`), Deref & coercion, Drop, Rc/`Rc::clone`/counts, RefCell & interior mutability, Cell vs RefCell, Weak & cycles, get_mut |
| `strings.yaml` | 21 | String vs &str, UTF-8 (bytes/chars/char_indices), building & joining, split/split_once/lines, find/replace/strip_prefix, parse pipelines, from_utf8 |
| `concurrency.yaml` | 20 | thread::spawn/join, `move`, scoped threads, mpsc (fan-in, pipelines, shutdown via drop), Mutex/MutexGuard, Arc, RwLock, atomics, Send/Sync |
| `modules.yaml` | 20 | packages/crates, module tree, `mod`, `pub`/`pub(crate)`/`pub(in path)`, `use`, re-exports, paths (`self`/`super`/`crate`), splitting modules across files |
| `oop.yaml` | 18 | encapsulation, trait objects (`dyn`), default methods, the state pattern (`Post`/`Draft`/`Published`), typestate pattern, object safety (`where Self: Sized`), builder pattern, trait objects vs enum match |
| `advanced.yaml` | 19 | unsafe superpowers (raw pointers, unsafe fn, FFI/`extern "C"`, statics, unsafe traits), `macro_rules!`, macro hygiene, newtype vs type alias, the never type `!`, fully-qualified syntax for disambiguation |

**Reading & judgment (94)** — reading and improving code, not just recalling syntax; also under `Rust Language Kata::Core::…`:

| File | Cards | Focus |
|------|-------|-------|
| `review.yaml` | 25 | code review — spot & fix a bug / perf / idiom / safety / allocation smell (rewrite it) |
| `refactor.yaml` | 12 | rewrite working-but-verbose code idiomatically (loops → iterators, `match` → combinators) |
| `predict.yaml` | 14 | predict the behaviour — what prints, does it compile, what's the value, and why |
| `design.yaml` | 15 | design decisions — pick the right type / collection / pattern and know when the alternative wins |
| `debugging.yaml` | 14 | diagnose real `rustc` / borrow-checker errors (E0382/E0499/E0502/E0106/…) → cause + fix |
| `edgecases.yaml` | 14 | find the input that breaks a function (overflow, empty, UTF-8 boundary, `unwrap`, negative `%`, …) |

**NeetCode 150 (150)** — interview problems grouped by pattern, nested under `Rust Language Kata::Neetcode::…`:

| File | Cards | Pattern |
|------|-------|---------|
| `01_arrays_hashing.yaml` | 9 | hashing, prefix products, dedup |
| `02_two_pointers.yaml` | 5 | opposite-end / fast-slow pointers |
| `03_sliding_window.yaml` | 6 | fixed & variable windows |
| `04_stack.yaml` | 7 | monotonic stacks, parsing |
| `05_binary_search.yaml` | 7 | search-on-answer, rotated arrays |
| `06_linked_list.yaml` | 11 | pointer rewiring, Floyd's cycle |
| `07_trees.yaml` | 15 | DFS/BFS, BST, recursion |
| `08_tries.yaml` | 3 | prefix trees |
| `09_heap.yaml` | 7 | top-k, two-heap median |
| `10_backtracking.yaml` | 9 | subsets, permutations, combinations |
| `11_graphs.yaml` | 13 | grid BFS/DFS, topological sort, union-find |
| `12_advanced_graphs.yaml` | 6 | Dijkstra, MST, Bellman-Ford, Euler |
| `13_dp_1d.yaml` | 12 | 1-D dynamic programming |
| `14_dp_2d.yaml` | 11 | grid & interval DP |
| `15_greedy.yaml` | 8 | greedy strategies |
| `16_intervals.yaml` | 6 | sort + sweep |
| `17_math_geometry.yaml` | 8 | matrix ops, number theory |
| `18_bit_manipulation.yaml` | 7 | XOR tricks, bit DP |

## Sources & attribution

Every card records where its content comes from in a `source:` field (shown small on the back).

- **Core Rust decks** are grounded in primary, openly-licensed material: the [Rust standard library docs](https://doc.rust-lang.org/std/), [*The Rust Programming Language* ("the book")](https://doc.rust-lang.org/book/), [Rustlings](https://github.com/rust-lang/rustlings), and [Rust by Example](https://doc.rust-lang.org/rust-by-example/). Solutions are checked against `clippy` so they reflect current idiomatic style rather than any one author's habits.
- **NeetCode 150 decks** follow the **[NeetCode 150](https://neetcode.io/practice)** list — a widely-used, pattern-organized index of common interview problems. We use that list **only as the index of which problems to cover and how to group them**. Every problem statement here is an **original paraphrase** written for this repo; LeetCode's problem text is copyrighted and is **not** reproduced, and nothing was scraped from LeetCode. Every solution is **original idiomatic Rust written and verified for this repo** (compiled, `clippy`-clean, and unit-tested via `asl check`), implementing the standard well-known algorithm for each problem — not copied from LeetCode or NeetCode editorial solutions. A few problems are modeled to be testable in safe Rust (e.g. linked-list cycle and copy-with-random-pointer use index-based representations, binary trees use `Option<Box<TreeNode>>`, Clone Graph uses an adjacency list); each such card explains the modeling in its prompt.

## Recommended deck settings

This deck is designed for **FSRS** (Anki's modern scheduler — enable it once in any
Deck Options page, it applies collection-wide). FSRS schedules from a desired-retention
target, so the old SM-2 knobs (starting ease, easy bonus, interval modifier, hard/new
interval, graduating/easy interval) don't apply and aren't listed.

Set up two presets — one per study group:

| Setting | `Rust Language Kata Core` | `Rust Language Kata NeetCode` |
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
(`Rust Language Kata::Neetcode::01 Arrays Hashing` … `18 Bit Manipulation`), so it stays correct
under any gather order — no position fiddling needed. Within a topic, cards are in
authored easy→hard order.

To apply: open Deck Options on **`Rust Language Kata::Core`**, create a preset `Rust Language Kata Core` with the
values above, then the preset menu → **Save to all subdecks** (the parent's 14/day cap
then bounds the daily total across the twenty-four core subdecks). Repeat from **`Rust Language Kata::Neetcode`**
with `Rust Language Kata NeetCode` (1/day). Study the two groups as two separate daily sessions →
14 random core cards + 1 NeetCode card in topic order. Change any number anytime.

> **Core must use gather order "Random notes."** On the default **Deck** order you'd
> only see one subdeck at a time (e.g. all of `Datastructures`) until it empties.
> NeetCode is the opposite — keep it on **Deck** so the `01`–`18` topics feed in order.

(The build also embeds both presets, from `cards/*/deck.yaml`; Anki applies them when you
tick **Import any deck presets** on import. Otherwise set them once as above.)

## Adding / editing cards

The card format is described in agentic-studying-loop's
[card format](https://github.com/yungselm/agentic-studying-loop/blob/main/docs/card-format.md);
the short version:

```yaml
# code card (default): you type the gap; on flip, differing lines turn red
- instruction: |
    What to write. Use `backticks` for inline code; generics like Vec<T> are fine.
  starter: |          # pre-filled scaffold (signature, `use` lines)
    fn add_one(n: i32) -> i32 {

    }
  solution: |
    fn add_one(n: i32) -> i32 {
        n + 1
    }
  notes: |            # optional, shown on the back
    Why it works.
  source: "std Iterator::map"
  tags: [rust, iterators]
  tests: |            # asserts run by `asl check`
    assert_eq!(add_one(1), 2);

# concept card: recall, then grade yourself against the bold lead
- type: concept
  question: |
    What is X?
  answer: |
    **X is, in one direct sentence, the actual answer.** Then the detail.
  code: |             # optional snippet on the back (also compiled)
    let x = 1;
```

Leave out `id:`: `asl fix cards/core` assigns it (`rlk-NNN`, `nc-NNN` for NeetCode). The id
drives the Anki note, so later edits, the front included, update the card in place. Existing
cards also carry a frozen `guid:` from before the move to ids; leave it alone.

**Concept answers lead with one bolded sentence that directly answers the question.** Anki is
self-graded, and a long paragraph makes it easy to let yourself off the hook; one crisp claim
gives you something to check your recall against before you read the reasoning.

Before a PR:

```bash
asl fix   cards/core cards/neetcode                    # ids for new cards
asl lint  -q --skip size cards/core cards/neetcode     # self-contained, no duplicates
asl check cards/core cards/neetcode                    # clippy + tests
```

(`asl lint` without `--skip size` also reports cards over the data-derived size limits; many
older cards are, and splitting them is welcome.) A recent stable toolchain is assumed: a couple
of solutions use newer std APIs (`Option::is_none_or` needs Rust ≥ 1.82, `is_multiple_of` ≥ 1.87).

## Additional cards (your own topics)

For topics that aren't for everyone (a framework like `iced`, patterns from your own project),
make a deck folder in `additional_cards/`: copy `additional_cards/_example/` and edit its
`deck.yaml`. Your folders are gitignored. See [additional_cards/README.md](additional_cards/README.md).
For cards that follow a real project of yours, agentic-studying-loop's `asl init` sets up the
whole loop (study notes, an agent that writes the cards, checks against your repo).

## Credits

- **[CodeMirror 5](https://codemirror.net/5/)**: In-card code editor. Copyright © Marijn Haverbeke and contributors. [MIT License](https://codemirror.net/5/LICENSE).
- **[genanki](https://github.com/kerricklong/genanki)**: Python library for generating Anki `.apkg` files (used by agentic-studying-loop). MIT License.

The card content in this repository is released under the [MIT License](LICENSE).

## Notes / gotchas

- Built for **modern Anki desktop**. When you change a **template** (not just cards),
  import with "Update notetypes" enabled. If it won't update, delete the note
  type once (Tools → Manage Note Types) and re-import.
- `StarterCode`/`Solution`/`Code` fields are stored base64-encoded, so they look
  like gibberish in Anki's card browser. Edit cards via the YAML, not in Anki.
