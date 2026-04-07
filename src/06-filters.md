# Filters

Filters shape the frequency content of audio. A quick reference:
human hearing spans roughly 20 Hz (low rumble) to 20 kHz (high hiss).

## highpass and lowpass

Remove everything below or above a cutoff frequency:

```bash
sox test.wav out.wav highpass 200     # remove rumble below 200 Hz
sox test.wav out.wav lowpass 8000     # remove hiss above 8 kHz
sox test.wav out.wav highpass 300 lowpass 3400   # telephone band
```

## bass and treble

Shelving filters: boost or cut below/above a crossover point.
Argument is in dB.

```bash
sox test.wav out.wav bass 3      # boost bass by 3 dB
sox test.wav out.wav treble -6   # cut treble by 6 dB
sox test.wav out.wav bass 2 treble -2
```

## equalizer — parametric EQ

Three arguments: center frequency, bandwidth (Hz or `q` factor),
gain in dB. Stack multiple `equalizer` effects to build a full EQ.

```bash
sox test.wav out.wav equalizer 1000 200 -6    # cut 6 dB at 1 kHz
sox test.wav out.wav equalizer 3000 150 3     # boost 3 dB at 3 kHz
```

## A practical voice cleanup chain

```bash
sox raw_voice.wav clean.wav \
    highpass 100 \
    equalizer 3000 500 2 \
    norm -3
```

Removes low-frequency noise, adds a little presence, normalizes.
