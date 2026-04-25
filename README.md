# Taming sox

An mdbook tutorial for the `sox` command-line audio tool, covering
its unusual CLI in a progressive order that makes the quirks feel
inevitable rather than arbitrary.

The published book is at
<https://pdx-cs-sound.github.io/taming-sox/>.

## Reading it

```bash
mdbook serve
```

Then open <http://localhost:3000>.

## Building

```bash
mdbook build
```

Output goes to `book/`.

## Contents

See [SUMMARY.md](src/SUMMARY.md), or read the
[published book](https://pdx-cs-sound.github.io/taming-sox/).

## Prerequisites

```bash
apt -t unstable install sox libsox-fmt-all   # Debian (sox_ng lives in unstable)
brew install sox                             # macOS
```

On Ubuntu and older Debian stables, `apt install sox` gets you the
legacy 2015 build; the book still works, but a few sox_ng-only
features are flagged. See the introduction's "Getting sox" section
for how to check what you have and where to build sox_ng from
source.

mdbook: <https://rust-lang.github.io/mdBook/guide/installation.html>

## Authoring

Conventions for editing the book are in [AUTHORING.md](AUTHORING.md).

## License

This work is licensed under
[Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You are free to share and adapt it for any purpose, provided you
give appropriate credit.
