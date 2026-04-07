# Chaining Effects

Effects in Zone 4 are applied strictly left to right. The output of
one effect becomes the input to the next.

```bash
sox source.wav out.wav trim 5 10 fade q 1 0 1 norm -3
#                       ──────── ──────────── ──────
#                       1. trim  2. fade      3. norm
```

## Order matters

```bash
# norm then gain: normalize to 0 dBFS, then boost 6 dB — likely clips
sox source.wav out.wav norm gain 6

# gain then norm: boost first, then normalize back down — norm undoes the gain
sox source.wav out.wav gain 6 norm
```

Neither is wrong — they just do different things. Think through the
pipeline before you run it.

## Audition with play

You don't need to write a file to hear the result. Use `play`:

```bash
play source.wav trim 5 10 fade q 1 0 1 norm -3
```

Same syntax, same effects, no output file. Iterate here, then write
the file when you're satisfied.

## Format conversion and effects together

These work in one command:

```bash
sox source.wav output.mp3 trim 0 30 norm -3
```

Sox converts the format *and* applies the effects in a single pass.
