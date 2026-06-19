# Release process

`python build.py` produces the cards, the deck hierarchy, and the NeetCode
card order. It also *embeds* the two deck-options presets, but **Anki's `.apkg`
importer ignores embedded presets** (by design it never lets a shared deck touch
your Default preset, and it doesn't read genanki's config). So presets have to be
stamped on with a **one-time round-trip through Anki**. Card/order updates don't
need the round-trip — only changes to the presets do.

## A. Build (every release)

```bash
python check_cards.py        # clippy clean + all tests pass
python build.py              # writes output/CodeCards.apkg
```

NeetCode subdecks are numbered `01`–`18` in topic order
(`Rust::Neetcode::01 Arrays Hashing` … `18 Bit Manipulation`), so they sort into
NeetCode order under any gather setting; within a topic, cards are in authored
easy→hard order.

## B. Stamp the presets (only when presets change)

Do this in Anki once; the result is the file you distribute.

1. Start from a **clean profile** (or delete any existing `Rust::*` decks first),
   import `output/CodeCards.apkg`, and enable **FSRS** (any Deck Options page → FSRS
   toggle; it's collection-wide).
2. Create preset **`Rust Core`** (Deck Options on `Rust::Core` → Add preset) and set:

   | Setting | Value |
   |---|---|
   | New cards/day | 14 |
   | Maximum reviews/day | 9999 |
   | Desired retention | 0.90 |
   | Learning / relearning steps | `1m 10m` / `10m` |
   | Display order → New card gather order | **Random notes** (Deck would show one subdeck at a time) |
   | Display order → New card sort order | Order gathered |
   | Leech threshold / action | 5 / Tag Only |
   | Maximum interval | 36500 |

   Then preset menu → **Save to all subdecks**.
3. Create preset **`Rust NeetCode`** from `Rust::Neetcode` with the **same values
   except** New cards/day **1**. NeetCode order is handled by the `01`–`18` subdeck
   prefixes, so the gather order can stay **Deck**. Save to all subdecks.
4. **File → Export → Anki Deck Package**. Select the **`Rust`** deck. Check
   **Include deck presets**. Uncheck **Include scheduling information** (so importers
   don't inherit your review history; the new-card order is preserved either way).
   Leave "Support older Anki versions" unchecked. Export to `output/CodeCards.apkg`.
5. **Verify**: import that file into a *fresh* profile and confirm Deck Options on
   `Rust::Core` / `Rust::Neetcode` show the named presets (not "Default"), and that
   studying `Rust::Neetcode` starts with a Contains-Duplicate / Arrays & Hashing card.
6. Commit the exported `output/CodeCards.apkg`.

Note: Anki's preset export/import has had bugs
(https://github.com/ankitects/anki/issues/3023), so step 5's verification matters.
Named (non-Default) presets like these are the ones that do travel.

## C. Studying

Study **`Rust::Core`** and **`Rust::Neetcode`** as two daily sessions → 14 random
core cards + 1 NeetCode card in fixed order. Sibling subdecks share their parent's
daily cap, which is what keeps those totals exact.
