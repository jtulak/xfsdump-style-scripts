#!/usr/bin/env bash
# remove trailing whitespaces

find . -name '*.[ch]' ! -type d -exec bash -c '
sed -i \
    -e "s/\s*$//" \
    $0
' {} \;