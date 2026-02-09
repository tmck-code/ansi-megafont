#!/usr/bin/env python3
"""
Generate markdown documentation and character images for all fonts in ANSICombined.ttf.
This script extracts glyphs from the combined font file and creates documentation pages
with character tables and individual PNG images for each glyph.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import unicodedata

# Font metadata - sourced from forge.py
FONTS = {
    'Topaz_A500': {
        'offset': 0xE000,
        'range_start': 0xE000,
        'range_end': 0xE0FF,
        'display_name': 'Topaz A500',
        'description': 'Classic Amiga 500 Topaz font',
        'folder_name': 'Topaz_A500'
    },
    'Topaz_Plus_A500': {
        'offset': 0xE100,
        'range_start': 0xE100,
        'range_end': 0xE1FF,
        'display_name': 'Topaz Plus A500',
        'description': 'Enhanced Amiga 500 Topaz font',
        'folder_name': 'Topaz_Plus_A500'
    },
    'Topaz_A1200': {
        'offset': 0xE200,
        'range_start': 0xE200,
        'range_end': 0xE2FF,
        'display_name': 'Topaz A1200',
        'description': 'Classic Amiga 1200 Topaz font',
        'folder_name': 'Topaz_A1200'
    },
    'Topaz_Plus_A1200': {
        'offset': 0xE300,
        'range_start': 0xE300,
        'range_end': 0xE3FF,
        'display_name': 'Topaz Plus A1200',
        'description': 'Enhanced Amiga 1200 Topaz font',
        'folder_name': 'Topaz_Plus_A1200'
    },
    'MicroKnight': {
        'offset': 0xE400,
        'range_start': 0xE400,
        'range_end': 0xE4FF,
        'display_name': 'MicroKnight',
        'description': 'MicroKnight bitmap font',
        'folder_name': 'MicroKnight'
    },
    'MicroKnight_Plus': {
        'offset': 0xE500,
        'range_start': 0xE500,
        'range_end': 0xE5FF,
        'display_name': 'MicroKnight Plus',
        'description': 'Enhanced MicroKnight font with extended characters',
        'folder_name': 'MicroKnight_Plus'
    },
    'mOsOul': {
        'offset': 0xE600,
        'range_start': 0xE600,
        'range_end': 0xE6FF,
        'display_name': "mO'sOul",
        'description': "mO'sOul ANSI font",
        'folder_name': 'mOsOul'
    },
    'P0T_NOoDLE': {
        'offset': 0xE700,
        'range_start': 0xE700,
        'range_end': 0xE7FF,
        'display_name': 'P0T-NOoDLE',
        'description': 'P0T-NOoDLE ANSI font',
        'folder_name': 'P0T_NOoDLE'
    },
    'IBM_VGA_9x16': {
        'offset': 0xE800,
        'range_start': 0xE800,
        'range_end': 0xE8FF,
        'display_name': 'IBM VGA 9x16',
        'description': 'Classic IBM VGA font (9x16)',
        'folder_name': 'IBM_VGA_9x16'
    },
}

# Control character names for 0x00-0x1F
CONTROL_CHARS = {
    0x00: 'NUL', 0x01: 'SOH', 0x02: 'STX', 0x03: 'ETX',
    0x04: 'EOT', 0x05: 'ENQ', 0x06: 'ACK', 0x07: 'BEL',
    0x08: 'BS',  0x09: 'HT',  0x0A: 'LF',  0x0B: 'VT',
    0x0C: 'FF',  0x0D: 'CR',  0x0E: 'SO',  0x0F: 'SI',
    0x10: 'DLE', 0x11: 'DC1', 0x12: 'DC2', 0x13: 'DC3',
    0x14: 'DC4', 0x15: 'NAK', 0x16: 'SYN', 0x17: 'ETB',
    0x18: 'CAN', 0x19: 'EM',  0x1A: 'SUB', 0x1B: 'ESC',
    0x1C: 'FS',  0x1D: 'GS',  0x1E: 'RS',  0x1F: 'US',
    0x7F: 'DEL', 0x20: 'SP'
}


def get_char_label(codepoint):
    """Get a descriptive label for a character."""
    offset_char = codepoint & 0xFF
    
    # Check control characters
    if offset_char in CONTROL_CHARS:
        return CONTROL_CHARS[offset_char]
    
    # For printable characters, try to get the actual character
    try:
        # Try to get the character from the original unicode codepoint
        char = chr(codepoint)
        if char.isprintable() and not char.isspace():
            return char
        # For extended range, try the offset character
        if codepoint >= 0xE000:
            char = chr(offset_char)
            if char.isprintable() and not char.isspace():
                return char
    except:
        pass
    
    return ''


def render_glyph_image(font_path, codepoint, output_path, size=64, scale=4):
    """Render a single glyph to a PNG image with improved visibility."""
    try:
        # Use larger size for rendering, then scale down for better quality
        render_size = size * scale
        font = ImageFont.truetype(font_path, render_size)
        
        # Create image with padding
        padding = render_size // 4
        img_width = render_size + padding * 2
        img_height = render_size + padding * 2
        
        # Create white background
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Get the character
        char = chr(codepoint)
        
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (img_width - text_width) // 2 - bbox[0]
        y = (img_height - text_height) // 2 - bbox[1]
        
        # Draw the character in black
        draw.text((x, y), char, fill='black', font=font)
        
        # Scale down for final output
        final_size = (size + padding // 2, size + padding // 2)
        img = img.resize(final_size, Image.Resampling.LANCZOS)
        
        # Save the image
        img.save(output_path, 'PNG', optimize=True)
        return True
        
    except Exception as e:
        print(f"Error rendering U+{codepoint:04X}: {e}")
        return False


def generate_markdown_table(font_info, font_key):
    """Generate the markdown table for a font."""
    range_start = font_info['range_start']
    range_end = font_info['range_end']
    folder_name = font_info['folder_name']
    
    lines = []
    
    # Start table
    lines.append('<table class="font-table">')
    lines.append('<thead>')
    lines.append('<tr>')
    lines.append('<th></th>')
    for i in range(16):
        lines.append(f'<th>{i:X}</th>')
    lines.append('</tr>')
    lines.append('</thead>')
    lines.append('<tbody>')
    
    # Generate rows
    for row in range(16):
        lines.append('<tr>')
        lines.append(f'<td><strong>{row:X}</strong></td>')
        
        for col in range(16):
            codepoint = range_start + (row * 16) + col
            if codepoint <= range_end:
                unicode_str = f"U+{codepoint:04X}"
                img_path = f"/docs/img/{folder_name}/{unicode_str}.png"
                label = get_char_label(codepoint)
                
                lines.append(f'<td><img src="{img_path}" alt=""><br>{label}<br><code>{unicode_str}</code></td>')
            else:
                lines.append('<td></td>')
        
        lines.append('</tr>')
    
    lines.append('</tbody>')
    lines.append('</table>')
    
    return '\n'.join(lines)


def generate_markdown_file(font_key, font_info, output_dir):
    """Generate a complete markdown file for a font."""
    display_name = font_info['display_name']
    range_start = font_info['range_start']
    range_end = font_info['range_end']
    description = font_info.get('description', '')
    
    lines = []
    lines.append(f'# {display_name}')
    lines.append('')
    
    # Special handling for base font
    if range_start == 0x0000:
        lines.append(f'> **Unicode Range:** U+{range_start:04X} - U+{range_end:04X} (Standard positions)')
    else:
        lines.append(f'> **Unicode Range:** U+{range_start:04X} - U+{range_end:04X}')
    
    if description:
        lines.append(f'>')
        lines.append(f'> {description}')
    
    lines.append('')
    
    # Add the table
    table = generate_markdown_table(font_info, font_key)
    lines.append(table)
    
    content = '\n'.join(lines)
    
    # Write to file
    # Convert display name to filename
    if 'Base Font' in display_name:
        filename = 'Topaz_Plus_A1200.md'
    else:
        filename = display_name.replace(' ', '_').replace("'", '').replace('(', '').replace(')', '').replace('-', '_')
        filename = f'{filename}.md'
    
    output_path = output_dir / filename
    output_path.write_text(content)
    print(f"Generated {output_path}")


def generate_all_images(font_path, docs_dir):
    """Generate all glyph images for all fonts."""
    if not os.path.exists(font_path):
        print(f"Error: Font file not found: {font_path}")
        return False
    
    img_dir = docs_dir / 'img'
    img_dir.mkdir(exist_ok=True)
    
    for font_key, font_info in FONTS.items():
        print(f"\nGenerating images for {font_info['display_name']}...")
        
        folder_name = font_info['folder_name']
        font_img_dir = img_dir / folder_name
        font_img_dir.mkdir(exist_ok=True)
        
        range_start = font_info['range_start']
        range_end = font_info['range_end']
        
        for codepoint in range(range_start, range_end + 1):
            unicode_str = f"U+{codepoint:04X}"
            output_path = font_img_dir / f"{unicode_str}.png"
            
            if render_glyph_image(font_path, codepoint, output_path):
                if (codepoint - range_start) % 16 == 0:
                    print(f"  Generated {codepoint - range_start + 1}/{range_end - range_start + 1} images...")
    
    return True


def generate_all_docs(docs_dir):
    """Generate all markdown documentation files."""
    print("\nGenerating markdown documentation...")
    
    for font_key, font_info in FONTS.items():
        print(f"  Generating docs for {font_info['display_name']}...")
        generate_markdown_file(font_key, font_info, docs_dir)


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_docs.py <path_to_ANSICombined.ttf>")
        sys.exit(1)
    
    font_path = sys.argv[1]
    
    # Determine docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    print(f"Font file: {font_path}")
    print(f"Documentation directory: {docs_dir}")
    print(f"Generating documentation for {len(FONTS)} fonts...")
    
    # Generate images for all fonts
    if not generate_all_images(font_path, docs_dir):
        sys.exit(1)
    
    # Generate markdown files
    generate_all_docs(docs_dir)
    
    print("\n✓ Documentation generation complete!")
    print(f"  - Images: {docs_dir / 'img'}")
    print(f"  - Markdown: {docs_dir}")


if __name__ == '__main__':
    main()
