#!/usr/bin/env python3
"""
Click Detector Script
Displays images one at a time and records user click coordinates on white spots.
"""

import os
import sys
import glob
import argparse
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox


class ClickDetector:
    def __init__(self, image_pattern, max_images=None, output_file=None):
        self.image_pattern = image_pattern
        self.max_images = max_images
        self.output_file = output_file
        self.coordinates = []
        self.current_image_index = 0
        self.current_image_path = None
        self.click_coords = None
        
        # Find and sort images
        self.image_files = self.find_images()
        if not self.image_files:
            print(f"No images found matching pattern: {image_pattern}")
            sys.exit(1)
        
        # Apply max_images limit if specified
        if max_images:
            self.image_files = self.image_files[:max_images]
        
        print(f"Found {len(self.image_files)} images to process")
        
        # Initialize tkinter
        self.root = tk.Tk()
        self.root.title("Click Detector")
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Create UI elements
        self.setup_ui()
        
    def find_images(self):
        """Find images matching the pattern and sort numerically."""
        import re
        
        # Find all matching files
        files = glob.glob(self.image_pattern)
        
        # Sort numerically (extract numbers from filenames)
        def extract_number(filename):
            match = re.search(r'(\d+)', filename)
            return int(match.group(1)) if match else 0
        
        files.sort(key=extract_number)
        return files
    
    def setup_ui(self):
        """Setup the tkinter UI."""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Canvas for image display
        self.canvas = tk.Canvas(main_frame, bg="gray")
        self.canvas.pack()
        
        # Instructions label
        instructions = tk.Label(main_frame, 
                               text="Click on the white spot. Close window to exit early.",
                               font=("Arial", 10))
        instructions.pack(pady=5)
        
        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def load_image(self, image_path):
        """Load an image and display it on the canvas."""
        try:
            # Open image with PIL
            pil_image = Image.open(image_path)
            
            # Store original size for coordinate conversion
            self.original_width, self.original_height = pil_image.size
            
            # Resize for display if needed (max 600x600)
            max_display_size = 600
            if pil_image.size[0] > max_display_size or pil_image.size[1] > max_display_size:
                ratio = min(max_display_size / pil_image.size[0], 
                           max_display_size / pil_image.size[1])
                new_size = (int(pil_image.size[0] * ratio), 
                           int(pil_image.size[1] * ratio))
                pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            self.photo = ImageTk.PhotoImage(pil_image)
            
            # Update canvas size and display image
            self.canvas.config(width=pil_image.size[0], height=pil_image.size[1])
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # Calculate scaling factor for coordinate conversion
            self.scale_x = self.original_width / pil_image.size[0]
            self.scale_y = self.original_height / pil_image.size[1]
            
            return True
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return False
    
    def on_canvas_click(self, event):
        """Handle mouse click on canvas."""
        # Convert canvas coordinates to original image coordinates
        original_x = int(event.x * self.scale_x)
        original_y = int(event.y * self.scale_y)
        
        # Validate coordinates are within image bounds
        if (0 <= original_x < self.original_width and 
            0 <= original_y < self.original_height):
            
            # Store the coordinates
            self.click_coords = (original_x, original_y)
            
            # Record the result
            filename = os.path.basename(self.current_image_path)
            result = f"{filename},{original_x},{original_y}"
            self.coordinates.append(result)
            
            # Display result
            print(f"Clicked {filename}: ({original_x}, {original_y})")
            
            # Move to next image
            self.show_next_image()
    
    def show_next_image(self):
        """Display the next image in the sequence."""
        if self.current_image_index < len(self.image_files):
            self.current_image_path = self.image_files[self.current_image_index]
            filename = os.path.basename(self.current_image_path)
            
            # Update status
            progress = f"{self.current_image_index + 1}/{len(self.image_files)}"
            self.status_label.config(text=f"Image {progress}: {filename}")
            self.root.title(f"Click Detector - Image {progress}: {filename}")
            
            # Load and display image
            if self.load_image(self.current_image_path):
                self.current_image_index += 1
                self.click_coords = None
            else:
                # Skip to next image if loading failed
                self.current_image_index += 1
                self.show_next_image()
        else:
            # All images processed
            self.finish_session()
    
    def on_window_close(self):
        """Handle window close event."""
        if messagebox.askyesno("Exit Early", 
                             "Do you want to exit and save current results?"):
            self.finish_session()
        else:
            # Keep the window open
            pass
    
    def finish_session(self):
        """Save results and exit."""
        if self.coordinates:
            if self.output_file:
                # Save to file
                try:
                    with open(self.output_file, 'w') as f:
                        f.write('\n'.join(self.coordinates))
                    print(f"\nResults saved to: {self.output_file}")
                except Exception as e:
                    print(f"Error saving to file {self.output_file}: {e}")
                    # Fallback to terminal output
                    print("\nResults (terminal output):")
                    for coord in self.coordinates:
                        print(coord)
            else:
                # Display to terminal
                print("\nResults:")
                for coord in self.coordinates:
                    print(coord)
            
            print(f"\nSession complete. Processed {len(self.coordinates)} images.")
        else:
            print("\nNo coordinates recorded.")
        
        # Close the tkinter window
        self.root.destroy()
    
    def run(self):
        """Start the click detection session."""
        if not self.image_files:
            print("No images to process.")
            return
        
        # Start with the first image
        self.show_next_image()
        
        # Start the tkinter event loop
        self.root.mainloop()


def main():
    """Main function to handle command line arguments and start the detector."""
    parser = argparse.ArgumentParser(
        description="Click on white spots in images and record coordinates."
    )
    
    parser.add_argument(
        "image_pattern",
        help="Image pattern to process (e.g., 'psf_*.bmp')"
    )
    
    parser.add_argument(
        "--max-images",
        type=int,
        help="Maximum number of images to process (for testing)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file for coordinates (default: print to terminal)"
    )
    
    args = parser.parse_args()
    
    # Validate image pattern
    if not args.image_pattern:
        print("Error: Please provide an image pattern.")
        sys.exit(1)
    
    # Create and run the click detector
    detector = ClickDetector(
        image_pattern=args.image_pattern,
        max_images=args.max_images,
        output_file=args.output
    )
    
    detector.run()


if __name__ == "__main__":
    main()