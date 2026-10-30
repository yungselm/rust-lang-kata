# Contributing

**The primary goal is building the best possible Rust card set together.**

The most valuable contribution is adding or improving cards in `cards/core/` and
`cards/neetcode/` (no Rust toolchain is required just to edit YAML). Solutions must pass
`clippy` without warnings, to keep them idiomatic.

## Workflow

The tooling is [agentic-studying-loop](https://github.com/yungselm/agentic-studying-loop):
`uv tool install git+https://github.com/yungselm/agentic-studying-loop`.

1. Fork → edit a card file (or add one; each file is a subdeck).
2. `asl fix cards/core cards/neetcode`: gives new cards their ids.
3. `asl lint -q --skip size cards/core cards/neetcode`: flags cards that aren't
   self-contained (e.g. "like the previous card"), duplicates and id problems.
4. `asl check cards/core cards/neetcode`: compiles every solution, runs
   `clippy -D warnings` and each card's `tests:` block.
5. `asl build cards/core cards/neetcode -o output/CodeCards.apkg` and smoke-test it in Anki.
6. Open a PR using the provided template.

CI runs the same steps on every push and pull request.

## Reporting issues

- **A card is wrong, unclear, or won't compile** → open a "Card issue".
- **You have an idea for a new card/topic** → open a "New card / topic suggestion".
- **The build, editor or checks are broken** → open an issue in agentic-studying-loop.

## Card budget

The deck is capped at roughly 2000 cards (a rough "basic vocabulary" size for a language,
even though I would argue for these patterns 1000 would be more appropriate). New cards
should earn their place — prefer improving or tightening an existing card over adding a
marginal one once a topic is well covered.

Niche topics (a specific framework, your own project) don't belong in `cards/` — put them
in a deck folder under `additional_cards/` instead; see
[additional_cards/README.md](additional_cards/README.md).
