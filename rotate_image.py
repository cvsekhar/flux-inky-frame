#!/usr/bin/env python3
"""
Rotate image 90 degrees counterclockwise (left) and save as JPG
Usage: python rotate_image.py image.png image.jpg
"""

from PIL import Image
import sys

def rotate_and_convert(input_path, output_path, quality=70):
    """
    Rotate image 90 degrees left and save as JPG
    
    Args:
        input_path: Path to input PNG file
        output_path: Path to output JPG file
        quality: JPG quality (0-100), default 70
    """
    # Open the image
    img = Image.open(input_path)
    
    # Rotate 90 degrees counterclockwise (left)
    # Negative angle rotates counterclockwise
    rotated = img.rotate(90, expand=True)
    
    # Convert RGBA to RGB if necessary (PNG might have alpha channel)
    if rotated.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        rgb_img = Image.new('RGB', rotated.size, (255, 255, 255))
        rgb_img.paste(rotated, mask=rotated.split()[-1] if rotated.mode == 'RGBA' else None)
        rotated = rgb_img
    
    # Save as JPG with specified quality
    rotated.save(output_path, 'JPEG', quality=quality, optimize=True)
    print(f"Rotated image saved to {output_path}")
    print(f"Original size: {img.size} -> New size: {rotated.size}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rotate_image.py <input.png> [output.jpg]")
        print("Example: python rotate_image.py image.png image.jpg")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "image.jpg"
    
    rotate_and_convert(input_file, output_file)
