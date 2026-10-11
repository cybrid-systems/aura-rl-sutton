#!/usr/bin/env bash
# Run tests/*.aura; fail if any prints a FAIL line, crashes, or exits non-zero.
set -uo pipefail
source "$(dirname "$0")/env.sh"
status=0
for t in "$REPO_ROOT"/tests/*.aura; do
  out=$("$AURA_BIN" "$t" 2>&1); rc=$?
  pass=$(grep -c '^PASS' <<<"$out" || true)
  if [ $rc -ne 0 ] || grep -qE '^FAIL|AURA CRASH|^error:' <<<"$out"; then
    echo "FAIL ${t#$REPO_ROOT/} (rc=$rc)"; echo "$out" | grep -E '^FAIL|CRASH|^error' | head -20
    status=1
  else
    echo "ok   ${t#$REPO_ROOT/} ($pass checks)"
  fi
done
exit $status
