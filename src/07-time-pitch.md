# Time and Pitch

Four effects; two axes:

| Effect | Changes speed? | Changes pitch? | Notes |
| --- | :---: | :---: | --- |
| `rate` | no | no | proper resampler; changes sample rate only |
| `speed` | yes | yes | varispeed tape |
| `tempo` | yes | no | time-stretch, pitch preserved |
| `pitch` | no | yes | pitch-shift, duration preserved |

## rate — resampling

Resamples the audio to a new sample rate. Pitch and duration are
both preserved — the output just has fewer (or more) samples per
second. Use it to change the technical format of a file, not to
alter how it sounds:

```bash
sox test.wav out.wav rate 22050    # downsample to 22050 Hz
play out.wav
sox test.wav out.wav rate 48000    # upsample to 48000 Hz
play out.wav
```

This is equivalent to writing `-r 22050 out.wav` as an output format
flag, but as an explicit effect it fits naturally in a chain and
gives access to quality options:

- `-h` — high quality: longer anti-aliasing filter, better stopband
  rejection, audibly cleaner on music
- `-v` — very high quality: even longer filter; diminishing returns
  over `-h` but useful for archival or repeated resampling where
  rounding errors accumulate

## speed — varispeed

Like a tape running faster or slower. Factor > 1 speeds up and
raises pitch; < 1 slows down and lowers pitch.

```bash
play test.wav speed 1.5    # faster and higher
play test.wav speed 0.75   # slower and lower
```

## tempo — time-stretch only

Changes duration while preserving pitch using the WSOLA algorithm
(chops audio into overlapping segments and re-stitches them).
Practical range: 0.5–2.0.

```bash
play test.wav tempo 1.2    # 20% faster, same pitch
play test.wav tempo 0.8    # 20% slower, same pitch
```

Three presets tune the algorithm for different material:

```bash
play test.wav tempo -m 1.2   # music (default)
play test.wav tempo -s 0.75  # speech
play test.wav tempo -l 1.1   # linear (least CPU, more artifacts)
```

## pitch — pitch-shift only

Argument is in *cents* (100 cents = 1 semitone, 1200 = one octave).

```bash
play test.wav pitch 200     # up 2 semitones
play test.wav pitch -1200   # down one octave
```

`pitch` uses the same WSOLA algorithm as `tempo` — it is implemented
as a `tempo` stretch followed by a `rate` resample in the opposite
direction, so the duration cancels out and only the pitch shift
remains. The `-m/-s/-l` presets are not exposed on `pitch`, but you
can pass the same `segment search overlap` tuning parameters if needed.

## stretch — OLA (occasionally useful)

Sox also has `stretch`, which uses basic Overlap-Add rather than
WSOLA. OLA chops audio into fixed-position windows and crossfades
them; WSOLA adds a cross-correlation search to find where waveforms
align before overlapping, avoiding phase cancellation artifacts.
`stretch` is faster and can occasionally outperform `tempo` for
factors very close to 1.0, where the fixed-position error is small
enough not to matter. For anything else, prefer `tempo`.

```bash
play test.wav stretch 1.2   # time-stretch by factor (>1 = longer)
```

Note that `stretch`'s factor is the opposite sense to `tempo`: `1.2`
means 20% longer, where `tempo 1.2` means 20% faster.

## Combining them

`tempo` and `pitch` are independent effects applied in sequence:

```bash
play test.wav tempo 1.2 pitch -400   # faster but lower
```

## See also: Rubber Band

Sox has no phase vocoder implementation. For higher-quality
time-stretching, pitch-shifting, or near-unity resampling (where
sox's anti-aliasing filter does more damage than the rate change
warrants) — `rubberband` is the standard tool
(see the [Rubber Band website](https://breakfastquay.com/rubberband/) for installation).

```bash
rubberband --tempo 1.2 input.wav output.wav   # 20% faster (same sense as sox tempo)
rubberband --time 0.8 input.wav output.wav    # 0.8x duration (--time is 1/--tempo)
rubberband --pitch 2 input.wav output.wav     # up 2 semitones (not cents)
rubberband --pitch -2 --tempo 1.1 input.wav output.wav  # combine freely
```

Rubberband has two engines: R2 (default, fast, WSOLA-based) and R3
(slower, phase vocoder, noticeably better on music):

```bash
rubberband --fine --pitch 4 input.wav output.wav   # R3 engine
rubberband-r3 --pitch 4 input.wav output.wav       # equivalent
```

For vocal pitch-shifting, `--formant` preserves the formant
structure so voices don't sound cartoonish:

```bash
rubberband --fine --formant --pitch 3 voice.wav output.wav
```

Rubberband does not support stdout, so combine with sox via a temp
file for format conversion:

```bash
rubberband -q --pitch 2 input.wav tmp.wav && sox tmp.wav output.flac
```
