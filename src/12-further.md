# Further Reading

## The manual

`man sox` is the authoritative reference — comprehensive, well-written,
and covers every effect and flag in detail. Two companion pages are
also worth bookmarking:

```bash
man sox          # effects, global options, examples
man soxformat    # format flags, encodings, file type details
```

## LADSPA plugins

Sox can load any LADSPA plugin via the `ladspa` effect, which opens
up hundreds of production-quality processors — noise gates, limiters,
multiband compressors, pitch correction, and more:

```bash
# List installed plugins
listplugins

# Apply a plugin by label
play voice.wav ladspa <plugin-label> [params...]
```

On Debian/Ubuntu, `apt install swh-plugins` installs Steve Harris's
widely-used collection. LADSPA extends sox without changing its
pipeline model.

## ffmpeg

`ffmpeg` handles the containers and codecs sox can't: AAC, Opus,
MP4, video tracks, streaming protocols. The two tools pair naturally
— use ffmpeg to get audio into or out of awkward formats, sox for
signal processing:

```bash
# Extract audio from a video, then process with sox
ffmpeg -i video.mp4 -vn audio.wav
sox audio.wav processed.wav highpass 100 norm -3
```

## When sox isn't enough: Rubber Band

Sox has no phase vocoder. WSOLA (`tempo`, `pitch`) is fast and
reasonable, but on complex music you can hear it working. For
higher-quality time-stretching, pitch-shifting, or near-unity
resampling, reach for
[`rubberband`](https://breakfastquay.com/rubberband/):

```bash
rubberband --tempo 1.2 input.wav output.wav   # 20% faster (same sense as sox tempo)
rubberband --time 0.8 input.wav output.wav    # 0.8x duration (--time is 1/--tempo)
rubberband --pitch 2 input.wav output.wav     # up 2 semitones (not cents)
rubberband --pitch -2 --tempo 1.1 input.wav output.wav  # combine freely
```

Rubber Band has two engines: R2 (default, fast, WSOLA-based) and R3
(slower, phase vocoder, noticeably better on music):

```bash
rubberband --fine --pitch 4 input.wav output.wav   # R3 engine
rubberband-r3 --pitch 4 input.wav output.wav       # equivalent
```

For vocal pitch-shifting, `--formant` preserves the formant
structure so voices don't sound cartoonish:

```bash
rubberband --fine --formant --pitch 3 voice.wav output.wav
```

`rubberband` doesn't support stdout, so to combine with sox for
format conversion, route through a temp file:

```bash
rubberband -q --pitch 2 input.wav tmp.wav && sox tmp.wav output.flac
```

## libsox

Sox is also a C library. If you need to embed audio processing in a
program, `libsox` exposes the full effect chain and format I/O via
a C API. The header is `sox.h`; the source ships with examples.

## Limitations

Knowing what sox is *not* good at saves time:

- **No phase vocoder.** WSOLA works well but produces artifacts on
  complex material; use Rubber Band (covered above) when quality matters.
- **No multitrack routing.** Sox processes one stream at a time.
  For independent tracks with sends and returns, look at `ecasound`
  or a DAW.
- **No streaming protocols.** Sox reads and writes files and pipes;
  it has no RTSP, HLS, or WebRTC support.
