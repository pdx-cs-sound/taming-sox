# Chaining Effects

Effects in the effects chain are applied strictly left to right. The
output of one effect becomes the input to the next.

```bash
play test.wav trim 5 10 fade q 1 0 1 norm -3
#             ──────── ──────────── ──────
#             1. trim  2. fade      3. norm
```

## Order matters

```bash
# norm then gain: normalize to 0 dBFS, then boost 6 dB — likely clips
play test.wav norm gain 6

# gain then norm: boost first, then normalize back down — norm undoes the gain
play test.wav gain 6 norm
```

Neither is wrong — they just do different things. Think through the
pipeline before you run it.

## Headroom between effects

As noted in [chapter 2](02-conversions-anatomy.md), the effect chain runs in 32-bit signed
integers with 0 dBFS well below saturation, so samples can exceed
full-scale between effects without clipping. `gain 6` followed by
`norm` round-trips cleanly: the boost is preserved through the
chain and `norm` scales it back before output.

Clipping only happens at *boundaries* with a fixed-point format:

- The output file. Writing 16- or 24-bit PCM clamps anything still
  above 0 dBFS and prints `WARN ... clipped N samples`. Floating-
  point output (`-e floating-point -b 32`) has no such ceiling and
  passes out-of-range values through unchanged — but any *internal*
  clipping at the int32 ceiling earlier in the chain is permanent
  and shows up in the float output as distortion. See
  [chapter 2](02-conversions-anatomy.md).
- A pipe between two sox processes, if the pipe format is bounded.
  `sox a.wav -t wav - | sox - out.wav norm` clips at the 16-bit
  WAV in the middle. Use `sox -p` (sox's native 32-bit format) or
  a float WAV to preserve headroom across the pipe — see the
  Piping section in the next chapter.

## Writing to a file

When you're happy with the chain, swap `play` for `sox` and add an
output filename:

```bash
sox test.wav output.wav trim 5 10 fade q 1 0 1 norm -3
play output.wav
```

Sox converts the format *and* applies the effects in a single pass,
so trimming and converting to MP3 is one command:

```bash
sox test.wav output.mp3 trim 0 30 norm -3
play output.mp3
```
