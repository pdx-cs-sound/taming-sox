# Taming sox

by Bart Massey and Claude Code

---

## Introduction

Sox is a command-line audio Swiss Army knife: it converts formats,
applies DSP effects, mixes files, generates tones, and slots cleanly
into shell pipelines. Its CLI is genuinely strange — effects come
*after* the output filename, format flags are positional, and a typo
can silently mean something completely different. This tutorial
introduces those quirks in an order that makes them feel inevitable
rather than arbitrary.

**What you need:** sox installed (`apt install sox libsox-fmt-all`
on Debian/Ubuntu; `brew install sox` on macOS). No audio files
required — we generate test tones as we go.
