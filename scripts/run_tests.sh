#!/usr/bin/env bash
# Run tests/*.aura (or the files given as arguments). A file fails if it prints a
# FAIL line, crashes, exits non-zero, prints no PASS line, or prints an error.
# A failed require exits 1 since aura#4460 was fixed; `<error>` is still checked
# because an error through a user procedure skips the rest and exits 0 (aura#4465).
set -uo pipefail
source "$(dirname "$0")/env.sh"
status=0
files=("$@")
[ ${#files[@]} -eq 0 ] && files=("$REPO_ROOT"/tests/*.aura)
for t in "${files[@]}"; do
  s=$(date +%s)
  out=$("$AURA_BIN" "$t" 2>&1); rc=$?
  pass=$(grep -c '^PASS' <<<"$out" || true)
  secs=$(( $(date +%s) - s ))
  if [ $rc -ne 0 ] || [ "$pass" -eq 0 ] || grep -qE '^FAIL|AURA CRASH|^error:|load_module_file:|<error>' <<<"$out"; then
    echo "FAIL ${t#$REPO_ROOT/} (rc=$rc, $pass checks, ${secs}s)"
    echo "$out" | grep -E '^FAIL|CRASH|^error|load_module_file|<error>' | head -20
    status=1
  else
    echo "ok   ${t#$REPO_ROOT/} ($pass checks, ${secs}s)"
  fi
done
exit $status
