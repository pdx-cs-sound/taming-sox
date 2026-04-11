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
     Zone 1         Zone 2                   Zone 3                  Zone 4
```

- **Zone 1** — global options affecting the whole run (`-V`, `--buffer`, ...)
- **Zone 2** — format options for the input(s), placed *immediately before* the filename
- **Zone 3** — the output file, with its own optional format options before it
- **Zone 4** — the effects chain, applied left to right

The `-v` flag from chapter 1 is a Zone 2 option: it scales the input
amplitude as the file is read, before any effects run. The `vol`
effect (chapter 3) does the same arithmetic but in Zone 4. These two
commands produce identical output:

```bash
sox -v 0.5 test.wav out.wav   # scale at input (Zone 2)
sox test.wav out.wav vol 0.5  # scale in effects chain (Zone 4)
```

`-v` is input-only — sox will reject it in Zone 3. To scale the
output, use `vol` or `gain` in the effects chain.

**`play` and `rec`** are just sox with one zone missing. `play` has
no Zone 3 (the speaker is implicit). `rec` has no Zone 2 (the
microphone is implicit). Any effect chain you'd write after the
output filename in `sox` comes directly after the input in `play`:

```bash
sox  input.wav output.wav highpass 300 norm -3
play input.wav            highpass 300 norm -3
```

### Format flags are positional

A format flag describes the *next* filename in the command — input
or output, depending on where you place it:

```bash
sox -r 8000 input.wav output.wav   # input is 8000 Hz; output rate unchanged
sox input.wav -r 8000 output.wav   # output is resampled to 8000 Hz; input rate unchanged
sox -r 16000 input.wav -r 8000 output.wav  # both specified explicitly
```

All three are valid and mean different things. Placing a flag in the
wrong zone will silently produce a different result than you intended,
which is the most common source of bugs in sox commands. Format
options are covered fully in chapter 5.

### Zone 4: effects come last

Effects go *after* the output filename. This surprises most people
once and never again:

```bash
sox input.wav output.wav trim 5 10 reverse
#                         ──────────────── Zone 4
play output.wav
```

Multiple effects are applied left to right: first `trim`, then
`reverse` on the trimmed result.
