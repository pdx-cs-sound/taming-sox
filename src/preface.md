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

**What you need:** sox installed — see the
[SoX documentation](https://sox.sourceforge.net/) for your platform.
Sample audio files are provided; test tones are generated as we go.
