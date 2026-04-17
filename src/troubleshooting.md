# Troubleshooting

Most sox problems fall into a small set of patterns. Each one has a
quick diagnostic.

## Silent output

The file exists, `soxi` shows sensible numbers, and you hear nothing.
Likely causes, in order:

- Audio device: another app has the output, or `play` is pointed at
  the wrong sink. Try `play` on a known-good file first
  (`play -n synth 1 sine 440`). If *that* is silent, it's not a sox
  problem.
- `-v` in the wrong section: `sox -v 0 input.wav out.wav` scales the
  input to zero, producing a silent file — no error. Check that `-v`
  belongs where you put it (see chapter 2).
- System volume muted at the OS level — check that independently.

## Clipping

Clipping sounds like harsh distortion on loud passages — a kind of
fuzzy crunch that tracks peaks rather than being continuous. Common
causes:

- `gain N` after `norm`: `norm` lifts the peak to 0 dBFS, then `gain`
  pushes above it. Reorder, or `norm -N` instead.
- Mixing without headroom: `-m` sums inputs, so two full-scale
  signals clip immediately. Either `-v 0.5` each input or `norm -3`
  the result.
- Upsampling a signal that was already at 0 dBFS — the interpolator's
  ringing can exceed the original peak.

Detect clipping with `stats`:

```bash
sox output.wav -n stats
```

Watch the `Pk lev dB` line and the `Flat factor` / `Num samples`
report for saturated counts. A non-zero `Flat factor` on output that
shouldn't have any flat runs is a strong signal.

## Format mismatch on concat or mix

Sox hard-fails when inputs to concatenation or `-m` mixing differ in
sample rate or channel count:

```text
sox FAIL sox: Input files must have the same sample-rate
```

Fix by pre-processing the outlier:

```bash
sox other.wav -r 44100 other-44k.wav      # match the rate
sox mono.wav -c 2 mono-stereo.wav         # match channels
sox main.wav other-44k.wav combined.wav   # now concat works
```

Or do it in a single pipeline with `-p`:

```bash
sox other.wav -p rate 44100 channels 2 | sox main.wav - combined.wav
```

## `play` fails on headless systems

`play` needs a working audio device. On servers, CI, and containers,
it typically can't find one and errors out. Diagnose a chain without
actually playing:

```bash
# Write to /dev/null-style null output and read stats
sox input.wav -n stats

# Or render to a temp file and inspect with soxi
sox input.wav out.wav <effects>
soxi out.wav
```

`-n` as the output lets effects run through to `stat`/`stats`
without needing a device.

## Typos that silently mean something else

Effect names in sox aren't validated against a "did you mean" list;
a misspelling is often a valid effect that does something completely
different. `bass` and `bas` both parse; one of them isn't the
shelving filter. Similarly, format flags put in the wrong section
apply to the wrong file without a warning.

The defense: eyeball the command before running, and use `-V3` to
see what sox actually thinks it's doing.

## Use -V for diagnostics

Sox takes a verbosity level from `-V1` (errors only) up through
`-V4` (everything it knows). `-V3` is the usual sweet spot — it
prints the effect chain as sox understands it, including which
effects actually ran and with what arguments:

```bash
sox -V3 input.wav out.wav highpass 100 norm -3
```

If an effect isn't doing what you expected, `-V3` usually tells you
why in the first few lines.

## Reading sox error messages

Most sox errors are in the form `sox FAIL <subsystem>: <message>`.
A few common ones:

- `sox FAIL formats: no handler for file extension ...` — you asked
  sox to read or write a format without a `-t` flag, and the
  extension didn't disambiguate. Add `-t wav` (or whatever).
- `sox FAIL sox: Input files must have the same sample-rate` —
  see the format-mismatch section above.
- `sox FAIL rate: Input sample-rate ... is unchanged` — you asked
  `rate` to resample to the rate it's already at. Remove the effect.
- `sox WARN ...: clipped N samples; ...` — output clipped; see the
  clipping section above.

When in doubt, re-run with `-V3` — the warning is usually right next
to the line that caused it.
