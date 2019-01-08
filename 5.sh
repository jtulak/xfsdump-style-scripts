#!/usr/bin/env bash
set -euo pipefail
#  add a space after , and ; where there is none


find . -name '*.[ch]' ! -type d -exec gawk -i inplace '{
    $0 = gensub(/^([^"]*)([,;])([-.*_&a-zA-Z0-9])/, "\\1\\2 \\3", "g")
    $0 = gensub(/([,;])([-.*_&a-zA-Z0-9])([^"]*)$/, "\\1 \\2\\3", "g")
}; {print }' {} \;