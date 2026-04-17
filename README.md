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

1. Getting Started — `sox --version`, `soxi`, `play`, `rec`, test tone recipe
2. Conversions and Anatomy — format detection, the globals/input/output/effects model
3. Basic Effects — `trim`, `reverse`, `fade`, `vol`, `gain`, `norm`
4. Chaining Effects — left-to-right pipelines, auditioning with `play`
5. Format Options — `-r`, `-b`, `-c`, `-e`, fully-specified output, raw PCM, piping
6. Filters — `highpass`, `lowpass`, `equalizer`
7. Time and Pitch — `rate`, `speed`, `tempo`, `pitch`
8. Combining Files — concatenation, mixing (`-m`), merging (`-M`), `remix`
9. Effects and Dynamics — `reverb`, `silence`, `vad`, `compand`
10. Synthesis — `synth`, waveforms, noise, sweeps, chords
11. Batch Processing — shell loops, parallel processing, piping
12. Troubleshooting — silent output, clipping, format mismatch, `-V` diagnostics
13. Beyond sox — man pages, LADSPA, ffmpeg, Rubber Band, libsox, limitations

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

## License

This work is licensed under
[Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You are free to share and adapt it for any purpose, provided you
give appropriate credit.
