#!/usr/bin/env bash
set -euo pipefail
# remove spaces from dereferences and negations
# the regexes are duplicated, because awk won't replace overlapping patterns

# TODO do not include this script in automatic checks, too unreliable.

find . -name '*.[ch]' ! -type d -exec gawk -i inplace '{
    $0 = gensub(/^([^"]*)\(\* /, "\\1(*", "g") # foo(* bar
    $0 = gensub(/\(\* ([^"]*)$/, "(*\\1", "g") #
    $0 = gensub(/^([^ *#]{2}[^"]*)! /, "\\1!", "g") # space after exclamation mark
    $0 = gensub(/^([^ *#]{2}[^"]*)! /, "\\1!", "g") # space after exclamation mark
    $0 = gensub(/^([^ *#]{2}[^"]*)! /, "\\1!", "g") # space after exclamation mark
}; {print }' {} \;