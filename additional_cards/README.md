# Additional cards

Your own topics (a framework you're learning like `iced`, `axum`, `bevy`; patterns from a
project at work), in the same card format and with the same checks as `cards/`, but in
their own decks so the main deck stays general.

## Make a topic

Each topic is a deck folder. Copy the example without the leading underscore:

```bash
cp -r additional_cards/_example additional_cards/iced
```

Then edit `additional_cards/iced/deck.yaml` (deck name, id prefix) and the two card files:

| File | Use for | `asl check` |
|---|---|---|
| `<topic>.yaml` | std-only code | compiled, `clippy -D warnings`, `tests:` run |
| `<topic>_ext.yaml` (`check: false` in deck.yaml) | external crates, code fragments | skipped |

Both files study together in one deck if you set `subdecks: false` in deck.yaml.

```bash
asl fix   additional_cards/iced
asl lint  -q additional_cards/iced
asl check additional_cards/iced
asl build additional_cards/iced -o output/Iced.apkg
```

## Privacy

Everything in `additional_cards/` except `_example/` and this README is gitignored, so
project code you write cards about never ends up in a commit.

## Cards that follow a real project

If the cards come from a project you're working on, agentic-studying-loop's `asl init`
sets that up properly: the deck lives in your notes vault next to your study notes, an AI
agent writes the cards from your confirmed code, and `asl lint` checks them against the repo.
