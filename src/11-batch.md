# Batch Processing

Sox works well in shell scripts and pipelines. The examples here
assume a POSIX shell (`bash`, `zsh`, etc.).

## Shell loops

### Process a directory

```bash
mkdir -p normalized
for f in *.wav; do
    sox "$f" "normalized/$f" norm -3
done
```

### Construct output filenames

```bash
for f in *.wav; do
    out="${f%.wav}_clean.wav"
    sox "$f" "$out" highpass 100 norm -3
done
```

`${f%.wav}` strips the `.wav` suffix.

### Batch format conversion

```bash
mkdir -p mp3
for f in *.wav; do
    sox "$f" "mp3/${f%.wav}.mp3"
done
```

### Use soxi in scripts

```bash
duration=$(soxi -D "$f")
if awk "BEGIN { exit !($duration > 5) }"; then
    sox "$f" trimmed.wav trim 0 5
fi
```

### Parallel processing

```bash
ls *.wav | xargs -P 4 -I{} sox {} "out/{}" norm -3
```

### Check exit codes

Sox exits non-zero on errors. Always check in scripts:

```bash
for f in *.wav; do
    sox "$f" "out/$f" norm -3 || echo "Failed: $f" >&2
done
```

### Piping between sox processes

The `-p` flag emits sox's internal format on stdout — no need to
specify sample rate, bit depth, or encoding on the receiving end:

```bash
sox voice.wav -p trim 0 3 | play - reverb 80
```

This avoids intermediate files in multi-step pipelines.
