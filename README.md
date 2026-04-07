# Taming sox

An mdbook tutorial for the `sox` command-line audio tool, covering
its unusual CLI in a progressive order that makes the quirks feel
inevitable rather than arbitrary.

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

1. Getting Started — `soxi`, `play`, `rec`, test tone recipe
2. Conversions and Anatomy — format detection, the 4-zone command model
3. Basic Effects — `trim`, `reverse`, `fade`, `vol`, `gain`, `norm`
4. Chaining Effects — left-to-right pipelines, auditioning with `play`
5. Format Options — `-r`, `-b`, `-c`, `-e`, raw PCM, piping
6. Filters — `highpass`, `lowpass`, `bass`, `treble`, `equalizer`
7. Time and Pitch — `speed`, `tempo`, `pitch`, `rate`
8. Combining Files — concatenation, mixing (`-m`), merging (`-M`), `remix`
9. Effects and Dynamics — `reverb`, `echo`, `silence`, `compand`
10. Synthesis and Batch Processing — `synth`, shell loops, parallel processing

## Prerequisites

```bash
apt install sox libsox-fmt-all   # Debian/Ubuntu
brew install sox                 # macOS
```

mdbook: <https://rust-lang.github.io/mdBook/guide/installation.html>
