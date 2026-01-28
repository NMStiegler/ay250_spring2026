#!/usr/bin/env python3
"""
Generate 100 black and white images with random white spots.
Images are square with customizable dimensions and border constraints.
"""

import os
import random
import numpy as np
from PIL import Image

# ============ CONFIGURABLE PARAMETERS ============
IMAGE_SIZE = 320          # Square image dimensions in pixels
BORDER_SIZE = 10          # Border margin where circles won't appear
NUM_IMAGES = 100          # Number of images to generate
OUTPUT_FOLDER = "example_psfs"  # Folder to save images
MIN_RADIUS = 5            # Minimum radius of white spots
MAX_RADIUS = 10           # Maximum radius of white spots
IMAGE_FORMAT = "BMP"      # Image format (BMP, PNG, JPEG, etc.)

def create_output_directory():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created directory: {OUTPUT_FOLDER}")

def generate_single_image(image_number):
    """Generate a single black and white image with a random white spot."""
    # Create black background
    img_array = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=np.uint8)
    
    # Calculate valid positioning area (considering border and max radius)
    min_pos = BORDER_SIZE + MAX_RADIUS
    max_pos = IMAGE_SIZE - BORDER_SIZE - MAX_RADIUS
    
    # Generate random center coordinates within valid area
    center_x = random.randint(min_pos, max_pos)
    center_y = random.randint(min_pos, max_pos)
    
    # Generate random radius
    radius = random.randint(MIN_RADIUS, MAX_RADIUS)
    
    # Create white spot using distance calculation
    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if distance <= radius:
                img_array[y, x] = 255  # White color
    
    # Convert to PIL Image
    img = Image.fromarray(img_array, mode='L')
    
    return img, center_x, center_y, radius

def save_image_metadata(image_number, center_x, center_y, radius):
    """Save metadata about the generated image."""
    metadata_file = os.path.join(OUTPUT_FOLDER, f"metadata_{image_number:03d}.txt")
    with open(metadata_file, 'w') as f:
        f.write(f"Image: psf_{image_number:03d}.bmp\n")
        f.write(f"Center X: {center_x}\n")
        f.write(f"Center Y: {center_y}\n")
        f.write(f"Radius: {radius}\n")

def generate_all_images():
    """Generate all images with progress indicator."""
    create_output_directory()
    
    generated_count = 0
    skipped_count = 0
    
    for i in range(1, NUM_IMAGES + 1):
        filename = f"psf_{i:03d}.bmp"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename} (already exists)")
            skipped_count += 1
            continue
        
        # Generate and save image
        try:
            img, center_x, center_y, radius = generate_single_image(i)
            img.save(filepath, format=IMAGE_FORMAT)
            save_image_metadata(i, center_x, center_y, radius)
            print(f"Generated {filename} (center: {center_x}, {center_y}, radius: {radius})")
            generated_count += 1
        except Exception as e:
            print(f"Error generating {filename}: {e}")
    
    print(f"\nGeneration complete!")
    print(f"Generated: {generated_count} images")
    print(f"Skipped: {skipped_count} images")
    print(f"Total: {NUM_IMAGES} images")

def validate_parameters():
    """Validate that parameters are compatible."""
    if BORDER_SIZE * 2 >= IMAGE_SIZE:
        raise ValueError("Border size is too large for the image size")
    
    if MIN_RADIUS > MAX_RADIUS:
        raise ValueError("Minimum radius cannot be larger than maximum radius")
    
    if BORDER_SIZE + MAX_RADIUS >= IMAGE_SIZE // 2:
        print("Warning: Border and radius combination may limit positioning area")

if __name__ == "__main__":
    try:
        validate_parameters()
        print(f"Generating {NUM_IMAGES} images ({IMAGE_SIZE}x{IMAGE_SIZE}px)")
        print(f"Border: {BORDER_SIZE}px, Spot radius: {MIN_RADIUS}-{MAX_RADIUS}px")
        print(f"Output folder: {OUTPUT_FOLDER}")
        print("-" * 50)
        generate_all_images()
    except Exception as e:
        print(f"Error: {e}")