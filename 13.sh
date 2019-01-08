#!/usr/bin/env bash
# all lines of multilines comments should start with a star

find . -name '*.[ch]' ! -type d -exec bash -c '
    uncrustify -c _uncrustify/linux13.cfg --no-backup $0;
    sed -i \
    -e "s/!\b/! /g" \
    $0
' {} \;
