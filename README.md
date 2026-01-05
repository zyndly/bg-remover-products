# Product Background Remover

A fast, local background removal tool for product images using the U²-Net deep learning model. All processing happens on your device - your images never leave your computer.

## Features

- **Privacy-focused**: All processing happens locally on your machine
- **Batch processing**: Process multiple images at once
- **U²-Net model**: Uses the same AI technology as professional tools
- **WebP output**: Saves images with transparency in optimized WebP format
- **Product-optimized**: Works excellently with product photography

## Requirements

- Python 3.9 (recommended for best compatibility)
- uv package manager

## Installation

### 1. Install uv (if you haven't already)

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone or download this project

```bash
cd your-project-folder
```

### 3. Create a virtual environment with Python 3.9

```bash
uv venv --python 3.9
```

### 4. Activate the virtual environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
uv pip install rembg pillow onnxruntime
```

## Usage

### Single Image

Process a single product image:

```bash
python remove_bg.py product.jpg
```

Save to a specific output folder:

```bash
python remove_bg.py product.jpg output_folder
```

### Batch Processing

Process all JPG images in a folder:

```bash
python remove_bg.py products/*.jpg
```

Process all images and save to a specific folder:

```bash
python remove_bg.py raw/*.jpg processed
```

Process all PNG files:

```bash
python remove_bg.py images/*.png clean_images
```

### Supported Formats

- JPG/JPEG
- PNG
- BMP
- TIFF

All outputs are saved as WebP with transparency.

## How It Works

1. **U²-Net Model**: The script uses U²-Net (U-squared Network), a state-of-the-art deep learning model specifically designed for salient object detection and background removal.

2. **Local Processing**: On first run, the model (~176MB) is downloaded and cached locally. All subsequent processing happens entirely on your computer.

3. **Batch Optimization**: When processing multiple images, the model loads once and processes all images efficiently, saving time.

4. **WebP Output**: Images are saved in WebP format with transparency, providing excellent quality at smaller file sizes compared to PNG.

## Example Workflow

```bash
# Activate environment
.venv\Scripts\activate

# Process all product photos in 'raw' folder
python remove_bg.py raw/*.jpg clean_products

# Output:
# Found 15 image(s) to process
# Loading U²-Net model...
# Processing images...
# 
# ✓ Processed: product-001.jpg → product-001_no_bg.webp
# ✓ Processed: product-002.jpg → product-002_no_bg.webp
# ...
# Complete! Processed 15 image(s)
```

## Project Structure

```
bg-remover-products/
├── remove_bg.py          # Main script
├── README.md             # This file
├── REQUIREMENTS.txt      # Python dependencies
├── .venv/               # Virtual environment (created during setup)
├── raw/                 # Your original product images (example)
└── processed/           # Output folder (example)
```

## Troubleshooting

### "No module named 'onnxruntime'"

Install the missing dependency:
```bash
uv pip install onnxruntime
```

### Python version issues

Make sure you're using Python 3.9:
```bash
uv venv --python 3.9
```

### Model download fails

The model downloads automatically on first run. If it fails, check your internet connection and try again.

### Images not processing

Ensure your images are in a supported format (JPG, PNG, BMP, TIFF) and the file paths are correct.

## Tips for Best Results

- Use high-resolution product images for best quality
- Ensure good lighting and contrast in original photos
- Products with clear edges work best
- The script works great for e-commerce product photography

## Credits

- Built with [rembg](https://github.com/danielgatis/rembg)
- Uses U²-Net model by Xuebin Qin et al.
- Package management with [uv](https://github.com/astral-sh/uv)

## License

This project is for personal and commercial use. Please check the licenses of the underlying libraries (rembg, U²-Net) for specific terms.