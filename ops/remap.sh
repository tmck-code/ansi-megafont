#!/bin/bash

set -euo pipefail

mkdir -p ./patched

fontforge -script bin/remap.py \
    /fonts/amigafonts/ttf/MicroKnightPlus_v1.0.ttf \
    /app/fonts/remapped/MicroKnightPlus_v1.0.patched.ttf \
    ISO \
    2> /dev/null
fontforge -script bin/remap.py \
    "/fonts/amigafonts/ttf/mO'sOul_v1.0.ttf" \
    "/app/fonts/remapped/mO'sOul_v1.0.patched.ttf" \
    ISO \
    2> /dev/null
fontforge -script bin/remap.py \
    /fonts/amigafonts/ttf/P0T-NOoDLE_v1.0.ttf \
    /app/fonts/remapped/P0T-NOoDLE_v1.0.patched.ttf \
    ISO \
    2> /dev/null
fontforge -script bin/remap.py \
    /fonts/amigafonts/ttf/TopazPlus_a1200_v1.0.ttf \
    /app/fonts/remapped/TopazPlus_a1200_v1.0.patched.ttf \
    ISO \
    2> /dev/null
fontforge -script bin/remap.py \
    /fonts/amigafonts/ttf/TopazPlus_a500_v1.0.ttf \
    /app/fonts/remapped/TopazPlus_a500_v1.0.patched.ttf \
    ISO \
    2> /dev/null
fontforge -script bin/remap.py \
    '/fonts/ibm/ttf - Ac (aspect-corrected)/Ac437_IBM_VGA_9x16.ttf' \
    /app/fonts/remapped/Ac437_IBM_VGA_9x16.patched.ttf \
    CP437 \
    2> /dev/null
