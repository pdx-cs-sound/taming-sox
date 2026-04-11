# Format Options

Sox detects format from file extensions. When that isn't possible —
raw PCM files, pipes, unusual encodings — you provide it explicitly.

Recall from chapter 2: format flags describe the *next* filename.
Put them in the wrong zone and they apply to the wrong file.

## The four core flags

| Flag | Meaning | Example |
|------|---------|---------|
| `-r` | sample rate (Hz) | `-r 44100` |
| `-b` | bit depth | `-b 16` |
| `-c` | channels | `-c 1` (mono), `-c 2` (stereo) |
| `-e` | encoding | `-e signed-integer` |
| `-t` | file type | `-t raw`, `-t wav` |

Common encodings: `signed-integer`, `unsigned-integer`,
`floating-point`, `a-law`, `u-law`.

## Resampling

```bash
sox input.wav -r 8000 telephone.wav    # downsample to 8 kHz
play telephone.wav                     # noticeably lo-fi
sox input.wav -r 48000 hq.wav          # upsample to 48 kHz
```

The format flag before `telephone.wav` describes the *output*.
Sox resamples automatically.

## Changing bit depth and channels

```bash
sox input.wav -b 24 output.wav    # convert to 24-bit
sox stereo.wav -c 1 mono.wav            # stereo → mono (averages channels)
play mono.wav
sox mono.wav -c 2 stereo.wav            # mono → stereo (duplicates channel)
```

`-c` uses sox's default algorithm: averaging when going down,
duplication when going up. For anything more specific — dropping a
channel, swapping L and R, custom mix weights — use `remix` (chapter 8).

## Reading raw PCM

Raw files have no header, so you must describe them completely:

```bash
sox -r 44100 -b 16 -c 1 -e signed-integer input.raw output.wav
play output.wav
```

Writing raw output:

```bash
sox input.wav -t raw -r 8000 -b 8 -c 1 -e unsigned-integer output.raw
```

## Piping

Use `-` for stdin or stdout, with `-t` to specify the format:

```bash
# Two sox processes in a pipeline
sox input.wav -t raw - | sox -t raw -r 44100 -b 16 -c 1 -e signed-integer - output.wav
```

For piping between two sox processes specifically, the `-p` flag
emits sox's own internal format, which avoids specifying all those
flags manually:

```bash
sox input.wav -p trim 10 | sox - output.wav norm -3
```
