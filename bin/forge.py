#!/usr/bin/env python3

from glob import glob
import os
import sys
from typing import NamedTuple

import fontforge
from laser_prynter.pbar import PBar


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

    def __str__(self):
        s = 'FontMetrics:'
        for field in self._fields:
            s += f'\n  {f"{field}:":<16} = {getattr(self, field)}'
        return s


OFFSETS = {
    # amiga fonts
    'Topaz_a500_v1.0.patched.ttf':      0xE000,
    'TopazPlus_a500_v1.0.patched.ttf':  0xE100,
    'Topaz_a1200_v1.0.patched.ttf':     0xE200,
    'TopazPlus_a1200_v1.0.patched.ttf': 0xE300,
    'MicroKnight_v1.0.patched.ttf':     0xE400,
    'MicroKnightPlus_v1.0.patched.ttf': 0xE500,
    "mO'sOul_v1.0.patched.ttf":         0xE600,
    'P0T-NOoDLE_v1.0.patched.ttf':      0xE700,
    # ibm fonts
    'Ac437_IBM_VGA_9x16.patched.ttf':   0xE800,
}

def find_files(dirpath: str) -> dict[str, dict[str, str | int]]:
    font_paths = {}

    for fpath in glob(f'{dirpath}*.ttf'):
        fname = os.path.basename(fpath)
        if fname in OFFSETS:
            font_paths[fname] = {'fpath': fpath, 'offset': OFFSETS[fname]}
        else:
            raise ValueError(f'Unknown font file: {fpath}, known fonts: {OFFSETS}')
    return font_paths


def copyTo(sourceFont, sourceIdx, targetFont, targetIdx, sourceDims=None, targetDims=None, scale_x=1.0):

    print(f'\x1b[93m{"["+sourceFont.fontname+"]":<22s}\x1b[0m copying: \\u{sourceIdx:<4} > \\u{targetIdx:<6}', end='')

    sourceFont.selection.select(sourceIdx)
    sourceFont.copy()

    if targetIdx not in targetFont:
        targetFont.createChar(targetIdx)

    targetFont.selection.select(targetIdx)
    targetFont.paste()

    glyph = targetFont[targetIdx]

    if sourceIdx in sourceFont:
        oldGlyph = sourceFont[sourceIdx]
        glyph.glyphname = oldGlyph.glyphname

    needs_transform = False
    offset_y = 0

    # Calculate vertical offset if metrics differ
    if sourceDims and targetDims and sourceDims != targetDims:
        offset_y = sourceDims.descent - targetDims.descent
        if offset_y != 0:
            needs_transform = True

    if scale_x != 1.0:
        needs_transform = True

    if needs_transform:
        print(f'- \x1b[3mtransformed [scale_x: {scale_x}, offset_y: {offset_y}]\x1b[0m', end='')
        # Create transformation matrix: [xx, xy, yx, yy, dx, dy]
        matrix = (scale_x, 0, 0, 1, 0, offset_y)
        glyph.transform(matrix)

    print(' \x1b[32mdone\x1b[0m')


print(f'converting {sys.argv[1]} to {sys.argv[2]}')

fonts = find_files(sys.argv[1])
# base_font = fontforge.open(fonts['topazplus_a1200']['fpath'])
base_font = fontforge.open(fonts['TopazPlus_a1200_v1.0.patched.ttf']['fpath'])
base_font.encoding = 'UnicodeFull'
base_font.fontname = sys.argv[3].replace(' ', '')
base_font.familyname = sys.argv[3]

dims = FontMetrics.from_font(base_font)

print(f'Using metrics from: {fonts["TopazPlus_a1200_v1.0.patched.ttf"]["fpath"]}')
print(dims, end='\n\n')

print('Included fonts:')
print('\n'.join([f' - {name}: {info["fpath"]}' for name, info in fonts.items()]))

with PBar(len(OFFSETS)*256) as pbar:
    for fname in OFFSETS:
        if fname not in fonts:
            print(f'skipping missing font: {fname}')
            continue
        font = fonts[fname]

        print("\n".join([
            '-' * 40,
            'modifying',
            f'  fname: {fname}',
        ]))
        source_font = fontforge.open(font['fpath'])
        source_font.encoding = 'UnicodeFull'
        source_dims = FontMetrics.from_font(source_font)
        print(source_dims, end='\n\n')

        # Emprically, I've found that scaling the "Ac437_IBM_VGA_9x16" font by 1.3x
        # produces an identical result to 16colo.rs reference PNGs
        # TODO: update this when adding more IBM fonts
        if 'ibm' in fname:
            scale_x = 1.3
        else:
            scale_x = 1.0
        if fname == 'TopazPlus_a1200_v1.0.patched.ttf':
            for i in range(256):
                copyTo(source_font, i, base_font, i, source_dims, dims, scale_x)
                pbar.update(1)

        for i in range(256):
            if i == 0x20:
                copyTo(base_font, i, base_font, i + font['offset'], source_dims, dims, scale_x)
            else:
                copyTo(source_font, i, base_font, i + font['offset'], source_dims, dims, scale_x)
            pbar.update(1)


FontMetrics.to_font(base_font, dims)

base_font.generate(f'{sys.argv[2]}')
base_font.close()

font = fontforge.open(f'{sys.argv[2]}')
FontMetrics.to_font(font, dims)
font.close()

print(f"\x1b[32m! Wrote combined font to '{sys.argv[2]}' ({sys.argv[3]})\x1b[0m")
