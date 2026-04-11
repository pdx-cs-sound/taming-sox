# Synthesis and Batch Processing

## synth — generating audio from nothing

`-n` in the input position means "no input file; generate audio."
`synth` tells sox what to generate.

```bash
play -n synth duration waveform frequency
```

### Waveforms

```bash
play -n synth 3 sine     440
play -n synth 3 square   440
play -n synth 3 triangle 440
play -n synth 3 sawtooth 440
```

### Noise

```bash
play -n synth 5 whitenoise
play -n synth 5 pinknoise
play -n synth 5 brownnoise
```

### Sweeps

Specify frequency as a range to sweep:

```bash
play -n synth 5 sine 100:8000    # 100 Hz → 8 kHz over 5s
```

### Chords

Multiple waveforms on one `synth` generate simultaneously:

```bash
# C major: C4, E4, G4
play -n synth 2 sine 261.63 sine 329.63 sine 392.00 gain -6
```

### Specifying output format

The output format follows your system's default audio configuration,
which may not be what you want. Specify it explicitly with format
flags before `-n`:

```bash
sox -n -r 44100 -b 16 -c 1 out.wav synth 3 sine 440
```

### Adding effects

`play -n synth` accepts a full effects chain:

```bash
play -n synth 10 sine 440 reverb 80
```

---

## Batch processing

### Process a directory

```bash
mkdir -p normalized
for f in *.wav; do
    sox "$f" "normalized/$f" norm -3
done
```

### Construct output filenames

```bash
for f in *.wav; do
    out="${f%.wav}_clean.wav"
    sox "$f" "$out" highpass 100 norm -3
done
```

`${f%.wav}` strips the `.wav` suffix.

### Batch format conversion

```bash
mkdir -p mp3
for f in *.wav; do
    sox "$f" "mp3/${f%.wav}.mp3"
done
```

### Use soxi in scripts

```bash
duration=$(soxi -D "$f")
if awk "BEGIN { exit !($duration > 5) }"; then
    sox "$f" trimmed.wav trim 0 5
fi
```

### Parallel processing

```bash
ls *.wav | xargs -P 4 -I{} sox {} "out/{}" norm -3
```

### Check exit codes

Sox exits non-zero on errors. Always check in scripts:

```bash
for f in *.wav; do
    sox "$f" "out/$f" norm -3 || echo "Failed: $f" >&2
done
```

### Piping between sox processes

The `-p` flag emits sox's internal format on stdout — no need to
specify sample rate, bit depth, or encoding on the receiving end:

```bash
sox input.wav -p trim 10 20 | sox - reverb 80 output.wav
```

This avoids intermediate files in multi-step pipelines.
