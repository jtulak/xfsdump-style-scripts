#!/usr/bin/env bash
# add a newline between type and function name on definitions
# (so skip .h files for this)

find . -name '*.c' ! -type d -exec bash -c '
sed -i \
    -e "s/^\([_a-zA-Z0-9][_a-zA-Z0-9 \t]\+\) \([_a-zA-Z0-9]\+\)(\([^;]\+\)$/\1\n\2(\3/" \
    $0
' {} \;