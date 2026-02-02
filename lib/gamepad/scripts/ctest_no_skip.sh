#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ctest_no_skip.sh <build_dir>

Env:
  CTEST_ARGS="--rerun-failed --verbose"  # optional extra args

Behavior:
  - runs ctest with --output-on-failure
  - fails if LastTest.log contains SKIP / Not Run
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

build_dir="$1"
if [[ ! -d "${build_dir}" ]]; then
  echo "❌ build_dir not found: ${build_dir}"
  exit 2
fi

ctest_args=()
if [[ -n "${CTEST_ARGS:-}" ]]; then
  # shellcheck disable=SC2206
  ctest_args=(${CTEST_ARGS})
fi

ctest --test-dir "${build_dir}" --output-on-failure "${ctest_args[@]}"

last_log="${build_dir}/Testing/Temporary/LastTest.log"
if [[ ! -f "${last_log}" ]]; then
  echo "❌ LastTest.log not found: ${last_log}"
  exit 3
fi

if grep -nE 'Not Run|\bSKIP\b|\*\*\*Skipped|Skipped' "${last_log}"; then
  echo "❌ Found SKIP/Not Run in LastTest.log: ${last_log}"
  exit 4
fi

echo "✅ no-skip gate PASS: ${last_log}"
