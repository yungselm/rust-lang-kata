## Pull Request Checklist

- [ ] `python lint_cards.py` passes (cards are self-contained, no cross-references)
- [ ] `python check_cards.py` passes (solutions compile, are clippy-clean, and pass their `tests:`)
- [ ] `python build.py` runs and I previewed the result (`preview.html` or importing the `.apkg` into Anki)
- [ ] New/changed cards keep total count in mind (~2000-card budget, see README)
- [ ] This PR is linked to an issue (if applicable): fixes #<issue-number>

### What changed
Which `cards/*.yaml` file(s), or which part of the build system/templates.

### Why this is useful
Brief motivation — e.g. gap in coverage, a wrong/unclear card, a rendering fix.

### Notes for reviewer
Any non-obvious points (e.g. a tricky clippy lint you had to work around).
