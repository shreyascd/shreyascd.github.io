#!/usr/bin/env python3
from PIL import Image
from rembg import remove
import os, sys

def prep_photo(input_path: str, output_path: str, size: tuple = (200, 200)) -> None:
    print(f"📷 Loading: {input_path}")
    img = Image.open(input_path)
    print("🎨 Removing background...")
    img_no_bg = remove(img)
    print("⚫ Converting to grayscale...")
    img_gray = img_no_bg.convert("L")
    print(f"📐 Resizing to {size}...")
    img_gray = img_gray.resize(size, Image.Resampling.LANCZOS)
    print(f"💾 Saving to {output_path}...")
    img_gray.save(output_path)
    print("✅ Done!")

if __name__ == "__main__":
    input_file = "source-photo.jpg"
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found.")
        sys.exit(1)
    prep_photo(input_file, "prep_photo.png")
