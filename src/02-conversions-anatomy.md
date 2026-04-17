# Conversions and Anatomy

## Your first conversion

Sox infers format from file extension. Converting is often just:

```bash
sox test.wav test.mp3
sox test.wav test.flac
sox test.wav test.ogg
```

Use `soxi` to verify the output matches your expectations.

The null output `-n` discards the result entirely — useful for
checking that sox can read a file without writing anything:

```bash
sox test.wav -n
```

## The anatomy of a sox command

Every sox command follows this structure:

```text
sox  [global opts]  [input opts]  infile(s)  [output opts]  outfile  [effects...]
     ────────────   ──────────────────────   ────────────────────    ──────────
     globals        input                    output                  effects
```

- **globals** — options affecting the whole run (`-V`, `--buffer`, ...)
- **input** — format options for the input(s), placed *immediately before* the filename
- **output** — the output file, with its own optional format options before it
- **effects** — the effects chain, applied left to right

The `-v` flag from chapter 1 lives in the input section: it scales the
input amplitude as the file is read, before any effects run. The `vol`
effect (chapter 3) does the same arithmetic but in the effects chain.
These two commands produce identical output:

```bash
sox -v 0.5 test.wav out.wav   # scale at input
sox test.wav out.wav vol 0.5  # scale in effects chain
```

`-v` is input-only — sox will reject it as an output flag. To scale the
output, use `vol` or `gain` in the effects chain.

**`play` and `rec`** are just sox with one section missing. `play` has
no output section (the speaker is implicit). `rec` has no input section
(the microphone is implicit). Any effect chain you'd write after the
output filename in `sox` comes directly after the input in `play`:

```bash
sox  test.wav out.wav highpass 300 norm -3
play test.wav            highpass 300 norm -3
```

### Format flags are positional

A format flag describes the *next* filename in the command — input
or output, depending on where you place it:

```bash
sox -r 8000 test.wav out.wav   # override input's declared rate; output inherits 8000 Hz
sox test.wav -r 8000 out.wav   # resample output to 8000 Hz; input rate unchanged
sox -r 16000 test.wav -r 8000 out.wav  # both specified explicitly
```

All three are valid and mean different things. Placing a flag in the
wrong section will silently produce a different result than you intended,
which is the most common source of bugs in sox commands. Format
options are covered fully in chapter 5.

### Effects come last

Effects go *after* the output filename. This surprises most people
once and never again:

```bash
sox test.wav out.wav trim 5 10 reverse
#                         ──────────────── effects
play out.wav
```

Multiple effects are applied left to right: first `trim`, then
`reverse` on the trimmed result.
