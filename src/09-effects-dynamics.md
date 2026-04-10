# Effects and Dynamics

**Setup:**
```bash
# Harmonically rich source for reverb, echo, chorus, flanger
sox -n source.wav synth 5 sawtooth 220 gain -6

# Varying dynamics for compand: loud / quiet / loud
sox -n _loud.wav synth 2 sawtooth 220 gain -6
sox -n _quiet.wav synth 2 sawtooth 220 gain -20
sox _loud.wav _quiet.wav _loud.wav dynamics.wav
```

A sine wave at a single frequency reveals little about spatial or
modulation effects. Sawtooth waves have harmonics across the whole
spectrum, making reverb, echo, chorus and flanger all clearly audible.

## reverb

Simulates room acoustics. Arguments: reverberance (0–100),
HF damping (0–100), room scale (0–100). Defaults are reasonable.

```bash
sox source.wav out.wav reverb
sox source.wav out.wav reverb 80 50 100    # large, bright room
```

`--wet-only` removes the dry signal, leaving only the wet (reverberated) signal:

```bash
sox source.wav out.wav reverb --wet-only 80
```

> **Note:** `reverb` does not extend the output file. The reverb
> decay is truncated at the input length. To capture the full tail,
> pad silence onto the end of the input first:
>
> ```bash
> sox source.wav out.wav pad 0 2 reverb 80
> ```

## echo

Discrete repeating delays. Arguments: `gain-in gain-out`, then one
or more `delay(ms) decay` pairs.

```bash
sox source.wav out.wav echo 0.8 0.7 500 0.4
#                            ──── ────  ─────── ────
#                            in  out   500ms   0.4 decay
```

Two taps:

```bash
sox source.wav out.wav echo 0.8 0.7 500 0.4 700 0.3
```

## chorus and flanger

```bash
sox source.wav out.wav chorus 0.6 0.9 55 0.4 0.25 2 -s
sox source.wav out.wav flanger
```

Both have complex parameter lists — the defaults are a reasonable
starting point; see `man sox` for tuning.

## silence — trim silence

These effects need a file that actually has silence. Generate one
with `pad`, which adds silence (in seconds) to the start and end:

```bash
sox -n padded.wav synth 5 sawtooth 220 gain -6 pad 1 1
```

Remove leading and trailing silence:

```bash
sox padded.wav out.wav silence 1 0.1 1% -1 0.1 1%
```

Each group is: `periods duration threshold`. The first group handles
the start; the second (preceded by `-1`) handles the end.

For voice recordings, `vad` (voice activity detection) is simpler —
it finds the onset of audio activity and trims everything before it:

```bash
sox padded.wav out.wav vad
```

## compand — dynamic range compression

`compand` reduces the gap between loud and quiet passages.
`dynamics.wav` from the setup has 14 dB of range to work with.

```bash
sox dynamics.wav out.wav compand 0.3,1 6:-70,-60,-20 -5 -90 0.2
```

Breaking that down:
- `0.3,1` — attack 0.3 s, decay 1 s
- `6:-70,-60,-20` — transfer function: input/output dB pairs
- `-5` — output gain offset
- `-90` — initial signal level
- `0.2` — delay before processing

A practical podcast leveling chain:

```bash
sox dynamics.wav podcast.wav \
    highpass 80 \
    compand 0.3,1 6:-70,-60,-20 -5 -90 0.2 \
    norm -3
```
