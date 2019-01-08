#!/usr/bin/env bash
# intercharacter spaces

find . -name '*.[ch]' ! -type d -exec bash -c '
    uncrustify -c _uncrustify/linux11.cfg --no-backup $0;
    sed -i \
    -e "s/!\b/! /g" \
    $0
' {} \;

# but return back changes defines that would cause redefinition error
sed -i \
    -e 's/^#define sizeofmember.*$/#define\tsizeofmember( t, m ) sizeof( ( ( t * )0 )->m )/' \
    -e 's/^#define offsetofmember.*$/#define\toffsetofmember( t, m ) ( ( size_t )( char * )\&( ( ( t * )0 )->m ) )/' \
    common/types.h