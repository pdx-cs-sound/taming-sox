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

**What you need:** sox installed — see the
[SoX documentation](https://sox.sourceforge.net/) for your platform.
Sample audio files are provided; test tones are generated as we go.
