#!/usr/bin/env bash
set -euo pipefail
# remove the space before , and ;

# regex explanation:
# We are avoiding strings - replacing only those spaces that are not surrounded
# by ". At the same time, we want to ignore also those cases, where
# there are only whitespace in front of the commas/semicolons, as those are
# likely aligned. At the end, return a space between two semicolons in cases
# like for (foo ; ; bar), where the spaces are important for readability.

find . -name '*.[ch]' ! -type d -exec gawk -i inplace '{
    $0 = gensub(/^([^"]*[^[:space:]"][^"]*) ,/, "\\1,", "g")
    $0 = gensub(/^([^"]*[^[:space:]"][^"]*) ;/, "\\1;", "g")
    $0 = gensub(/^(.*[^[:space:]"].*) ,([^"]*)$/, "\\1,\\2", "g")
    $0 = gensub(/^(.*[^[:space:]"].*) ;([^"]*)$/, "\\1;\\2", "g")
    $0 = gensub(/([^([:space:]]);;([^\n])/, "\\1 ; ;\\2", "g")
}; {print }' {} \;