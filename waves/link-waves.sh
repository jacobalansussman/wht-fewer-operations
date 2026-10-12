#!/bin/sh
# link-waves.sh: let programs find the folders of other waves.
#
# The agents worked in one flat folder, and some programs reach into another
# agent's folder as ../<folder>/. Here the folders are sorted by wave. This
# script makes, in every wave folder, a symbolic link to each folder of the
# other waves. Nothing is copied and no file is changed.
#
#   sh waves/link-waves.sh         make the links
#   sh waves/link-waves.sh undo    remove them
#
# Do not commit the links.
cd "$(dirname "$0")" || exit 1
if [ "$1" = undo ]; then
  n=0
  for l in wave-*/*; do
    if [ -L "$l" ]; then rm "$l"; n=$((n + 1)); fi
  done
  echo "removed $n links"
  exit 0
fi
n=0
for d in wave-*/*/; do
  d=${d%/}
  [ -L "$d" ] && continue
  name=${d#*/}
  from=${d%%/*}
  for w in wave-*; do
    [ "$w" = "$from" ] && continue
    [ -e "$w/$name" ] && continue
    ln -s "../$d" "$w/$name" && n=$((n + 1))
  done
done
echo "made $n links"
