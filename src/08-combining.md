# Combining Files

**Setup:**
```bash
sox -n a.wav synth 3 sine 440
sox -n b.wav synth 3 sine 660
sox -n music.wav synth 5 sine 220
sox -n voice.wav synth 5 sine 880
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

`remix` lets you route and combine channels explicitly. Arguments
are output channel assignments.

```bash
sox stereo.wav out.wav remix 2 1       # swap L and R
sox stereo.wav mono.wav remix -        # mix all channels to mono
sox stereo.wav mono.wav remix 1 2      # keep both channels
```

`-` means "average all input channels into this output channel."
