# Release process

```bash
asl fix   cards/core cards/neetcode
asl lint  -q --skip size cards/core cards/neetcode
asl check cards/core cards/neetcode              # clippy clean + all tests pass
asl build cards/core cards/neetcode -o output/CodeCards.apkg
```

The package contains the cards, the deck hierarchy, the NeetCode new-card order
(`01`–`18` subdecks, authored easy→hard within a topic) and both deck-options presets
from `cards/*/deck.yaml` (`Rust Language Kata Core`: 14/day, random; `Rust Language
Kata NeetCode`: 1/day, in order). Anki applies the presets when the importer ticks
**Import any deck presets**; otherwise people set them once by hand (README,
"Recommended deck settings").

Verify in a fresh Anki profile before publishing: Deck Options on
`Rust Language Kata::Core` / `::Neetcode` show the named presets, and studying
`::Neetcode` starts with an Arrays & Hashing card.

## Studying

Study **`Rust Language Kata::Core`** and **`::Neetcode`** as two daily sessions → 14
random core cards + 1 NeetCode card in fixed order. Sibling subdecks share their
parent's daily cap, which is what keeps those totals exact.
