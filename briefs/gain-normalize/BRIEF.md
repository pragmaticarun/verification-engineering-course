# Brief: pcmx gain --normalize

## Goal
Peak-normalize a mono or stereo WAV file so the loudest sample has magnitude 1, and leave exact silence unchanged and finite.

## Acceptance
command: python3 briefs/gain-normalize/accept.py
expect_exit: 0

## Non-goals
- Sample-rate conversion
- MP3, AAC, or any container other than WAV
- Loudness normalization in LUFS

## Allowed-files
- pcmkit/crates/pcmkit/src/audio.rs
- pcmkit/crates/pcmx/src/main.rs
- briefs/gain-normalize/accept.py
