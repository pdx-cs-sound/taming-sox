# Authoring notes

## Permalinks and cross-links

The book is published on GitHub Pages, so chapter URLs are
external-link surface. Two rules to keep them stable:

1. **Whenever a chapter file is renamed, split, or renumbered**,
   add an entry to `[output.html.redirect]` in `book.toml` mapping
   the old path to the new one. mdbook generates a redirect HTML
   page at the old URL. Keep old entries even after several
   reorgs — they cost almost nothing.
2. **Cross-references between chapters use mdbook links**, not
   bare prose: write `[chapter 5](05-formats.md)`, not
   "chapter 5". The link target survives renames automatically;
   on a renumber, both the visible number and the file path
   update together via grep.

Audit cross-references after any structural change with
`grep -rn 'chapter [0-9]' src/` — every match should be inside an
mdbook link.

## Version numbering and tags

The book carries a single line near the top of `src/preface.md`:

    Version X.Y — YYYY-MM-DD.

Both fields are hand-maintained; there is no build-time injection.

Bump rules:

- The version number tracks the existing `vX.Y` git tag sequence.
  The next release after `v0.4` is `v0.5`, then `v0.6`, and so on
  — increment by one, do not skip.
- `X.Y` has no patch component. Small fixes between releases
  don't get a new version; they roll into the next bump.
- The date is the calendar date of the release.

Tagging rules:

- Tags are **annotated** (`git tag -a vX.Y -m "..."`), not
  lightweight. Annotated tags carry an author, date, and message
  and are the right shape for a release marker.
- The message is a single line summarizing what changed since the
  previous tag — readable from `git tag -n` and `git log
  --decorate`. Keep it to one line; longer notes live in the
  commit log.

Bump and tag together in a single commit titled along the lines
of `bumped to version X.Y` so `git log` makes the release point
easy to find.
