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
