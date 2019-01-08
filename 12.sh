#!/usr/bin/env bash
# newlines

find . -name '*.[ch]' ! -type d -exec bash -c '
    uncrustify -c _uncrustify/linux12.cfg --no-backup $0;
    sed -i \
    -e "s/!\b/! /g" \
    $0
' {} \;
