#!/bin/bash

set -euxo pipefail

mkdir -p ./patched

fonts=(
  "Topaz_a500_v1.0.ttf"
  "TopazPlus_a500_v1.0.ttf"
  "Topaz_a1200_v1.0.ttf"
  "TopazPlus_a1200_v1.0.ttf"
  "MicroKnight_v1.0.ttf"
  "MicroKnightPlus_v1.0.ttf"
  "mO'sOul_v1.0.ttf"
  "P0T-NOoDLE_v1.0.ttf"
)

for font in "${fonts[@]}"; do
  fontforge -script bin/remap.py \
    "/fonts/amigafonts/ttf/${font}" \
    "/app/fonts/remapped/${font%.ttf}.patched.ttf" \
    ISO \
    2>/dev/null
done

fontforge -script bin/remap.py \
  '/fonts/ibm/ttf - Ac (aspect-corrected)/Ac437_IBM_VGA_9x16.ttf' \
  /app/fonts/remapped/Ac437_IBM_VGA_9x16.patched.ttf \
  CP437 \
  2>/dev/null

tree -C /app/fonts/remapped
