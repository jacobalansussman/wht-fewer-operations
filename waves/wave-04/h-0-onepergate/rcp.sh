#!/bin/sh
# rcp.sh up <local files...> <remote dir>   |   rcp.sh down <remote path> <local dir>
mode=$1; shift
if [ "$mode" = up ]; then
  eval last=\${$#}
  n=$(($# - 1)); files=""; i=1
  for a in "$@"; do if [ $i -le $n ]; then files="$files $a"; fi; i=$((i + 1)); done
  echo "remote copy removed: this script copied files to or from a rented Linux machine and cannot run here" >&2; exit 1
else
  echo "remote copy removed: this script copied files to or from a rented Linux machine and cannot run here" >&2; exit 1
fi
