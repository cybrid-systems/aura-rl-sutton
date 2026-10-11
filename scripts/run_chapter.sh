#!/usr/bin/env bash
# Run every .aura driver of one chapter: scripts/run_chapter.sh 2
set -euo pipefail
source "$(dirname "$0")/env.sh"
ch=$(printf "%02d" "${1:?usage: run_chapter.sh <chapter-number>}")
shopt -s nullglob
files=("$REPO_ROOT"/chapters/ch${ch}_*/*.aura)
if [ ${#files[@]} -eq 0 ]; then
  echo "chapter $ch: no .aura drivers yet (see chapters/ch${ch}_*/README.md)"
  exit 0
fi
for f in "${files[@]}"; do
  echo "== ${f#$REPO_ROOT/}"
  "$AURA_BIN" "$f"
done
