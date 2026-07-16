# Contributing

**The primary goal is building the best possible Rust card set together.**

The most valuable contribution is adding or improving cards in `cards/*.yaml` —
no Rust toolchain is required just to edit YAML. Improving the build system or
templates is also welcome. The one hard requirement for code changes is that
`clippy` passes without warnings, to keep solutions idiomatic.

## Workflow

1. Fork → edit a `cards/*.yaml` file (or add a new one).
2. `python lint_cards.py` — flags cards that aren't self-contained (e.g. "like
   the previous card").
3. `python check_cards.py` — compiles every card's solution, runs `clippy -D
   warnings`, and runs each card's `tests:` block.
4. `python build.py` — rebuilds `output/CodeCards.apkg`; smoke-test it in Anki,
   or preview the look by opening `preview.html` in a browser.
5. Open a PR using the provided template.

CI runs the same three scripts (`lint_cards.py`, `check_cards.py`, `build.py`)
on every push and pull request, so a green check confirms the deck still
compiles, lints clean, and builds.

## Reporting issues

- **A card is wrong, unclear, or won't compile** → open a "Card issue".
- **You have an idea for a new card/topic** → open a "New card / topic
  suggestion".
- **Something in the build/templates is broken** → open a "Bug report".

## Card budget

The deck is capped at roughly 2000 cards (a rough "basic vocabulary" size for
a language). New cards should earn their place — prefer improving or
tightening an existing card over adding a marginal one once a topic is well
covered.
