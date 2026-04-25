# Getting Started

## Check your install

```bash
sox --version
```

You should see a version line. If it starts with `SoX_ng`, you have
the maintained fork; if it says `SoX 14.4.2`, you have the 2015
legacy release. The book works on both — a few sox_ng-only features
are flagged where they come up.

## Inspecting files with soxi

`soxi` reads metadata without touching the audio. The book ships
with a short voice recording you can try it on:

<audio controls src="samples/voice.wav"></audio>
<a href="samples/voice.wav" download>⬇ voice.wav</a> (CC0)

```bash
soxi voice.wav
```

```text
Input File     : 'voice.wav'
Channels       : 1
Sample Rate    : 48000
Precision      : 16-bit
Duration       : 00:00:04.09 = 196162 samples ~ 306.503 CDDA sectors
File Size      : 392k
Bit Rate       : 768k
Sample Encoding: 16-bit Signed Integer PCM
```

Useful individual fields (handy in shell scripts):

```bash
soxi -r voice.wav    # sample rate
soxi -b voice.wav    # bit depth
soxi -c voice.wav    # channels
soxi -D voice.wav    # duration in seconds
```

## A test tone

When you want predictable audio to experiment with, generate it:

```bash
sox -n test.wav synth 10 sine 440 gain -6
play test.wav
```

Three new pieces, one sentence each: `-n` in the input position
means "no input file — generate audio instead." `synth 10 sine 440`
synthesizes ten seconds of a 440 Hz sine wave. `gain -6` knocks it
down 6 dB (roughly half amplitude), which leaves headroom so later
effects don't clip. [Chapter 11](11-synthesis.md) goes deeper on
`synth`; this is all you need for now.

## Playing audio with play

```bash
play test.wav
```

`play` is sox with your speaker as the implicit output. It is
literally a symlink to the same binary. It needs a working audio
device — on headless servers, use `sox ... -n` with `stat` or
`soxi` to verify results instead.

Scale the playback amplitude with `-v` (`1.0` = unchanged,
`0.5` = half amplitude). Despite the name, `-v` operates on amplitude,
which is linear — halving the amplitude reduces perceived loudness by
6 dB, not by half. Use `gain` ([chapter 3](03-basic-effects.md)) if
you want to think in decibels:

```bash
play -v 0.5 test.wav
```

Play only the first half-second:

```bash
play test.wav trim 0 0.5
```

That `trim 0 0.5` at the end is an *effect*. Don't worry about the
syntax yet — [chapter 2](02-conversions-anatomy.md) will make it click.

## Recording with rec

`rec` is the mirror image: sox with your microphone as the implicit
input.

```bash
rec capture.wav              # record until Ctrl-C
rec capture.wav trim 0 5     # record for 5 seconds
```
