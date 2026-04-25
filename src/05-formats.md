# Audio Formats

This chapter is the reference: the flags sox uses to describe
audio, what each one means, and what sox infers when you leave
them off. [Chapter 6](06-format-conversions.md) follows up with
recipes — resampling, channel changes, raw PCM, piping — built on
this vocabulary.

Recall from [chapter 2](02-conversions-anatomy.md): format flags
describe the *next* filename.
Put them in the wrong section and they apply to the wrong file.

## Two kinds of format

An audio file has two independent layers, and sox has separate
flags for each:

- **Container (file format).** The wrapper: WAV, AIFF, FLAC, Ogg,
  MP3, raw, ... Specified with `-t`.
- **Sample format.** The properties of the audio inside: sample
  rate, bit depth, channel count, encoding. Specified with
  `-r`, `-b`, `-c`, `-e`.

Most user-facing containers (WAV, FLAC, AIFF, Ogg) carry the
sample format in a header, so sox can read it back. Raw PCM has no
header, so you must describe it completely on the command line.

## The four sample-format flags

| Flag | Meaning | Example |
| --- | --- | --- |
| `-r` | sample rate (Hz) | `-r 44100` |
| `-b` | bit depth | `-b 16` |
| `-c` | channels | `-c 1` (mono), `-c 2` (stereo) |
| `-e` | encoding | `-e signed-integer` |

`-e` selects the numeric representation of each sample:

| Encoding | Typical use |
| --- | --- |
| `signed-integer` | PCM in WAV (16-bit and up), AIFF, FLAC — the default for almost everything |
| `unsigned-integer` | 8-bit WAV (see below), some legacy raw formats |
| `floating-point` | 32- or 64-bit float WAV; sox's lossless intermediate |
| `a-law`, `u-law` | telephony (8-bit logarithmic, low bandwidth) |

A historical quirk worth knowing: in the WAV format, 8-bit PCM is
**unsigned** (samples 0–255, with silence at 128) while 16-bit and
wider PCM is **signed** (silence at 0). The asymmetry is baked
into the WAV spec, not a sox choice — sox just follows it. It
matters when you read or write 8-bit WAVs as raw, or when you
hand 8-bit data to a tool that assumes signed: getting the
signedness wrong shifts silence to full-scale and is loud.

## Endianness

For multi-byte sample encodings (16-bit and wider integers, and
floating point), the byte order matters. Sox has three flags:

| Flag | Meaning |
| --- | --- |
| `-L`, `--endian little` | little-endian |
| `-B`, `--endian big` | big-endian |
| `-x`, `--endian swap` | opposite of the host system |

Self-describing containers nail this down by spec — WAV is always
little-endian, AIFF always big-endian — and sox respects the
header. You only need to set endianness explicitly for **raw**
files (no header to read), and occasionally to override an
ambiguous or wrong header. 8-bit, a-law, and u-law are byte-sized,
so endianness doesn't apply.

```bash
sox -t raw -r 44100 -b 16 -c 2 -e signed-integer -B big.raw out.wav
```

## The container flag

`-t` names the container, *not* a property of the audio. Sox
normally infers it from the filename extension, so you rarely set
it. Reach for `-t` only when there's no extension to read (pipes
with `-`, headerless raw files) or the extension lies about the
content.

```bash
-t raw      # headerless PCM — must also give -r -b -c -e
-t wav      # force WAV regardless of extension
```

## What sox infers, and what it doesn't

For **inputs**:

- Extension → container.
- Container header → sample format (rate, depth, channels,
  encoding) for self-describing formats. WAV, FLAC, AIFF, Ogg,
  MP3 all work this way.
- Raw input has no header, so sox infers nothing. You must give
  `-r -b -c -e` (and `-t raw` if the extension doesn't say so,
  plus `-L`/`-B` for multi-byte encodings).

For **outputs**:

- Extension → container.
- If there's a real input file, its sample format propagates to
  the output unless you override with `-r`, `-b`, `-c`, or `-e`.
  `sox in.wav out.wav` produces an exact-format copy.
- If the input is `-n` (synth, sox-from-nothing), there's nothing
  to propagate from, and sox falls back to compiled-in defaults
  (typically 48 kHz, 32-bit signed integer, mono — *not* the
  CD-style 44.1 kHz / 16-bit / stereo many tools assume). For
  example:

  ```bash
  sox -n tone.wav synth 3 sine 1000
  soxi tone.wav    # 48000 Hz, 32-bit, 1 channel
  ```

  If you need a specific shape, say so on the output:

  ```bash
  sox -n -r 44100 -b 16 -c 2 tone.wav synth 3 sine 1000
  ```

  This bites people whose downstream tools expect 16-bit PCM —
  consumer apps, embedded players, older DAWs — and reject 32-bit
  WAVs as "unsupported." [Chapter 6](06-format-conversions.md)
  covers how to specify output shape explicitly.
