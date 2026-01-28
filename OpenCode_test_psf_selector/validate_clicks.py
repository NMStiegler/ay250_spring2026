#!/usr/bin/env python3
"""
PSF Validation Script
Validates user click coordinates against ground truth metadata to determine if clicks landed inside white circles.
"""

import os
import sys
import argparse
import json
import csv
import math
from typing import Dict, List, Tuple, Optional


class ValidationResult:
    """Stores validation result for a single image."""
    def __init__(self, filename: str, click_x: int, click_y: int, 
                 center_x: Optional[int] = None, center_y: Optional[int] = None,
                 radius: Optional[int] = None, distance: Optional[float] = None,
                 passed: Optional[bool] = None, error: Optional[str] = None):
        self.filename = filename
        self.click_x = click_x
        self.click_y = click_y
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.distance = distance
        self.passed = passed
        self.error = error


class PSFValidator:
    def __init__(self, coordinates_file: str, metadata_dir: str = "example_psfs/"):
        self.coordinates_file = coordinates_file
        self.metadata_dir = metadata_dir
        self.results: List[ValidationResult] = []
        self.total_images = 0
        self.validated_images = 0
        self.passed_images = 0
        self.failed_images = 0
        self.missing_metadata = 0
        
    def load_click_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Load click coordinates from CSV file."""
        coordinates = {}
        
        if not os.path.exists(self.coordinates_file):
            raise FileNotFoundError(f"Coordinates file not found: {self.coordinates_file}")
        
        with open(self.coordinates_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    parts = line.split(',')
                    if len(parts) != 3:
                        print(f"Warning: Invalid format on line {line_num}: {line}")
                        continue
                    
                    filename = parts[0].strip()
                    click_x = int(parts[1].strip())
                    click_y = int(parts[2].strip())
                    
                    coordinates[filename] = (click_x, click_y)
                    
                except ValueError as e:
                    print(f"Warning: Invalid coordinates on line {line_num}: {line}")
                    continue
                except Exception as e:
                    print(f"Warning: Error parsing line {line_num}: {e}")
                    continue
        
        self.total_images = len(coordinates)
        return coordinates
    
    def load_metadata(self, filename: str) -> Tuple[int, int, int]:
        """Load metadata for a specific image."""
        # Extract image number from filename (e.g., psf_001.bmp -> 001)
        import re
        match = re.search(r'psf_(\d+)', filename)
        if not match:
            raise ValueError(f"Cannot extract image number from filename: {filename}")
        
        image_number = match.group(1)
        metadata_file = os.path.join(self.metadata_dir, f"metadata_{image_number}.txt")
        
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
        
        with open(metadata_file, 'r') as f:
            center_x = None
            center_y = None
            radius = None
            
            for line in f:
                line = line.strip()
                if line.startswith("Center X:"):
                    center_x = int(line.split(':')[1].strip())
                elif line.startswith("Center Y:"):
                    center_y = int(line.split(':')[1].strip())
                elif line.startswith("Radius:"):
                    radius = int(line.split(':')[1].strip())
            
            if center_x is None or center_y is None or radius is None:
                raise ValueError(f"Invalid metadata format in: {metadata_file}")
            
            return center_x, center_y, radius
    
    def calculate_distance(self, click_x: int, click_y: int, center_x: int, center_y: int) -> float:
        """Calculate Euclidean distance between click and center."""
        return math.sqrt((click_x - center_x)**2 + (click_y - center_y)**2)
    
    def is_inside_circle(self, distance: float, radius: int) -> bool:
        """Check if click is inside the circle."""
        return distance <= radius
    
    def ask_user_continue(self, filename: str, error_msg: str) -> bool:
        """Ask user whether to continue when encountering errors."""
        print(f"\nError processing {filename}: {error_msg}")
        while True:
            response = input("Continue processing other files? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def validate_all(self) -> List[ValidationResult]:
        """Validate all click coordinates against metadata."""
        coordinates = self.load_click_coordinates()
        
        for filename, (click_x, click_y) in coordinates.items():
            try:
                # Load metadata
                center_x, center_y, radius = self.load_metadata(filename)
                
                # Calculate distance and validate
                distance = self.calculate_distance(click_x, click_y, center_x, center_y)
                passed = self.is_inside_circle(distance, radius)
                
                # Create result
                result = ValidationResult(
                    filename=filename,
                    click_x=click_x,
                    click_y=click_y,
                    center_x=center_x,
                    center_y=center_y,
                    radius=radius,
                    distance=distance,
                    passed=passed
                )
                
                # Update counters
                self.validated_images += 1
                if passed:
                    self.passed_images += 1
                else:
                    self.failed_images += 1
                
            except Exception as e:
                result = ValidationResult(
                    filename=filename,
                    click_x=click_x,
                    click_y=click_y,
                    error=str(e)
                )
                
                # Handle missing metadata separately
                if "Metadata file not found" in str(e):
                    self.missing_metadata += 1
                
                # Ask user whether to continue
                if not self.ask_user_continue(filename, str(e)):
                    break
            
            self.results.append(result)
        
        return self.results
    
    def print_detailed_results(self):
        """Print detailed validation results (default format)."""
        print("=" * 40)
        print("PSF Validation Results")
        print("=" * 40)
        print(f"Total Images: {self.total_images}")
        print(f"Validated: {self.validated_images}")
        print(f"Missing Metadata: {self.missing_metadata}")
        
        if self.validated_images > 0:
            print(f"Passed: {self.passed_images} ({self.passed_images/self.validated_images*100:.1f}%)")
            print(f"Failed: {self.failed_images} ({self.failed_images/self.validated_images*100:.1f}%)")
            
            # Distance statistics
            distances = [r.distance for r in self.results if r.distance is not None]
            if distances:
                print(f"Average Distance: {sum(distances)/len(distances):.2f}px")
                print(f"Min Distance: {min(distances):.2f}px")
                print(f"Max Distance: {max(distances):.2f}px")
        
        print("\n" + "=" * 40)
        print("Individual Results")
        print("=" * 40)
        
        for result in self.results:
            if result.error:
                print(f"{result.filename}: ERROR - {result.error}")
            elif result.passed is not None:
                status = "PASS" if result.passed else "FAIL"
                print(f"{result.filename}: {status} - Distance: {result.distance:.2f}px (radius: {result.radius}px)")
    
    def print_summary_results(self):
        """Print summary statistics only."""
        print("=" * 30)
        print("PSF Validation Summary")
        print("=" * 30)
        print(f"Total Images: {self.total_images}")
        print(f"Validated: {self.validated_images}")
        print(f"Missing Metadata: {self.missing_metadata}")
        
        if self.validated_images > 0:
            print(f"Pass Rate: {self.passed_images/self.validated_images*100:.1f}%")
            print(f"Passed: {self.passed_images}")
            print(f"Failed: {self.failed_images}")
    
    def export_csv(self, output_file: str):
        """Export results to CSV format."""
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['filename', 'click_x', 'click_y', 'center_x', 'center_y', 'radius', 'distance', 'result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                if result.error:
                    writer.writerow({
                        'filename': result.filename,
                        'click_x': result.click_x,
                        'click_y': result.click_y,
                        'center_x': '',
                        'center_y': '',
                        'radius': '',
                        'distance': '',
                        'result': f'ERROR: {result.error}'
                    })
                else:
                    writer.writerow({
                        'filename': result.filename,
                        'click_x': result.click_x,
                        'click_y': result.click_y,
                        'center_x': result.center_x,
                        'center_y': result.center_y,
                        'radius': result.radius,
                        'distance': result.distance,
                        'result': 'PASS' if result.passed else 'FAIL'
                    })
        
        print(f"Results exported to: {output_file}")
    
    def export_json(self, output_file: str):
        """Export results to JSON format."""
        summary = {
            'total_images': self.total_images,
            'validated': self.validated_images,
            'missing_metadata': self.missing_metadata,
            'passed': self.passed_images,
            'failed': self.failed_images,
        }
        
        if self.validated_images > 0:
            summary['pass_rate'] = self.passed_images / self.validated_images * 100
            
            distances = [r.distance for r in self.results if r.distance is not None]
            if distances:
                summary['distance_stats'] = {
                    'average': sum(distances) / len(distances),
                    'min': min(distances),
                    'max': max(distances)
                }
        
        results_data = []
        for result in self.results:
            if result.error:
                results_data.append({
                    'filename': result.filename,
                    'click_x': result.click_x,
                    'click_y': result.click_y,
                    'error': result.error
                })
            else:
                results_data.append({
                    'filename': result.filename,
                    'click_x': result.click_x,
                    'click_y': result.click_y,
                    'center_x': result.center_x,
                    'center_y': result.center_y,
                    'radius': result.radius,
                    'distance': result.distance,
                    'passed': result.passed
                })
        
        export_data = {
            'summary': summary,
            'results': results_data
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Results exported to: {output_file}")


def main():
    """Main function to handle command line arguments and run validation."""
    parser = argparse.ArgumentParser(
        description="Validate PSF click coordinates against metadata."
    )
    
    parser.add_argument(
        "coordinates_file",
        help="File containing click coordinates (CSV format: filename,x,y)"
    )
    
    parser.add_argument(
        "--metadata-dir",
        default="example_psfs/",
        help="Directory containing metadata files (default: example_psfs/)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["detailed", "summary", "csv", "json"],
        default="detailed",
        help="Output format (default: detailed)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file for csv/json formats (optional)"
    )
    
    args = parser.parse_args()
    
    try:
        # Create validator and run validation
        validator = PSFValidator(args.coordinates_file, args.metadata_dir)
        results = validator.validate_all()
        
        # Output results based on format
        if args.format == "detailed":
            validator.print_detailed_results()
        elif args.format == "summary":
            validator.print_summary_results()
        elif args.format == "csv":
            output_file = args.output or "validation_results.csv"
            validator.export_csv(output_file)
        elif args.format == "json":
            output_file = args.output or "validation_results.json"
            validator.export_json(output_file)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nValidation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()