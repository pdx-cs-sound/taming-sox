# Basic Effects

## trim — cut out a section

```bash
sox test.wav out.wav trim start [length]
```

`trim` takes a start position and a *length*, not start and end.

```bash
sox test.wav out.wav trim 0 5      # first 5 seconds
sox test.wav out.wav trim 3 4      # 4 seconds starting at 3s
sox test.wav out.wav trim 5        # skip the first 5 seconds
sox test.wav out.wav trim -3       # last 3 seconds
sox test.wav out.wav trim 00:01:30 # start at 1m30s
```

Verify with `soxi -D out.wav`.

## reverse — play backwards

```bash
sox test.wav out.wav reverse
```

Sox loads the whole file into memory to do this; large files are slow.

## fade — smooth edges

```bash
sox test.wav out.wav fade [type] fade-in [duration] fade-out
```

The type can be `q` (quarter-sine, natural sounding), `t` (linear),
`h` (half-sine), or `l` (logarithmic). Omitting type defaults to
linear.

```bash
sox test.wav out.wav fade 1         # 1s linear fade-in, play to end
sox test.wav out.wav fade q 2 0 2   # 2s fade-in, full duration, 2s fade-out
```

Duration `0` means "play to the natural end of the file."

## vol and gain — adjust volume

`vol` takes a multiplier; `gain` takes decibels:

```bash
sox test.wav out.wav vol 0.5    # half amplitude
sox test.wav out.wav vol 2.0    # double (can clip!)
sox test.wav out.wav gain -6    # quieter by 6 dB
sox test.wav out.wav gain 6     # louder by 6 dB (can clip!)
```

A rough guide: −6 dB ≈ half perceived loudness; +6 dB ≈ double.

## norm — automatic normalization

`norm` brings the peak sample to a target level (default 0 dBFS):

```bash
sox test.wav out.wav norm       # peak to 0 dBFS
sox test.wav out.wav norm -3    # peak to -3 dBFS (safer headroom)
```

## stat — measure levels

Use `-n` as the output to discard audio and just print statistics:

```bash
sox test.wav -n stat
sox test.wav -n stats     # per-channel version
```

Stats print to stderr. Useful for spotting clipping before it
becomes a problem.
