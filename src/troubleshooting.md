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
fuzzy crunch that tracks peaks rather than being continuous. The
`WARN ... clipped N samples` message on stderr is sox telling you
the same thing.

### Diagnosing where it happened

The warning by itself doesn't say *which* effect clipped. Re-run
with `-V3` and sox prints per-effect statistics, including clip
counts attributed to each effect in the chain:

```bash
sox -V3 in.wav out.wav highpass 100 gain 6 norm 2>&1 | grep -i clip
```

If one effect shows a non-zero clip count, that's your culprit. If
the count appears only on the output writer, the chain itself is
fine — you're just exceeding the output format's range and the
fix is at the end (lower `norm` target, or float output).

When `-V3` output is too noisy, bisect: remove effects from the
end of the chain one at a time and re-run, until the warning
disappears. The last effect you removed is the one pushing the
signal over.

### Common causes and fixes

- `gain N` after `norm`: `norm` lifts the peak to 0 dBFS, then
  `gain` pushes above it. Reorder, or use `norm -N`.
- Mixing without headroom: `-m` sums inputs, so two full-scale
  signals clip immediately. Either `-v 0.5` each input or `norm -3`
  the result.
- Upsampling a signal that was already at 0 dBFS — the
  interpolator's ringing can exceed the original peak. Insert
  `gain -3` before `rate`, or `norm -3` after.
- A bounded format in the middle of a sox-to-sox pipe. Switch the
  pipe to `-p` (sox's native int32) — see chapter 6.
- Aggressive boosts hitting the int32 ceiling internally (chapter
  2). Rare in normal use; if you see it, lower input level with
  `-v 0.5` on the input side rather than chasing it later.

Two useful prophylactics:

- `gain -l N` applies `N` dB of gain through a simple limiter
  instead of as straight amplification — it boosts without ever
  clipping. Best for small-to-moderate boosts; aggressive limiting
  audibly distorts.
- The global `-G` flag (`sox -G in.wav out.wav ...`) automatically
  inserts `gain -h` / `gain -r` pairs around the chain. The
  attenuation is computed analytically, not by scanning the audio:
  effects that know their worst-case gain (`rate`, `reverb`, the
  biquad filters, `remix`, `dither`, ...) declare it, and `gain -h`
  multiplies those together and attenuates by the inverse upfront,
  with `gain -r` reclaiming any unused headroom at the end. This
  is the right tool when filters or resampling might overshoot,
  but it does *not* protect against `gain +N`, `vol`, or `norm` —
  those don't participate in the protocol. Use `gain -l` for those.

### Detecting clipping after the fact

If the WARN is gone but you still hear distortion, check the
output with `stats`:

```bash
sox output.wav -n stats
```

Watch the `Pk lev dB` line and the `Flat factor` / `Num samples`
report for saturated counts. A non-zero `Flat factor` on output
that shouldn't have any flat runs is a strong signal.

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
