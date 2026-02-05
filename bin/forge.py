#!/usr/bin/env python3

from glob import glob
import sys
from typing import NamedTuple
import fontforge

FONTS = (
    'topazplus_a1200',
    'noodle',
    'microknightplus',
    'mosoul',
    'topazplus_a500',
    'ibm',
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

def find_files(dirpath: str) -> dict[str, dict[str, str | int]]:
    font_paths = {}

    for fpath in glob(f'{dirpath}*.ttf'):
        if 'topazplus' in fpath.lower():
            if 'a500' in fpath.lower():
                font_paths['topazplus_a500'] = {'fpath': fpath, 'offset': 0xE000}
            elif 'a1200' in fpath.lower():
                font_paths['topazplus_a1200'] = {'fpath': fpath, 'offset': 0xE100}
        elif 'soul' in fpath.lower():
            font_paths['mosoul'] = {'fpath': fpath, 'offset': 0xE200}
        elif 'microknightplus' in fpath.lower():
            font_paths['microknightplus'] = {'fpath': fpath, 'offset': 0xE300}
        elif 'noodle' in fpath.lower():
            font_paths['noodle'] = {'fpath': fpath, 'offset': 0xE400}
        elif 'ibm' in fpath.lower():
            font_paths['ibm'] = {'fpath': fpath, 'offset': 0xE500}
        else:
            raise ValueError(f'Unknown font file: {fpath}')
    return font_paths


def calculate_scale_factor(sourceFont, targetFont, reference_chars=[32, 65, 77, 88]):
    'Calculate horizontal scaling factor by comparing glyph widths.'
    source_widths = []
    target_widths = []

    for char_code in reference_chars:
        try:
            if char_code in sourceFont and char_code in targetFont:
                source_widths.append(sourceFont[char_code].width)
                target_widths.append(targetFont[char_code].width)
        except:
            continue

    if source_widths and target_widths:
        avg_source = sum(source_widths) / len(source_widths)
        avg_target = sum(target_widths) / len(target_widths)
        if avg_source > 0:
            ratio = avg_target / avg_source
            # hack
            return ratio * 1.06

    return 1.0

def copyTo(sourceFont, sourceIdx, targetFont, targetIdx, sourceDims=None, targetDims=None, scale_x=1.0):
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
        # Create transformation matrix: [xx, xy, yx, yy, dx, dy]
        matrix = (scale_x, 0, 0, 1, 0, offset_y)
        glyph.transform(matrix)

    print(f', copied: {sourceFont.fontname} {sourceIdx} > {targetIdx}')


print(f'converting {sys.argv[1]} to {sys.argv[2]}')

fonts = find_files(sys.argv[1])
base_font = fontforge.open(fonts['topazplus_a1200']['fpath'])
base_font.encoding = 'UnicodeFull'
base_font.fontname = sys.argv[3]
base_font.familyname = sys.argv[3]

dims = FontMetrics.from_font(base_font)

print(f'Using metrics from: {fonts["topazplus_a1200"]["fpath"]}')
print(f'> {dims.em_size=}, {dims.ascent=}, {dims.descent=}, {dims.os2_typoascent=}, {dims.os2_typodescent=}, {dims.os2_typolinegap=}')

print('Included fonts:')
print('\n'.join([f' - {name}: {info["fpath"]}' for name, info in fonts.items()]))
for font_name in FONTS:
    if font_name not in fonts:
        print(f'skipping missing font: {font_name}')
        continue
    font = fonts.get(font_name)

    print(f'> modifying font: {font_name} - {font['fpath']}')
    source_font = fontforge.open(font['fpath'])
    source_font.encoding = 'UnicodeFull'
    source_dims = FontMetrics.from_font(source_font)
    print(f'> {source_font.em=}, {source_font.ascent=}, {source_font.descent=}, {source_font.os2_typoascent=}, {source_font.os2_typodescent=}, {source_font.os2_typolinegap=}')

    # Calculate horizontal scaling factor dynamically
    scale_x = calculate_scale_factor(source_font, base_font)
    if scale_x != 1.0:
        print(f'> calculated horizontal scale factor: {scale_x:.3f}')

    if font_name == 'topazplus_a1200':
        for i in range(256):
            copyTo(source_font, i, base_font, i, source_dims, dims, scale_x)

    for i in range(256):
        if i == 0x20:
            copyTo(base_font, i, base_font, i + font['offset'], source_dims, dims, scale_x)
        else:
            copyTo(source_font, i, base_font, i + font['offset'], source_dims, dims, scale_x)


FontMetrics.to_font(base_font, dims)

base_font.generate(f'{sys.argv[2]}')
base_font.close()

font = fontforge.open(f'{sys.argv[2]}')
FontMetrics.to_font(font, dims)
font.close()

print(f"\x1b[32m! Wrote combined font to '{sys.argv[2]}' ({sys.argv[3]})\x1b[0m")