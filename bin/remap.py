#!/usr/bin/env python3
'''
FontForge script to remap CP437/ISO-8859-1 characters from Unicode positions to their original positions.
Usage: fontforge -script bin/remap.py input.ttf output.ttf
'''

import json
import sys
from typing import NamedTuple

import fontforge
from laser_prynter.pbar import PBar

# cp437_code: (unicode_code, glyph_name)
CP437_TO_UNICODE = {
    0x80: (0x00C7, 'Ccedilla'),
    0x81: (0x00FC, 'udieresis'),
    0x82: (0x00E9, 'eacute'),
    0x83: (0x00E2, 'acircumflex'),
    0x84: (0x00E4, 'adieresis'),
    0x85: (0x00E0, 'agrave'),
    0x86: (0x00E5, 'aring'),
    0x87: (0x00E7, 'ccedilla'),
    0x88: (0x00EA, 'ecircumflex'),
    0x89: (0x00EB, 'edieresis'),
    0x8A: (0x00E8, 'egrave'),
    0x8B: (0x00EF, 'idieresis'),
    0x8C: (0x00EE, 'icircumflex'),
    0x8D: (0x00EC, 'igrave'),
    0x8E: (0x00C4, 'Adieresis'),
    0x8F: (0x00C5, 'Aring'),
    0x90: (0x00C9, 'Eacute'),
    0x91: (0x00E6, 'ae'),
    0x92: (0x00C6, 'AE'),
    0x93: (0x00F4, 'ocircumflex'),
    0x94: (0x00F6, 'odieresis'),
    0x95: (0x00F2, 'ograve'),
    0x96: (0x00FB, 'ucircumflex'),
    0x97: (0x00F9, 'ugrave'),
    0x98: (0x00FF, 'ydieresis'),
    0x99: (0x00D6, 'Odieresis'),
    0x9A: (0x00DC, 'Udieresis'),
    0x9B: (0x00A2, 'cent'),
    0x9C: (0x00A3, 'sterling'),
    0x9D: (0x00A5, 'yen'),
    0x9E: (0x20A7, 'peseta'),
    0x9F: (0x0192, 'florin'),
    0xA0: (0x00E1, 'aacute'),
    0xA1: (0x00ED, 'iacute'),
    0xA2: (0x00F3, 'oacute'),
    0xA3: (0x00FA, 'uacute'),
    0xA4: (0x00F1, 'ntilde'),
    0xA5: (0x00D1, 'Ntilde'),
    0xA6: (0x00AA, 'ordfeminine'),
    0xA7: (0x00BA, 'ordmasculine'),
    0xA8: (0x00BF, 'questiondown'),
    0xA9: (0x2310, 'revlogicalnot'),
    0xAA: (0x00AC, 'logicalnot'),
    0xAB: (0x00BD, 'onehalf'),
    0xAC: (0x00BC, 'onequarter'),
    0xAD: (0x00A1, 'exclamdown'),
    0xAE: (0x00AB, 'guillemotleft'),
    0xAF: (0x00BB, 'guillemotright'),
    0xB0: (0x2591, 'ltshade'),
    0xB1: (0x2592, 'shade'),
    0xB2: (0x2593, 'dkshade'),
    0xB3: (0x2502, 'SF100000'),
    0xB4: (0x2524, 'SF110000'),
    0xB5: (0x2561, 'SF190000'),
    0xB6: (0x2562, 'SF200000'),
    0xB7: (0x2556, 'SF210000'),
    0xB8: (0x2555, 'SF220000'),
    0xB9: (0x2563, 'SF230000'),
    0xBA: (0x2551, 'SF240000'),
    0xBB: (0x2557, 'SF250000'),
    0xBC: (0x255D, 'SF260000'),
    0xBD: (0x255C, 'SF270000'),
    0xBE: (0x255B, 'SF280000'),
    0xBF: (0x2510, 'SF030000'),
    0xC0: (0x2514, 'SF020000'),
    0xC1: (0x2534, 'SF070000'),
    0xC2: (0x252C, 'SF060000'),
    0xC3: (0x251C, 'SF080000'),
    0xC4: (0x2500, 'SF050000'),
    0xC5: (0x253C, 'SF090000'),
    0xC6: (0x255E, 'SF360000'),
    0xC7: (0x255F, 'SF370000'),
    0xC8: (0x255A, 'SF380000'),
    0xC9: (0x2554, 'SF390000'),
    0xCA: (0x2569, 'SF400000'),
    0xCB: (0x2566, 'SF410000'),
    0xCC: (0x2560, 'SF420000'),
    0xCD: (0x2550, 'SF430000'),
    0xCE: (0x256C, 'SF440000'),
    0xCF: (0x2567, 'SF450000'),
    0xD0: (0x2568, 'SF460000'),
    0xD1: (0x2564, 'SF470000'),
    0xD2: (0x2565, 'SF480000'),
    0xD3: (0x2559, 'SF490000'),
    0xD4: (0x2558, 'SF500000'),
    0xD5: (0x2552, 'SF510000'),
    0xD6: (0x2553, 'SF520000'),
    0xD7: (0x256B, 'SF530000'),
    0xD8: (0x256A, 'SF540000'),
    0xD9: (0x2518, 'SF010000'),
    0xDA: (0x250C, 'SF040000'),
    0xDB: (0x2588, 'block'),
    0xDC: (0x2584, 'dnblock'),
    0xDD: (0x258C, 'lfblock'),
    0xDE: (0x2590, 'rtblock'),
    0xDF: (0x2580, 'upblock'),
    0xE0: (0x03B1, 'alpha'),
    0xE1: (0x00DF, 'germandbls'),
    0xE2: (0x0393, 'Gamma'),
    0xE3: (0x03C0, 'pi'),
    0xE4: (0x03A3, 'Sigma'),
    0xE5: (0x03C3, 'sigma'),
    0xE6: (0x00B5, 'mu'),
    0xE7: (0x03C4, 'tau'),
    0xE8: (0x03A6, 'Phi'),
    0xE9: (0x0398, 'Theta'),
    0xEA: (0x03A9, 'Omega'),
    0xEB: (0x03B4, 'delta'),
    0xEC: (0x221E, 'infinity'),
    0xED: (0x03C6, 'phi'),
    0xEE: (0x03B5, 'epsilon'),
    0xEF: (0x2229, 'intersection'),
    0xF0: (0x2261, 'equivalence'),
    0xF1: (0x00B1, 'plusminus'),
    0xF2: (0x2265, 'greaterequal'),
    0xF3: (0x2264, 'lessequal'),
    0xF4: (0x2320, 'integraltp'),
    0xF5: (0x2321, 'integralbt'),
    0xF6: (0x00F7, 'divide'),
    0xF7: (0x2248, 'approxequal'),
    0xF8: (0x00B0, 'degree'),
    0xF9: (0x2219, 'periodcentered'),
    0xFA: (0x00B7, 'middot'),
    0xFB: (0x221A, 'radical'),
    0xFC: (0x207F, 'nsuperior'),
    0xFD: (0x00B2, 'twosuperior'),
    0xFE: (0x25A0, 'filledbox'),
    0xFF: (0x00A0, 'nbspace'),
}

ISO8859_1_NON_PRINTING_TO_UNICODE = {
    0x00: (0x20, ''),
    0x01: (0x00, ''),
    0x02: (0x110008, ''),
    0x03: (0x02, ''),
    0x04: (0x110009, ''),
    0x05: (0x11000A, ''),
    0x06: (0x11000B, ''),
    0x07: (0x11000C, ''),
    0x08: (0x11000D, ''),
    0x09: (0x11000E, ''),
    0x0A: (0x09, ''),
    0x0B: (0x0A, ''),
    0x0C: (0x11000F, ''),
    0x0D: (0x110010, ''),
    0x0E: (0x0D, ''),
    0x0F: (0x110011, 'SI'),
    0x10: (0x110012, 'DLE'),
    0x11: (0x110013, 'DC1'),
    0x12: (0x110014, 'DC2'),
    0x13: (0x110015, 'DC3'),
    0x14: (0x110016, 'DC4'),
    0x15: (0x110017, 'NAK'),
    0x16: (0x110018, 'SYN'),
    0x17: (0x110019, 'ETB'),
    0x18: (0x11001A, 'CAN'),
    0x19: (0x11001B, 'EM'),
    0x1A: (0x11001C, 'SUB'),
    0x1B: (0x11001D, 'ESC'),
    0x1C: (0x11001E, 'FS'),
    0x1D: (0x11001F, 'GS'),
    0x1E: (0x110020, 'RS'),
    0x1F: (0x110021, 'US'),
    0x20: ('space', 'space'),
    0x7F: (0x110023, ''),
}

ISO8859_1_NON_PRINTING_BLANK_TO_UNICODE = {
    0x00: (0x20, ''),
    0x01: (0x20, ''),
    0x02: (0x20, ''),
    0x03: (0x20, ''),
    0x04: (0x20, ''),
    0x05: (0x20, ''),
    0x06: (0x20, ''),
    0x07: (0x20, ''),
    0x08: (0x20, ''),
    0x09: (0x20, ''),
    0x0A: (0x20, ''),
    0x0B: (0x20, ''),
    0x0C: (0x20, ''),
    0x0D: ('nonmarkingreturn', 'CR'),
    0x0E: (0x20, ''),
    0x0F: (0x20, ''),
    0x10: (0x20, ''),
    0x11: (0x20, ''),
    0x12: (0x20, ''),
    0x13: (0x20, ''),
    0x14: (0x20, ''),
    0x15: (0x20, ''),
    0x16: (0x20, ''),
    0x17: (0x20, ''),
    0x18: (0x20, ''),
    0x19: (0x20, ''),
    0x1A: (0x20, ''),
    0x1B: (0x20, ''),
    0x1C: (0x20, ''),
    0x1D: (0x20, ''),
    0x1E: (0x20, ''),
    0x1F: (0x20, ''),
    0x20: ('space', 'space'),
    0x7F: ('uni007F', 'DEL'),
}


TOPAZ_1200_MAPPING = ISO8859_1_NON_PRINTING_TO_UNICODE | {
    0x81: (0x110024, ''),
    0x8D: (0x110002, ''),
    0x8E: (0x110003, ''),
    0x8F: (0x110004, ''),
    0x90: (0x110005, ''),
    0x9D: (0x110006, ''),
    0x9E: (0x110007, ''),
}


MOSOUL_MAPPING = ISO8859_1_NON_PRINTING_BLANK_TO_UNICODE | {
    0x80: (0x9F, ''),
    0x81: (0x9F, ''),
    0x82: (0x9F, ''),
    0x83: (0x9F, ''),
    0x84: (0x9F, ''),
    0x85: (0x9F, ''),
    0x86: (0x9F, ''),
    0x87: (0x9F, ''),
    0x88: (0x9F, ''),
    0x89: (0x9F, ''),
    0x8A: (0x9F, ''),
    0x8B: (0x9F, ''),
    0x8C: (0x9F, ''),
    0x8D: (0x9F, ''),
    0x8E: (0x9F, ''),
    0x8F: (0x9F, ''),
    0x90: (0x9F, ''),
    0x91: (0x9F, ''),
    0x92: (0x9F, ''),
    0x93: (0x9F, ''),
    0x94: (0x9F, ''),
    0x95: (0x9F, ''),
    0x96: (0x9F, ''),
    0x97: (0x9F, ''),
    0x98: (0x9F, ''),
    0x99: (0x9F, ''),
    0x9A: (0x9F, ''),
    0x9B: (0x9F, ''),
    0x9C: (0x9F, ''),
    0x9D: (0x9F, ''),
    0x9E: (0x9F, ''),
    0x9F: (0x9F, ''),
    0x7F: (0x110007, 'DEL'),
}
TOPAZ_500_MAPPING = MOSOUL_MAPPING | {
    0x7F: (0x110022, 'DEL'),
}

MICROKNIGHTPLUS_MAPPING = ISO8859_1_NON_PRINTING_BLANK_TO_UNICODE | {
    0x20: (0x20, ''),
    0x7F: (0x10FFFF + 0x23, ''),
    0x81: (0x10FFFF + 0x24, ''),
    0x87: (0x20, ''),  # cent char is missing
    0x8D: (0x10FFFF + 2, ''),
    0x8E: (0x10FFFF + 3, ''),
    0x8F: (0x10FFFF + 4, ''),
    0x90: (0x10FFFF + 5, ''),
    0x9D: (0x10FFFF + 6, ''),
    0x9E: (0x10FFFF + 7, ''),
}

P0TNOODLE_MAPPING = (
    MICROKNIGHTPLUS_MAPPING
    | ISO8859_1_NON_PRINTING_TO_UNICODE
    | {
        0x7F: (0x110022, 'DEL'),
        0x81: (0x10FFFF + 0x24, ''),
    }
)


class FontMetrics(NamedTuple):
    em_size:         int
    ascent:          int
    descent:         int
    os2_typoascent:  int = 0
    os2_typodescent: int = 0
    os2_typolinegap: int = 0
    hea_ascent:      int = 0
    hea_descent:     int = 0
    hea_linegap:     int = 0
    os2_winascent:   int = 0
    os2_windescent:  int = 0
    upos:            int = 0
    uwidth:          int = 0

    @classmethod
    def from_font(cls, font):
        return cls(
            em_size         = font.em,
            ascent          = font.ascent,
            descent         = font.descent,
            os2_typoascent  = font.os2_typoascent,
            os2_typodescent = font.os2_typodescent,
            os2_typolinegap = font.os2_typolinegap,
            hea_ascent      = font.hhea_ascent,
            hea_descent     = font.hhea_descent,
            hea_linegap     = font.hhea_linegap,
            os2_winascent   = font.os2_winascent,
            os2_windescent  = font.os2_windescent,
            upos            = font.upos,
            uwidth          = font.uwidth,
        )

    @classmethod
    def to_font(cls, font, dims):
        font.em                   = dims.em_size
        font.ascent               = dims.ascent
        font.descent              = dims.descent
        font.os2_typoascent       = dims.os2_typoascent
        font.os2_typodescent      = dims.os2_typodescent
        font.os2_typolinegap      = dims.os2_typolinegap
        font.hhea_ascent          = dims.hea_ascent
        font.hhea_descent         = dims.hea_descent
        font.hhea_linegap         = dims.hea_linegap
        font.os2_winascent        = dims.os2_winascent
        font.os2_windescent       = dims.os2_windescent
        font.os2_use_typo_metrics = True
        font.upos                 = dims.upos
        font.uwidth               = dims.uwidth

    def __str__(self):
        s = 'FontMetrics:'
        for field in self._fields:
            s += f'\n  {f"{field}:":<16} = {getattr(self, field)}'
        return s


def remap_glyph(source_font, new_font, source_code, target_code, glyph_name, offset):
    for offset in (0, offset):
        if source_code == 0x20:
            space_glyph = source_font['space']
            width = space_glyph.width
        new_glyph = new_font.createChar(target_code + offset)
        if source_code == 0x20:
            new_glyph.width = width
            continue
        if glyph_name:
            new_glyph.glyphname = glyph_name

        new_font.selection.select(target_code + offset)
        new_font.paste()
    return True

OFFSETS = {
    # amiga fonts
    'Topaz_a500_v1.0':      {'offset': 0xE000, 'mapping': TOPAZ_500_MAPPING},
    'TopazPlus_a500_v1.0':  {'offset': 0xE100, 'mapping': TOPAZ_500_MAPPING},
    'Topaz_a1200_v1.0':     {'offset': 0xE200, 'mapping': TOPAZ_1200_MAPPING},
    'TopazPlus_a1200_v1.0': {'offset': 0xE300, 'mapping': TOPAZ_1200_MAPPING},
    'MicroKnight_v1.0':     {'offset': 0xE400, 'mapping': MICROKNIGHTPLUS_MAPPING},
    'MicroKnightPlus_v1.0': {'offset': 0xE500, 'mapping': MICROKNIGHTPLUS_MAPPING},
    "mO'sOul_v1.0":         {'offset': 0xE600, 'mapping': MOSOUL_MAPPING},
    'P0T-NOoDLE_v1.0':      {'offset': 0xE700, 'mapping': P0TNOODLE_MAPPING},
    # ibm fonts
    'Ac437_IBM_VGA_9x16':   {'offset': 0xE800, 'mapping': CP437_TO_UNICODE},
}

def remap_font(input_font, output_font, encoding):
    'Create a new font with Unicode encoding from a CP436/ISO-8859-1 font.'

    print(f'Remapping: \x1b[93m{input_font}\x1b[0m')
    source_font = fontforge.open(input_font)
    source_font.encoding = 'UnicodeFull'

    offset = 0
    for f, offset in OFFSETS.items():
        if f in input_font:
            mapping = OFFSETS[f]['mapping']
            offset = OFFSETS[f]['offset']
            break
    else:
        raise ValueError('No font mapping found!')

    dims = FontMetrics.from_font(source_font)

    new_font = fontforge.font()

    new_font.fontname = source_font.fontname
    new_font.familyname = source_font.familyname
    new_font.fullname = source_font.fullname
    new_font.copyright = source_font.copyright
    new_font.version = source_font.version
    new_font.encoding = 'UnicodeFull'

    FontMetrics.to_font(new_font, dims)
    print(dims, end='\n\n')

    # Copy extended characters from Unicode positions to CP437 positions
    print('Remapping characters 0x00-0xFF')

    # Group mappings by source to avoid repeated copying of the same glyph
    source_to_targets = {}
    with PBar(0xFF+1, *PBar.randgrad()) as pb:
        for from_code in range(0x00, 0xFF + 1):
            if from_code in mapping:
                unicode_code, glyph_name = mapping[from_code]
                if not glyph_name and isinstance(unicode_code, int):
                    glyph_name = f'uni{unicode_code:04X}'
            else:
                unicode_code = from_code
                glyph_name = (
                    source_font[from_code].glyphname
                    if from_code in source_font
                    else f'uni{from_code:04X}'
                )

            # Convert glyph names to unicode positions for proper selection
            if isinstance(unicode_code, str):
                # Try to find the glyph by name in the source font
                try:
                    glyph = source_font[unicode_code]
                    actual_unicode = glyph.unicode
                    if actual_unicode < 0:
                        # Glyph has no unicode mapping, skip it
                        print(f'\x1b[31m  Skipping {unicode_code} (no unicode mapping) for 0x{from_code:02X}\x1b[0m')
                        continue
                    unicode_code = actual_unicode
                except (TypeError, KeyError):
                    print(f'\x1b[31m  Warning: glyph {unicode_code} not found in source font for 0x{from_code:02X}\x1b[0m')
                    continue

            if unicode_code not in source_to_targets:
                source_to_targets[unicode_code] = []
            source_to_targets[unicode_code].append((from_code, glyph_name))
            pb.update(1)

    with PBar(sum(len(targets) for targets in source_to_targets.values()), *PBar.randgrad()) as pb:
        # Process each unique source glyph
        for unicode_code, targets in source_to_targets.items():
            # Copy once from source
            try:
                source_font.selection.select(unicode_code)
                source_font.copy()

                # Paste to all targets
                for from_code, glyph_name in targets:
                    print(
                        f'  Copying 0x{f"{unicode_code:04X}":<8} > 0x{f"{from_code:02X}":<8} {f"({glyph_name})":<15}',
                        end='',
                    )
                    pb.update(1)
                    remap_glyph(source_font, new_font, unicode_code, from_code, glyph_name, offset)
                    print(' \x1b[32mdone\x1b[0m')
            except (ValueError, TypeError) as e:
                print(f' \x1b[31m(error: {e})\x1b[0m')

    source_font.close()

    # Set font metrics i.e. the dimension-related properties & write the font to file
    FontMetrics.to_font(new_font, dims)
    new_font.generate(output_font)
    new_font.close()

    # Re-open the font, re-write the metrics and re-write
    # the first .generate always changes the metrics but a 2nd attempt always works ¯\_(ツ)_/¯
    font = fontforge.open(output_font)
    FontMetrics.to_font(font, dims)
    font.generate(output_font)

    print(f'Old font metrics\n{dims}')
    print(f'New font metrics\n{FontMetrics.from_font(font)}')
    print(f'\nSaved new font to: {output_font} ({font.familyname})')
    font.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: fontforge -script remap_cp437.py input.ttf output.ttf ENCODING')
        sys.exit(1)

    input_font  = sys.argv[1]
    output_font = sys.argv[2]
    encoding    = sys.argv[3]

    if encoding not in ('CP437', 'ISO'):
        print('Error: encoding must be either CP437 or ISO')
        sys.exit(1)

    remap_font(input_font, output_font, encoding)
