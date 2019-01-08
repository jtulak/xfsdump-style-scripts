#!/usr/bin/env bash
# indent and align

find . -name '*.[ch]' ! -type d -exec bash -c '
    uncrustify -c _uncrustify/linux.cfg --no-backup $0;
    sed -i \
    -e "s/!\b/! /g" \
    $0
' {} \;
