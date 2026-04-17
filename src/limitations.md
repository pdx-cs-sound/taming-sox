# What sox isn't

Sox is a Swiss Army knife, but some problems aren't shaped like a
knife. Knowing what sox is *not* good at saves time:

- **No phase vocoder.** WSOLA (`tempo`, `pitch`) works well but
  produces artifacts on complex material; use Rubber Band (see
  Further Reading) when quality matters.
- **No multitrack routing.** Sox processes one stream at a time.
  For independent tracks with sends and returns, look at `ecasound`
  or a DAW.
- **No streaming protocols.** Sox reads and writes files and pipes;
  it has no RTSP, HLS, or WebRTC support.
