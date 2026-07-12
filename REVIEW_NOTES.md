# Card review notes (2026-07-12)

Audit of the eight original core decks, now fully worked through. Remaining
items are low-priority polish, not correctness gaps — everything else in the
original backlog is done and verified.

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

## Remaining book coverage (candidates for future decks)

Second half of the book still uncovered: modules & visibility (ch. 7),
automated tests (ch. 11), OOP/state pattern (ch. 18), advanced features
(ch. 20: unsafe, macros), async (ch. 17). Given the interview focus, ch. 11
(tests) and ch. 17 (async) are probably next in value.

## Toolchain note

Two NeetCode solutions require newer std APIs than the 1.75 toolchain this
repo's harness is pinned to: `Option::is_none_or` (≥ 1.82,
`neetcode__sliding_window.yaml`) and `is_multiple_of` (≥ 1.87,
`neetcode__greedy.yaml`) — these two files are excluded from the 1.75
`check_cards.py` sweep but are otherwise unchanged. (A third file,
`neetcode__binary_search.yaml`, initially looked toolchain-gated too, but the
actual failure was two `if`/`else if`/`else` chains tripping clippy's
`comparison_chain` lint — rewritten as `match ....cmp(&target)`, it now
compiles and passes clean on 1.75 as well.) Everything else — 389 compileable
blocks across all other decks — compiles clean, lint-free, and passes on
1.75. README mentions the floor.
