#!/usr/bin/env bash
# add a space after some keywords: for, while, ... so we get 'for (' instead of 'for('

find . -name '*.[ch]' ! -type d -exec bash -c '
sed -i \
    -e "s/\(for\|while\|if\|switch\)(/\1 (/g" \
    -e "s/do{/do {/g" \
    $0
' {} \;