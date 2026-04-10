# Combining Files

**Sample files** — download and place in your working directory:

<audio controls src="samples/music.wav"></audio>
<a href="samples/music.wav" download>⬇ music.wav</a> — "Erase Data" by Koi-discovery (CC0)

<audio controls src="samples/voice.wav"></audio>
<a href="samples/voice.wav" download>⬇ voice.wav</a> (CC0)

**Setup:**
```bash
sox -n a.wav synth 3 sine 440 gain -6
sox -n b.wav synth 3 sine 660 gain -6
# use the downloaded music.wav and voice.wav directly
```

## Per-input Zone 2 flags

With multiple inputs, Zone 2 format flags repeat independently for
each input file — place them immediately before the file they describe:

```bash
sox [Zone2a] infile_a [Zone2b] infile_b [Zone3] outfile [Zone4]
```

Any Zone 2 flag works this way: `-v`, `-r`, `-b`, `-c`, `-t`, `-e`.
The most common use is `-v` for per-input volume (shown below), and
format flags when combining files of different types or encodings.

`-v` takes a linear multiplier only — there is no dB form. Common
conversions: −6 dB ≈ `0.5`, −12 dB ≈ `0.25`, −20 dB = `0.1`.

```bash
sox -v 0.8 a.wav -t raw -r 48000 -b 32 -c 1 -e signed-integer -v 0.5 b.raw out.wav
```

## Concatenation — A then B

List multiple inputs before the output:

```bash
sox a.wav b.wav combined.wav
```

Files must have compatible sample rates and channel counts. If rates
differ, sox resamples to match the first file.

For a smooth crossfade at the join, use the `splice` effect:

```bash
sox a.wav b.wav out.wav splice 3    # crossfade at the 3-second mark
```

## Mixing — A over B

The `-m` flag (Zone 1) sums inputs together rather than concatenating:

```bash
sox -m music.wav voice.wav mixed.wav
```

Mixing raises the overall level — normalize afterward to avoid
clipping:

```bash
sox -m music.wav voice.wav mixed.wav norm -3
```

Set per-file volume with `-v` immediately before each input:

```bash
sox -m -v 0.3 music.wav -v 1.0 voice.wav out.wav norm -3
```

## Merging channels — A and B side by side

`-M` puts channels from each file side by side. Two mono files
become one stereo file:

```bash
sox -M left.wav right.wav stereo.wav
```

## remix — channel routing

Where `-c` uses sox's default averaging/duplication, `remix` gives
explicit control. Each argument describes one output channel by
naming the input channel(s) that feed it.

```bash
sox stereo.wav out.wav remix 2 1       # swap L and R
sox stereo.wav mono.wav remix -        # average all channels to mono
sox stereo.wav mono.wav remix 1        # keep left channel only, drop right
sox stereo.wav out.wav remix 1,2 1,2   # both output channels = L+R mix
```

`-` averages all input channels into one output channel — equivalent
to `-c 1` but as an explicit effect. `1,2` sums channels 1 and 2.
