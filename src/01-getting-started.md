# Getting Started

## Test tones

We need audio to work with. This command generates it:

```bash
sox -n test.wav synth 3 sine 440
```

That produces a 3-second 440 Hz sine wave. We'll explain `synth` and
`-n` fully in chapter 10; for now treat it as a recipe. Each chapter
will tell you which test files to generate.

## Inspecting files with soxi

`soxi` reads metadata without touching the audio:

```bash
soxi test.wav
```

```
Input File     : 'test.wav'
Channels       : 1
Sample Rate    : 48000
Precision      : 32-bit
Duration       : 00:00:03.00 = 144000 samples ~ 225 CDDA sectors
File Size      : 576k
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
literally a symlink to the same binary.

Adjust playback volume with `-v` (a number, not decibels):

```bash
play -v 0.5 test.wav
```

Play only the first two seconds:

```bash
play test.wav trim 0 2
```

That `trim 0 2` at the end is an *effect*. Don't worry about the
syntax yet — chapter 2 will make it click.

## Recording with rec

`rec` is the mirror image: sox with your microphone as the implicit
input.

```bash
rec capture.wav              # record until Ctrl-C
rec capture.wav trim 0 5     # record for 5 seconds
```
