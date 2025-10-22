#!/usr/bin/env bash
set -euo pipefail

: "${PIPER_VOICES_DIR:=/voices}"
: "${PIPER_VOICE:=en_GB-alan-medium}"

PIPER_VOICE_FILE="$PIPER_VOICES_DIR/$PIPER_VOICE.onyx"

echo "[entrypoint] Voices dir: $PIPER_VOICES_DIR"
mkdir -p "$PIPER_VOICES_DIR"

if [[ ! -f "$PIPER_VOICE_FILE" ]]; then
  echo "[entrypoint] Voice not found at $PIPER_VOICE_FILE, downloading..."
  python -m piper.download_voices \
    --debug \
    --download-dir "$PIPER_VOICES_DIR" \
    "$PIPER_VOICE"
else
  echo "[entrypoint] Voice found at $PIPER_VOICE_FILE"
fi

echo "[entrypoint] Launching bot..."
exec "$@"