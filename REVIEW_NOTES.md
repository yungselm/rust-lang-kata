# Card review notes (2026-07-12)

Findings from a full audit of the eight original core decks, plus what was
already fixed. Use this as a backlog; delete items as they're addressed.

## Already fixed

- Stale book-section references updated to the current (2024-edition) chapter
  numbering: patterns are ch. 19 (`matching.yaml`, 14 sources), advanced traits
  are ch. 20 (`traits.yaml`, 3 sources), DSTs are ch. 20 (`generics.yaml`),
  `iter()/iter_mut()/into_iter()` concept is §13.2 not §13.1
  (`iterators.yaml`), `let else` now points at §6.3 where the current book
  teaches it. Sources are display-only, so no card guids changed.
- README deck table updated (counts were stale: iterators 38, hashmaps 27,
  generics 20, datastructures 28) and the five new decks added.

## Biggest gap: missing `tests:` blocks

`generics.yaml` and `traits.yaml` are fully tested; in the other decks only the
Rustlings-derived cards have tests. Code cards without tests: iterators ~25,
matching ~20, results ~23, vectors ~24, hashmaps ~21 (≈113 cards). These only
get the clippy gate today, so a wrong-but-compiling solution would slip
through. Worth adding wholesale.

Side effect worth knowing: `most_common` (hashmaps) has an unspecified
tie-break (depends on random HashMap iteration order) — any test must use
inputs with a unique winner, or the card should specify a tie-break.

## Duplicates / overlap to consolidate

Within/across the original decks:

- Collect-into-`Result` short-circuit appears in both `iterators.yaml`
  (`parse_all`, `sum_parsed`, plus a concept card) and `results.yaml`
  (`result_with_list` / `list_of_results`). Keep both drills if intentional,
  but consider cross-referencing in notes.
- The four consecutive `windows(2)`/`|&w|` unsized-peel concept cards in
  `iterators.yaml` teach one lesson four times → collapse to ~2.
- `iterators.yaml reversed` vs `generics.yaml reversed` (same drill, generic).
- `hashmaps.yaml`: `char_counts` (`or_insert(0)`) vs `count_with_default`
  (`or_default()`) near-duplicates; also two entry-API concept cards.
- `datastructures.yaml` duplicates `hashmaps.yaml` on the entry API and
  HashMap ordering concepts.

Overlap with the new decks (decide which deck owns the topic):

- `datastructures.yaml` has three string concepts (String vs &str, bytes vs
  chars, char counting) now covered more deeply in `strings.yaml` → trim from
  datastructures.
- `traits.yaml` "Why is cloning an Rc/Arc cheap?" → now owned by
  `smartpointers.yaml`.
- `traits.yaml make_adder` and `generics.yaml map_each` overlap
  `closures.yaml`, but justifiably (they drill impl-Trait-return / generic
  bounds) → keep.

## High-yield cards still missing (per deck)

- iterators: `unzip`; `reduce` or `min_by_key` (only max is covered);
  `peekable`/`peek`.
- matching: `_` vs `..` ignoring; or-pattern binding (`Some(1 | 2)`); nested
  enum-in-struct destructure.
- results: `transpose()`; `or_else`; `Option::zip`.
- vectors: `rotate_left/right`; `split_at`; `sort_by` with custom comparator
  (descending).
- hashmaps: `HashMap::from([...])` literal; `or_insert_with` code card;
  HashSet `union`/`difference`.
- generics: const generics; two-bound rewrite (`PartialOrd + Clone` min);
  generic method with its own extra type parameter.
- traits: `TryFrom`/`TryInto`; blanket impl; manual `Ord`/`PartialOrd`.
- datastructures: `BinaryHeap` complexity card; recursion space-complexity;
  side-by-side collection cheat-sheet card. Also: this deck has no `source:`
  fields at all (inconsistent with the others).

## Remaining book coverage (candidates for future decks)

Second half of the book still uncovered after the five new decks: modules &
visibility (ch. 7), automated tests (ch. 11), OOP/state pattern (ch. 18),
advanced features (ch. 20: unsafe, advanced traits beyond current cards,
macros), async (ch. 17). Given the interview focus, ch. 11 (tests) and ch. 17
(async) are probably next in value.

## Toolchain note

Two NeetCode solutions require newer std APIs: `Option::is_none_or` (≥ 1.82,
sliding_window #4) and `is_multiple_of` (≥ 1.87, greedy #4). Everything else —
including all 110 new cards — compiles clean on 1.75. README now mentions the
floor.
