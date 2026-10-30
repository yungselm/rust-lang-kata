## Pull Request Checklist

- [ ] `asl fix` ran (new cards got ids) and `asl lint -q --skip size cards/core cards/neetcode` passes
- [ ] `asl check cards/core cards/neetcode` passes (solutions compile, are clippy-clean, and pass their `tests:`)
- [ ] `asl build cards/core cards/neetcode` runs and I checked the result in Anki
- [ ] New/changed cards keep total count in mind (~2000-card budget, see README)
- [ ] This PR is linked to an issue (if applicable): fixes #<issue-number>

### What changed
Which card file(s) in `cards/core/` or `cards/neetcode/`.

### Why this is useful
Brief motivation — e.g. gap in coverage, a wrong/unclear card, a rendering fix.

### Notes for reviewer
Any non-obvious points (e.g. a tricky clippy lint you had to work around).
