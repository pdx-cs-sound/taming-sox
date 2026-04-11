# Getting Started

## Test tones

We need audio to work with. This command generates it:

```bash
sox -n test.wav synth 10 sine 440 gain -6
play test.wav
```

That produces a 10-second 440 Hz sine wave at −6 dB (half amplitude),
which leaves headroom for effects that add energy. We'll explain `synth` and `-n` fully in chapter 10;
for now treat it as a recipe.

## Inspecting files with soxi

`soxi` reads metadata without touching the audio:

```bash
soxi test.wav
```

```text
Input File     : 'test.wav'
Channels       : 1
Sample Rate    : 48000
Precision      : 32-bit
Duration       : 00:00:10.00 = 480000 samples ~ 750 CDDA sectors
File Size      : 1.92M
Bit Rate       : 1.54M
Sample Encoding: 32-bit Signed Integer PCM
```

The exact values depend on your system's default audio configuration.

Useful individual fields:

```bash
soxi -r test.wav    # sample rate
soxi -b test.wav    # bit depth
soxi -c test.wav    # channels
soxi -D test.wav    # duration in seconds (good for scripts)
```

## Playing audio with play

```bash
play test.wav
```

`play` is sox with your speaker as the implicit output. It is
literally a symlink to the same binary. It requires a working audio
device — on headless servers, use `sox ... -n` with `stat` or
`soxi` to verify results instead.

Scale the playback amplitude with `-v` (`1.0` = unchanged, `0.5` = half
amplitude). Despite the name suggesting volume, `-v` operates on amplitude, which is a
linear scale — halving the amplitude reduces perceived loudness by 6 dB,
not by half. Use `gain` (chapter 3) if you want to think in decibels:

```bash
play -v 0.5 test.wav
```

Play only the first half-second:

```bash
play test.wav trim 0 0.5
```

That `trim 0 0.5` at the end is an *effect*. Don't worry about the
syntax yet — chapter 2 will make it click.

## Recording with rec

`rec` is the mirror image: sox with your microphone as the implicit
input.

```bash
rec capture.wav              # record until Ctrl-C
rec capture.wav trim 0 5     # record for 5 seconds
```
