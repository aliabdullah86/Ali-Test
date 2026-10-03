#!/usr/bin/env bash
# Downloads the brand fonts (all free, SIL Open Font License) from Google Fonts.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)/fonts"
mkdir -p "$DIR"
get() { [ -s "$DIR/$1" ] || curl -sSfL -o "$DIR/$1" "$2"; }
get CormorantGaramond-Light.ttf   https://fonts.gstatic.com/s/cormorantgaramond/v21/co3umX5slCNuHLi8bLeY9MK7whWMhyjypVO7abI26QOD_qE6GnM.ttf
get CormorantGaramond-Regular.ttf https://fonts.gstatic.com/s/cormorantgaramond/v21/co3umX5slCNuHLi8bLeY9MK7whWMhyjypVO7abI26QOD_v86GnM.ttf
get CormorantGaramond-Medium.ttf  https://fonts.gstatic.com/s/cormorantgaramond/v21/co3umX5slCNuHLi8bLeY9MK7whWMhyjypVO7abI26QOD_s06GnM.ttf
get CormorantGaramond-Italic.ttf  https://fonts.gstatic.com/s/cormorantgaramond/v21/co3smX5slCNuHLi8bLeY9MK7whWMhyjYrGFEsdtdc62E6zd58jDOjw.ttf
get PinyonScript-Regular.ttf      https://fonts.gstatic.com/s/pinyonscript/v24/6xKpdSJbL9-e9LuoeQiDRQR8aOI.ttf
get Montserrat-Regular.ttf        https://fonts.gstatic.com/s/montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtr6Ew-.ttf
get Montserrat-Medium.ttf         https://fonts.gstatic.com/s/montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtZ6Ew-.ttf
echo "fonts ready in $DIR"
