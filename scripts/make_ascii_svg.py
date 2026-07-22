#!/usr/bin/env python3
from PIL import Image
import os

CHARS = " .\`:-=+*cs#%@"

def brightness_to_char(brightness: int) -> str:
    index = min(int((brightness / 255) * (len(CHARS) - 1)), len(CHARS) - 1)
    return CHARS[index]

def image_to_ascii(img_path: str, width: int = 50) -> list:
    img = Image.open(img_path).convert("L")
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = img.getdata()
    ascii_rows = []
    for i in range(height):
        row = ""
        for j in range(width):
            brightness = pixels[i * width + j]
            row += brightness_to_char(brightness)
        ascii_rows.append(row)
    return ascii_rows

def ascii_to_svg(ascii_rows: list, output_path: str = "../ascii.svg") -> None:
    char_width = 8
    char_height = 14
    width = len(ascii_rows[0]) * char_width
    height = len(ascii_rows) * char_height
    
    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        '@keyframes type { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }',
        '.ascii-row { font-family: monospace; font-size: 12px; fill: #0e4429; animation: type 0.8s ease-out forwards; }',
        '</style>',
    ]
    
    for row_idx, row in enumerate(ascii_rows):
        y = row_idx * char_height + 12
        delay = row_idx * 0.05
        svg_lines.append(f'<text class="ascii-row" x="0" y="{y}" style="animation-delay: {delay}s;">{row}</text>')
    
    svg_lines.append('</svg>')
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    print(f"✅ ASCII SVG saved")

if __name__ == "__main__":
    input_file = "prep_photo.png"
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found. Run prep_photo.py first.")
        exit(1)
    ascii_rows = image_to_ascii(input_file, width=50)
    ascii_to_svg(ascii_rows)
