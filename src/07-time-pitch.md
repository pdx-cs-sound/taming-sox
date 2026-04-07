# Time and Pitch

**Setup:**
```bash
sox -n source.wav synth 5 sine 440 gain -6
```

Four effects; two axes:

| Effect | Changes speed? | Changes pitch? | Notes |
|--------|:--------------:|:--------------:|-------|
| `rate` | yes | yes | simple resampling |
| `speed` | yes | yes | varispeed tape |
| `tempo` | yes | no | time-stretch, pitch preserved |
| `pitch` | no | yes | pitch-shift, duration preserved |

## rate — the blunt instrument

Changes the declared sample rate, which changes both speed and pitch:

```bash
sox source.wav out.wav rate 22050    # half speed, half pitch
```

## speed — varispeed

Like a tape running faster or slower. Factor > 1 speeds up and
raises pitch; < 1 slows down and lowers pitch.

```bash
sox source.wav out.wav speed 1.5    # faster and higher
sox source.wav out.wav speed 0.75   # slower and lower
```

## tempo — time-stretch only

Changes duration while preserving pitch. Uses the WSOLA algorithm.
Practical range: 0.5–2.0.

```bash
sox source.wav out.wav tempo 1.2    # 20% faster, same pitch
sox source.wav out.wav tempo 0.8    # 20% slower, same pitch
```

For speech, add `-s` for better quality:

```bash
sox lecture.wav slow.wav tempo -s 0.75
```

## pitch — pitch-shift only

Argument is in *cents* (100 cents = 1 semitone, 1200 = one octave).
Uses a phase vocoder; computationally expensive.

```bash
sox source.wav out.wav pitch 200     # up 2 semitones
sox source.wav out.wav pitch -1200   # down one octave
```

## Combining them

`tempo` and `pitch` are independent, so you can combine freely:

```bash
sox source.wav out.wav tempo 1.2 pitch -400   # faster but lower
```
