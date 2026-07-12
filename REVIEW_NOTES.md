# Card review notes (2026-07-12)

Audit of the original core decks, now fully worked through, plus five new
decks completing full book coverage. Remaining items are low-priority polish,
not correctness gaps — everything else in the original backlog is done and
verified.

## Done

- Stale book-section references updated to the current (2024-edition) chapter
  numbering: patterns are ch. 19 (`matching.yaml`), advanced traits are ch. 20
  (`traits.yaml`), DSTs are ch. 20 (`generics.yaml`), `iter()/iter_mut()/
  into_iter()` concept is §13.2 not §13.1 (`iterators.yaml`), `let else` now
  points at §6.3. Sources are display-only, so no card guids changed.
- **Missing `tests:` blocks — fully backfilled.** Every code card in every
  core deck now has a `tests:` block; `check_cards.py` confirms all 353 core
  cards (382 compileable blocks, including concept `code:` snippets) compile,
  lint clean under `clippy -D warnings`, and pass. Nothing relies on the
  clippy gate alone anymore.
- `most_common` (hashmaps) tie-break risk addressed: its test input has a
  unique winner, so the unspecified HashMap iteration order can't flake it.
- **High-yield cards added to every deck on the original list:**
  - iterators: `unzip`, `reduce` (`overall_max`), `peekable`/`peek`
    (`count_leading_dupes`).
  - matching: `_` vs `..` concept card, or-pattern + `@` binding
    (`classify_die`), nested enum-in-struct destructure (`click_coords`).
  - results: `transpose`, `or_else` (`first_available`), `Option::zip` (`pair`).
  - vectors: `rotate_left`/`rotate_right` (`rotate`), `split_at`
    (`split_around`), `sort_by` descending (`sort_desc`).
  - hashmaps: `HashMap::from([...])` literal (`build_lit`), `or_insert_with`
    (`first_seen`), `HashSet::union`/`difference` (`all_and_only_a`).
  - generics: const generics (`sum_array`), two-bound rewrite (`clamp`),
    generic method with its own type parameter (`Pair::map`).
  - traits: `TryFrom`/`TryInto` (`Age`), blanket impl (`Double`), manual
    `Ord`/`PartialOrd` (`Priority`).
  - datastructures: `BinaryHeap` complexity + min/max-heap card, recursion
    space-complexity card, Vec/VecDeque/HashMap/BTreeMap/BinaryHeap
    side-by-side cheat sheet; every card now carries a `source:` field.
- Overlap trimmed: `datastructures.yaml`'s three string concepts (String vs
  &str, bytes vs chars, char counting) removed in favor of `strings.yaml`
  (kept the char-counting concept for its distinct interview framing);
  `traits.yaml`'s "Why is cloning an Rc/Arc cheap?" removed in favor of
  `smartpointers.yaml`; `hashmaps.yaml`'s duplicate entry-API/HashMap-ordering
  concepts removed from `datastructures.yaml`.
- README deck table and card counts refreshed (503 total: 353 core + 150
  NeetCode).
- **Full book coverage achieved — five new decks written for the previously
  uncovered second half of the book, each held to the same bar (every code
  card has a `tests:` block, clippy-clean under `-D warnings`, verified via
  `check_cards.py`):**
  - `testing.yaml` (21 cards, ch. 11 automated tests) — `#[test]`,
    assert!/assert_eq!/assert_ne! + custom messages, `#[should_panic]` (with
    and without `expected`), tests returning `Result`, `#[ignore]`, unit vs
    integration tests, testing private functions, doc-tests, table-driven
    tests via `match ....cmp()`, `--nocapture`.
  - `async.yaml` (21 cards, ch. 17 async/await) — async fns as lazy state
    machines, `Future`/`Poll`/`Waker`, a hand-rolled `block_on` executor
    (`RawWaker`/`RawWakerVTable`), chained `.await`, multi-poll
    Pending→Ready futures, a hand-rolled join combinator, plus prose-only
    concept cards for runtime-specific APIs (`#[tokio::main]`, `spawn`,
    `join!`/`select!`, blocking pitfalls, async-vs-threads tradeoffs,
    Pin/Unpin) since the harness has no network access to pull in tokio.
  - `modules.yaml` (20 cards, ch. 7 packages/crates/modules) — module tree,
    `mod`, `pub`/`pub(crate)`/`pub(in path)`, `use`, re-exports, paths
    (`self`/`super`/`crate`), splitting modules across files.
  - `oop.yaml` (18 cards, ch. 18 OOP features) — encapsulation, trait
    objects, default methods, the state pattern (`Post`/`Draft`/
    `Published`), the typestate pattern, object safety
    (`where Self: Sized`), the builder pattern, trait objects vs enum match.
  - `advanced.yaml` (19 cards, ch. 20 advanced features) — unsafe
    superpowers (raw pointers, unsafe fn, FFI/`extern "C"`, statics, unsafe
    traits), `macro_rules!` + hygiene, newtype vs type alias, the never
    type `!`, fully-qualified syntax for disambiguation.
  - New grand total: **602 cards** (452 core + 150 NeetCode), all 429
    checkable blocks (across every deck except the two toolchain-gated
    NeetCode files, see below) compiling, lint-clean, and passing on the
    1.75 toolchain.

## Still open (minor, deferred)

- The four consecutive `windows(2)`/`|&w|` unsized-peel concept cards in
  `iterators.yaml` teach one lesson four times → could collapse to ~2.
  Left as-is since each frames the rule from a different angle (map closure,
  general pattern rule, safe default, scope of the rule) and none are wrong.
- `iterators.yaml reversed` vs `generics.yaml reversed` — same drill, one
  concrete one generic. Intentional pairing (concrete-first, then the
  generic rewrite), so left alone.
- `hashmaps.yaml`: `char_counts` (`or_insert(0)`) vs `count_with_default`
  (`or_default()`) are near-duplicates by design — they contrast the two
  entry-API idioms side by side, so kept both.
- Collect-into-`Result` short-circuit appears in both `iterators.yaml`
  (`parse_all`, `sum_parsed`) and `results.yaml` (`result_with_list` /
  `list_of_results`) — intentional cross-deck reinforcement of the same
  idiom from two contexts, left as-is.

## Book coverage

The book is now covered front-to-back across the fourteen core-Rust decks
listed in the README (Core Rust section), plus `testing.yaml`, `async.yaml`,
`modules.yaml`, `oop.yaml`, and `advanced.yaml` added this pass. No chapters
remain untouched; any future work here is depth/polish on existing decks
rather than new-chapter coverage.

## Toolchain note

Two NeetCode solutions require newer std APIs than the 1.75 toolchain this
repo's harness is pinned to: `Option::is_none_or` (≥ 1.82,
`neetcode__sliding_window.yaml`) and `is_multiple_of` (≥ 1.87,
`neetcode__greedy.yaml`) — these two files are excluded from the 1.75
`check_cards.py` sweep but are otherwise unchanged. (A third file,
`neetcode__binary_search.yaml`, initially looked toolchain-gated too, but the
actual failure was two `if`/`else if`/`else` chains tripping clippy's
`comparison_chain` lint — rewritten as `match ....cmp(&target)`, it now
compiles and passes clean on 1.75 as well.) Everything else — 429 compileable
blocks across all other decks, including the five decks added this pass —
compiles clean, lint-free, and passes on 1.75. README mentions the floor.
