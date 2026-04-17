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
