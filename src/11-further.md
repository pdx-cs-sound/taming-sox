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

## libsox

Sox is also a C library. If you need to embed audio processing in a
program, `libsox` exposes the full effect chain and format I/O via
a C API. The header is `sox.h`; the source ships with examples.

## Limitations

Knowing what sox is *not* good at saves time:

- **No phase vocoder.** WSOLA works well but produces artifacts on
  complex material; use Rubber Band (chapter 7) when quality matters.
- **No multitrack routing.** Sox processes one stream at a time.
  For independent tracks with sends and returns, look at `ecasound`
  or a DAW.
- **No streaming protocols.** Sox reads and writes files and pipes;
  it has no RTSP, HLS, or WebRTC support.
