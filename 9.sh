#!/usr/bin/env bash
set -euo pipefail
# there should be a single space inside of curly brackets
# add where missing "{foo}" and remove where too many "{   foo   }"

find . -name '*.[ch]' ! -type d -exec bash -c '
sed -i \
    -e "s/{\s*\(\S\)/{ \1/g" \
    -e "s/\(\S\)\s*}/\1 }/g" \
    $0
' {} \;