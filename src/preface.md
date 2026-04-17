# Taming sox

*Bart Massey and Claude Code*

Licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Introduction

Sox is a command-line audio Swiss Army knife: it converts formats,
applies DSP effects, mixes files, generates tones, and slots cleanly
into shell pipelines. Its CLI is genuinely strange — effects come
*after* the output filename, format flags are positional, and a typo
can silently mean something completely different. This tutorial
introduces those quirks in an order that makes them feel inevitable
rather than arbitrary.

The source for this book is available at
<https://github.com/pdx-cs-sound/taming-sox>.

**What this book covers.** Sox has many more effects than any one
tutorial can reasonably teach. The approach here: show the arguments
that teach concepts — the `q`/`t`/`h`/`l` shapes in `fade`, the
Q/Hz/octaves units in `equalizer`, the transfer-function syntax in
`compand`. For arguments that just tune existing behavior, the sox
man page is the right reference. When an effect is mentioned only in
passing, that's why.

Sox has real limits — they're collected in the last chapter if you
want to check whether it fits your problem before investing in
learning it.

Sample audio files are provided; test tones are generated as we go.

## Getting sox

Most modern distros ship `sox_ng` (the maintained fork) under the
name `sox`. Some older stable releases still ship the 2015 legacy
build. Homebrew and the BSDs vary.

Run `sox --version` to check. `SoX_ng` means you're set. `SoX 14.4.2`
means you have the legacy build — everything in this book still works,
but you'll miss the sox_ng-flagged features later, and you'll be
running an unmaintained binary.

If your platform doesn't ship sox_ng and you want it, build from
<https://codeberg.org/sox_ng/sox_ng>. Windows binaries are on the
releases page.
