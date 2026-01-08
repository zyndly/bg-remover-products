#!/usr/bin/env python3
"""
Add Background to Product Images
Adds a background image to transparent product images and saves as WebP.
Supports batch processing and automatic centering/sizing.
"""

from PIL import Image
import sys
import os
import glob

def add_background(product_path, background_path, output_dir=None, resize_product=True, center=True):
    """
    Add a background image to a transparent product image.
    
    Args:
        product_path: Path to product image (with transparency)
        background_path: Path to background image
        output_dir: Directory for output (optional)
        resize_product: If True, resize product to fit nicely on background
        center: If True, center the product on the background
    """
    try:
        # Open images
        product = Image.open(product_path).convert("RGBA")
        background = Image.open(background_path).convert("RGB")
        
        # Resize product if requested (80% of background size max)
        if resize_product:
            bg_width, bg_height = background.size
            prod_width, prod_height = product.size
            
            # Calculate scale to fit product nicely (80% max of background)
            max_width = int(bg_width * 0.8)
            max_height = int(bg_height * 0.8)
            
            # Scale down if product is larger
            scale = min(max_width / prod_width, max_height / prod_height)
            if scale < 1:
                new_width = int(prod_width * scale)
                new_height = int(prod_height * scale)
                product = product.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a copy of background to paste on
        result = background.copy()
        
        # Calculate position (center by default)
        if center:
            prod_width, prod_height = product.size
            bg_width, bg_height = background.size
            x = (bg_width - prod_width) // 2
            y = (bg_height - prod_height) // 2
        else:
            x, y = 0, 0
        
        # Paste product onto background using alpha channel as mask
        result.paste(product, (x, y), product)
        
        # Determine output path
        base_name = os.path.splitext(os.path.basename(product_path))[0]
        # Remove '_no_bg' suffix if present
        if base_name.endswith('_no_bg'):
            base_name = base_name[:-6]
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{base_name}_with_bg.webp")
        else:
            product_dir = os.path.dirname(product_path) or "."
            output_path = os.path.join(product_dir, f"{base_name}_with_bg.webp")
        
        # Save as WebP
        result.save(output_path, 'WEBP', quality=95)
        
        print(f"✓ Processed: {os.path.basename(product_path)} → {os.path.basename(output_path)}")
        
        return output_path
        
    except Exception as e:
        print(f"✗ Error processing {product_path}: {e}")
        return None

def process_batch(product_pattern, background_path, output_dir=None):
    """
    Process multiple product images with the same background.
    
    Args:
        product_pattern: File pattern for products (e.g., "products/*.webp")
        background_path: Path to background image
        output_dir: Directory for output images
    """
    # Find matching files
    files = glob.glob(product_pattern)
    
    if not files:
        print(f"✗ No files found matching: {product_pattern}")
        sys.exit(1)
    
    if not os.path.exists(background_path):
        print(f"✗ Background image not found: {background_path}")
        sys.exit(1)
    
    print(f"Found {len(files)} product image(s) to process")
    print(f"Using background: {background_path}")
    print("Processing images...\n")
    
    successful = 0
    failed = 0
    
    for file_path in files:
        result = add_background(file_path, background_path, output_dir)
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
    if len(sys.argv) < 3:
        print("Add Background to Product Images")
        print("=" * 50)
        print("\nUsage:")
        print("  Single file:  python add_bg.py <product_image> <background_image> [output_dir]")
        print("  Batch mode:   python add_bg.py <product_pattern> <background_image> [output_dir]")
        print("\nExamples:")
        print("  python add_bg.py product_no_bg.webp white_bg.jpg")
        print("  python add_bg.py product_no_bg.webp white_bg.jpg final")
        print("  python add_bg.py \"processed/*_no_bg.webp\" backgrounds/white.jpg final")
        print("  python add_bg.py \"clean/*.webp\" backgrounds/gradient.png output")
        print("\nSupported formats: WebP, JPG, PNG, BMP")
        sys.exit(1)
    
    product_input = sys.argv[1]
    background_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Check if background exists
    if not os.path.exists(background_path):
        print(f"✗ Error: Background image '{background_path}' not found.")
        sys.exit(1)
    
    # Check if it's a pattern or single file
    if any(char in product_input for char in ['*', '?', '[', ']']):
        # Batch processing
        process_batch(product_input, background_path, output_dir)
    else:
        # Single file
        if not os.path.exists(product_input):
            print(f"✗ Error: Product image '{product_input}' not found.")
            sys.exit(1)
        
        print("Processing image...\n")
        
        result = add_background(product_input, background_path, output_dir)
        
        if result:
            print(f"\n✓ Success! Saved to: {result}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()