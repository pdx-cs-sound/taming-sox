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

## Combining them

`tempo` and `pitch` are independent effects applied in sequence:

```bash
play test.wav tempo 1.2 pitch -400   # faster but lower
```

## See also: Rubber Band

Sox has no phase vocoder. When quality matters — especially for
time-stretching, pitch-shifting, or formant-preserved vocal shifts —
[`rubberband`](https://breakfastquay.com/rubberband/) is the standard
tool. Further Reading covers how to reach for it.
