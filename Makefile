remap_fonts:
	rm -rf fontsPatched
	mkdir -p fontsPatched
	fontforge -script bin/remap_font.py fonts/Ac437_IBM_VGA_9x16.ttf   fontsPatched/Ac437_IBM_VGA_9x16.patched.ttf CP437
	fontforge -script bin/remap_font.py fonts/MicroKnightPlus_v1.0.ttf fontsPatched/MicroKnightPlus.patched.ttf    ISO
	fontforge -script bin/remap_font.py fonts/"mO'sOul_v1.0.ttf"       fontsPatched/"mO'sOul.patched.ttf"          ISO
	fontforge -script bin/remap_font.py fonts/P0T-NOoDLE_v1.0.ttf      fontsPatched/P0T-NOoDLE.patched.ttf         ISO
	fontforge -script bin/remap_font.py fonts/TopazPlus_a1200_v1.0.ttf fontsPatched/TopazPlus_a1200.patched.ttf    ISO
	fontforge -script bin/remap_font.py fonts/TopazPlus_a500_v1.0.ttf  fontsPatched/TopazPlus_a500.patched.ttf     ISO

combine_fonts:
	fontforge -script ./bin/forge.py ./fontsPatched/ TopazPlusPlus

all: remap_fonts combine_fonts

.PHONY: remap_fonts combine_fonts all