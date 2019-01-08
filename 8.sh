#!/usr/bin/env bash
# change the multiline comment style from /* foo to /*\n * foo

find . -name '*.[ch]' ! -type d -exec bash -c '
sed -i \
    -e "s/^\(\s*\)\/\* \(.\+[^*][^/]\)$/\1\/*\n\1 * \2/g" \
    $0
' {} \;