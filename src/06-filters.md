# Filters

Filters shape the frequency content of audio. A quick reference:
human hearing spans roughly 20 Hz (low rumble) to 20 kHz (high hiss).

Filtering a single sine wave is uninteresting — it either passes or
it doesn't. Pink noise has energy across the whole spectrum, so
filters produce an audible and visible change. Generate some:

```bash
sox -n noise.wav synth 5 pinknoise gain -6
play noise.wav
```

## highpass and lowpass

Remove everything below or above a cutoff frequency:

```bash
play noise.wav highpass 2000    # remove everything below 2 kHz
play noise.wav lowpass 2000     # remove everything above 2 kHz
play noise.wav highpass 300 lowpass 3400   # telephone band
```

The telephone band example is a good one to listen to: the
characteristic "tinny phone" sound comes entirely from cutting the
low and high ends.

## bass and treble

Shelving filters: boost or cut below/above a crossover point.
Argument is in dB.

```bash
play noise.wav bass 3      # boost bass by 3 dB
play noise.wav treble -6   # cut treble by 6 dB
play noise.wav bass 2 treble -2
```

## equalizer — parametric EQ

Three arguments: center frequency, width, gain in dB. Width units
are controlled by a suffix:

| Suffix | Unit | Example |
|--------|------|---------|
| none | Hz | `200` = 200 Hz wide |
| `q` | Q factor | `2q` = Q of 2 |
| `o` | octaves | `1o` = one octave wide |

Q and Hz are inversely related: a higher Q means a narrower band.
`Q = center / bandwidth`, so `2q` at 1 kHz equals a 500 Hz bandwidth.
Q is more useful when you want consistent relative width across
different center frequencies.

Stack multiple `equalizer` effects to build a full EQ:

```bash
play noise.wav equalizer 1000 200 -6    # cut 6 dB at 1 kHz, 200 Hz wide
play noise.wav equalizer 1000 2q -6     # same centre, Q=2 (500 Hz wide)
play noise.wav equalizer 3000 1o 3      # boost 3 dB at 3 kHz, one octave wide
```

## A practical voice cleanup chain

```bash
sox raw_voice.wav clean.wav \
    highpass 100 \
    equalizer 3000 500 2 \
    norm -3
play clean.wav
```

Removes low-frequency noise, adds a little presence, normalizes.
