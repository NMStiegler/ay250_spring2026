# PSF Selector - OpenCode Toy Model Project

A toy model project created as an exercise in using OpenCode for AY250 Spring 2026. This project generates synthetic Point Spread Function (PSF) images with white spots and provides tools to validate user click coordinates on these spots.

## Overview

This project consists of three main components:
1. **PSF Generator** - Creates synthetic black and white images with random white circular spots
2. **Click Detector** - Interactive GUI for users to click on white spots in images
3. **Validation Tool** - Validates user clicks against ground truth metadata

## Features

- **Synthetic PSF Generation**: Creates configurable black and white images with random white circles
- **Interactive Click Detection**: Tkinter-based GUI for collecting user click coordinates
- **Comprehensive Validation**: Validates clicks with distance calculations and pass/fail metrics
- **Multiple Output Formats**: Supports terminal output, CSV, and JSON export
- **Configurable Parameters**: Easy to modify image dimensions, spot sizes, and generation count

## Files and Structure

```
OpenCode_test_psf_selector/
├── generate_psfs.py          # Generate synthetic PSF images
├── click_detector.py         # Interactive click detection GUI
├── validate_clicks.py        # Validate clicks against metadata
├── requirements.txt          # Python dependencies
├── example_psfs/             # Generated images and metadata
│   ├── psf_*.bmp            # Generated PSF images
│   └── metadata_*.txt       # Ground truth for each image
└── README.md                 # This file
```

## Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Generate PSF Images

Generate 100 synthetic PSF images with random white spots:

```bash
python generate_psfs.py
```

This will create:
- 100 black and white BMP images (320x320px)
- Corresponding metadata files with center coordinates and radius
- All files saved in `example_psfs/` directory

### 2. Click Detection

Launch the interactive click detector:

```bash
python click_detector.py example_psfs/psf_*.bmp
```

Options:
- `--max-images N`: Limit number of images for testing
- `--output file.csv`: Save coordinates to file instead of terminal

The GUI displays each image and records where you click on the white spot.

### 3. Validate Results

Validate click coordinates against ground truth metadata:

```bash
python validate_clicks.py test_coordinates.txt
```

Options:
- `--format detailed`: Full detailed report (default)
- `--format summary`: Summary statistics only
- `--format csv`: Export to CSV format
- `--format json`: Export to JSON format
- `--metadata-dir path/`: Custom metadata directory
- `--output file.ext`: Output file for CSV/JSON formats

## Example Workflow

1. **Generate test data**:
```bash
python generate_psfs.py
```

2. **Collect user clicks**:
```bash
python click_detector.py example_psfs/psf_*.bmp --output my_clicks.csv
```

3. **Validate accuracy**:
```bash
python validate_clicks.py my_clicks.csv --format detailed
```

## Configuration

The PSF generator can be customized by modifying these parameters in `generate_psfs.py`:

- `IMAGE_SIZE`: Image dimensions (default: 320px)
- `BORDER_SIZE`: Border margin for spots (default: 10px)
- `NUM_IMAGES`: Number of images to generate (default: 100)
- `MIN_RADIUS` / `MAX_RADIUS`: Spot radius range (default: 5-10px)
- `OUTPUT_FOLDER`: Output directory (default: "example_psfs")

## Technical Details

### Image Generation
- Black background (0) with white circular spots (255)
- Spots placed randomly within border constraints
- Each spot has recorded center coordinates and radius
- Images saved as BMP format for simplicity

### Click Detection
- Tkinter GUI with canvas display
- Automatic image scaling for display (max 600x600)
- Coordinate conversion to original image resolution
- Progress tracking and early exit options

### Validation Algorithm
- Euclidean distance calculation between click and spot center
- Pass/fail determination based on radius threshold
- Comprehensive statistics and error handling
- Multiple export formats for analysis

## Dependencies

- **numpy**: Array operations and distance calculations
- **Pillow (PIL)**: Image generation and display
- **tkinter**: GUI framework (included with Python)

## Educational Purpose

This toy model demonstrates:
- Image processing and generation
- Interactive GUI development with Tkinter
- Coordinate validation and distance calculations
- File I/O and data export in multiple formats
- Command-line argument parsing
- Error handling and user interaction

Created as an exercise for AY250 Spring 2026 to showcase OpenCode's capabilities in generating and documenting Python projects.