#!/usr/bin/env python3
"""
Product Background Remover with U²-Net
Removes background from product images using U²-Net model and saves as WebP.
Supports batch processing of multiple images.
"""

from rembg import remove, new_session
from PIL import Image
import sys
import os
import glob

def remove_background(input_path, output_dir=None, session=None):
    """
    Remove background from a product image using U²-Net and save as WebP.
    
    Args:
        input_path: Path to input image
        output_dir: Directory for output (optional, defaults to same directory)
        session: Reusable model session for batch processing
    """
    try:
        # Open input image
        input_img = Image.open(input_path)
        
        # Remove background
        output_img = remove(input_img, session=session)
        
        # Determine output path
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{base_name}_no_bg.webp")
        else:
            input_dir = os.path.dirname(input_path) or "."
            output_path = os.path.join(input_dir, f"{base_name}_no_bg.webp")
        
        # Save as WebP with transparency
        output_img.save(output_path, 'WEBP', quality=95, lossless=False)
        
        print(f"✓ Processed: {os.path.basename(input_path)} → {os.path.basename(output_path)}")
        
        return output_path
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return None

def process_batch(input_pattern, output_dir=None):
    """
    Process multiple images matching a pattern.
    
    Args:
        input_pattern: File pattern (e.g., "products/*.jpg")
        output_dir: Directory for output images
    """
    # Find matching files
    files = glob.glob(input_pattern)
    
    if not files:
        print(f"✗ No files found matching: {input_pattern}")
        sys.exit(1)
    
    print(f"Found {len(files)} image(s) to process")
    print("Loading U²-Net model...")
    
    # Create session once for all images (faster for batch processing)
    session = new_session("u2net")
    
    print("Processing images...\n")
    
    successful = 0
    failed = 0
    
    for file_path in files:
        result = remove_background(file_path, output_dir, session)
        if result:
            successful += 1
        else:
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Complete! Processed {successful} image(s)")
    if failed > 0:
        print(f"Failed: {failed} image(s)")

def main():
    """Main function to handle command line usage."""
    if len(sys.argv) < 2:
        print("Product Background Remover with U²-Net")
        print("=" * 50)
        print("\nUsage:")
        print("  Single file:  python remove_bg.py <image_file> [output_dir]")
        print("  Batch mode:   python remove_bg.py <pattern> [output_dir]")
        print("\nExamples:")
        print("  python remove_bg.py product.jpg")
        print("  python remove_bg.py product.jpg output_folder")
        print("  python remove_bg.py products/*.jpg")
        print("  python remove_bg.py products/*.jpg clean_images")
        print("  python remove_bg.py \"images/**/*.png\"")
        print("\nSupported formats: JPG, PNG, JPEG, BMP, TIFF")
        sys.exit(1)
    
    input_pattern = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if it's a pattern or single file
    if any(char in input_pattern for char in ['*', '?', '[', ']']):
        # Batch processing
        process_batch(input_pattern, output_dir)
    else:
        # Single file
        if not os.path.exists(input_pattern):
            print(f"✗ Error: File '{input_pattern}' not found.")
            sys.exit(1)
        
        print("Loading U²-Net model...")
        session = new_session("u2net")
        print("Processing image...\n")
        
        result = remove_background(input_pattern, output_dir, session)
        
        if result:
            print(f"\n✓ Success! Saved to: {result}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()