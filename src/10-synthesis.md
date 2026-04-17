# Synthesis

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
which may not be what you want. Specify it explicitly with output
format flags between `-n` and the output filename (see "Fully-specified
output" in chapter 5):

```bash
sox -n -r 44100 -b 16 -c 1 out.wav synth 3 sine 440
```

### Adding effects

`play -n synth` accepts a full effects chain:

```bash
play -n synth 10 sine 440 reverb 80
```
