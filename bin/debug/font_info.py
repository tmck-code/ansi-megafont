#!/usr/bin/env python3

'''
FontForge script to print dimension info about a font.
Usage: fontforge -script font_info.py font.ttf
'''

import sys
import json
import fontforge


def print_font_info(font_path):
    """Print detailed dimension information about a font as JSON."""
    font = fontforge.open(font_path)
    
    # Calculate line heights
    typo_line_height = font.os2_typoascent - font.os2_typodescent + font.os2_typolinegap
    
    # Glyph counts
    glyph_count = sum(1 for _ in font.glyphs())
    glyphs_with_encoding = sum(1 for g in font.glyphs() if g.encoding >= 0)

    # Build data structure
    data = {
        "font_path": font_path,
        "font_name": font.fontname,
        "family_name": font.familyname,
        "em_size": font.em,
        "ascent": font.ascent,
        "descent": font.descent,
        "os2_ascent": font.os2_typoascent,
        "os2_descent": font.os2_typodescent,
        "os2_linegap": font.os2_typolinegap,
        "line_height": typo_line_height,
        "win_ascent": font.os2_winascent,
        "win_descent": font.os2_windescent,
        "win_linegap": font.os2_winascent + font.os2_windescent,
        "total_glyphs": glyph_count,
        "with_encoding": glyphs_with_encoding,
    }
    
    font.close()
    print(json.dumps(data))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fontforge -script font_info.py font1.ttf [font2.ttf ...]")
        sys.exit(1)
    
    for font_path in sys.argv[1:]:
        try:
            print_font_info(font_path)
        except Exception as e:
            print(f"Error processing {font_path}: {e}")
