# Ideas / backlog

## `Rust::Neetcode::Tradeoffs` deck (planned ~Sept 2026)

A future deck of **"improve this solution"** cards. The editor is pre-filled with a
*correct but suboptimal* solution; the task is to rewrite it as a faster/leaner one.
The line-diff then checks your rewrite against the better approach, and the notes
explain the tradeoff (asymptotics vs constant factors, early-exit, memory, the
hasher, cache locality, ...).

**Format** — reuse the existing code-card mechanic:
- `instruction`: "Here's a working solution to <problem>. Rewrite it to be faster/use less memory; explain the win."
- `starter`: the suboptimal solution (pre-filled).
- `solution`: the improved version.
- `tests`: verify correctness (same as the normal NeetCode cards).
- `notes`: why it's better — and importantly, when the "slower" one actually wins.
- `source`: the NeetCode problem.

**Seed example (from review):**
- *Contains Duplicate* — sort + adjacent scan `O(n log n)` vs `HashSet` `O(n)`.
  Teaches that Big-O hides constants: the sort version is cache-friendly with cheap
  `i32` compares and no allocation, while the HashSet pays SipHash + scattered bucket
  probes + table growth — so the "worse" complexity is often faster in practice.
  Counterpoints: the HashSet short-circuits on an early duplicate, a faster hasher
  (ahash/FxHash) flips it, and large `n` eventually favors `O(n)`.
- (collect more of these as they come up during review)

**Trigger:** start once ~half of the current deck is learned (~75 days out from
2026-06-18). A scheduled reminder is set for that date.
