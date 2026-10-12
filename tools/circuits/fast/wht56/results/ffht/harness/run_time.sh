#!/bin/sh
# run_time.sh -- one timing run of the harness under the rules of this job.
#
#   sh run_time.sh OUTFILE [arguments of "harness time"]
#
# See locked_run.sh for what happens around the run (waiting, the lock, the pinning, the record
# of the load before and after).
here=$(cd "$(dirname "$0")" && pwd)
out=$1
[ -n "$out" ] || { echo "usage: sh run_time.sh OUTFILE [harness time arguments]" >&2; exit 2; }
shift
exec sh "$here/locked_run.sh" "$out" "$here/build/harness" time "$@"
