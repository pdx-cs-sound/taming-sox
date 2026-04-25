# Format Options

Sox detects format from file extensions. When that isn't possible —
raw PCM files, pipes, unusual encodings — you provide it explicitly.

Recall from chapter 2: format flags describe the *next* filename.
Put them in the wrong section and they apply to the wrong file.

## The four core flags

These describe the audio itself. Sox will resample, convert, or
remix as needed to meet them.

| Flag | Meaning | Example |
| --- | --- | --- |
| `-r` | sample rate (Hz) | `-r 44100` |
| `-b` | bit depth | `-b 16` |
| `-c` | channels | `-c 1` (mono), `-c 2` (stereo) |
| `-e` | encoding | `-e signed-integer` |

Common encodings: `signed-integer`, `unsigned-integer`,
`floating-point`, `a-law`, `u-law`.

## The file type flag

`-t` is different: it names the container format (WAV, AIFF, FLAC,
raw, and so on) rather than a property of the audio. Sox normally
infers it from the filename extension, so you rarely set it. Reach
for `-t` only when there's no extension to read (pipes with `-`,
headerless raw files) or the extension lies about the content.

```bash
-t raw      # headerless PCM
-t wav      # force WAV regardless of extension
```

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

## Fully-specified output

Sometimes you want to know *exactly* what comes out: a specific
sample rate, bit depth, channel count, and encoding. This matters
for archival (so the artifact doesn't drift with the default audio
config), for interop (another tool expects 16-bit 44.1 kHz stereo
signed-integer and nothing else), and for pipelines that hand audio
to downstream processes with narrow assumptions.

The recipe: specify all four flags on the output.

```bash
sox input.wav -r 44100 -b 16 -c 2 -e signed-integer output.wav
```

That produces a WAV with exactly those properties regardless of
what the input looked like — sox resamples, converts bit depth,
remixes channels, and re-encodes as needed. Verify with `soxi
output.wav`.

The same four-flag pattern works for raw output — just add `-t raw`:

```bash
sox input.wav -t raw -r 44100 -b 16 -c 1 -e signed-integer output.raw
```

## Reading raw PCM

Raw files have no header, so you must describe them completely:

```bash
sox -r 44100 -b 16 -c 1 -e signed-integer input.raw output.wav
play output.wav
```

Writing raw output (see "Fully-specified output" above):

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
sox test.wav -p trim 0 5 | sox - output.wav norm -3
```

`-p` also preserves headroom across the pipe — samples above 0
dBFS survive into the second sox, where they can be scaled back
without clipping. A 16-bit WAV in the middle would clamp them.
See the headroom note in the previous chapter.
