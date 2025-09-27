#!/usr/bin/env python3
"""
PDF Merger Script

A command-line tool to merge multiple PDF files into one.
If no files are provided as arguments, a GUI file selection dialog will open.

Usage:
    python mergepdf.py file1.pdf file2.pdf file3.pdf [--output merged.pdf]
    python mergepdf.py *.pdf --output combined.pdf
    python mergepdf.py  # Opens file selection dialog
"""

import argparse
import sys
import os
from pathlib import Path
from io import BytesIO

try:
    from PyPDF2 import PdfWriter, PdfReader
except ImportError:
    print("Error: PyPDF2 is required. Install it with: pip install PyPDF2")
    sys.exit(1)

# Optional: Pillow for image support (now required for image merging)
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}

# A4 sizing constants (we'll create 300 DPI pages so physical size is A4)
A4_DPI = 300
# Common 300 DPI A4 pixel dimensions (approx 8.27" x 11.69")
A4_WIDTH_PX = 2480  # could also be 2481 depending on rounding
A4_HEIGHT_PX = 3508


def merge_pdfs_and_images(input_files, output_file, image_size: str = "a4"):
    """Merge multiple PDF and image files into a single PDF.

    Each image is converted to a single-page PDF and appended in order.

    Args:
        input_files (list[str]): List of input file paths (PDF or images)
        output_file (str): Output PDF file path
    """
    pdf_writer = PdfWriter()
    total_input = len(input_files)
    for file_path in input_files:
        suffix = Path(file_path).suffix.lower()
        try:
            print(f"Processing: {file_path}")
            if suffix == '.pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    print(f"  Added {len(pdf_reader.pages)} pages from PDF {file_path}")
            elif suffix in SUPPORTED_IMAGE_EXTS:
                if not PIL_AVAILABLE:
                    print("  Skipped (Pillow not installed)")
                    continue
                with Image.open(file_path) as img:
                    # Convert to RGB (drop alpha) for PDF compatibility
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    buffer = BytesIO()

                    if image_size == "a4":
                        # Scale image to fit within A4 while preserving aspect ratio
                        scale = min(A4_WIDTH_PX / img.width, A4_HEIGHT_PX / img.height)
                        new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
                        if new_size != (img.width, img.height):
                            img = img.resize(new_size, Image.Resampling.LANCZOS)

                        # Create A4 white canvas and center the image
                        a4_canvas = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")
                        offset = ((A4_WIDTH_PX - img.width) // 2, (A4_HEIGHT_PX - img.height) // 2)
                        a4_canvas.paste(img, offset)

                        a4_canvas.save(buffer, format="PDF", resolution=A4_DPI)
                        buffer.seek(0)
                        img_pdf = PdfReader(buffer)
                        pdf_writer.add_page(img_pdf.pages[0])
                        print(f"  Converted image to A4 PDF page: {file_path} (placed at {img.width}x{img.height} within A4)")
                    else:  # original
                        # Save the image directly as a single-page PDF at its native pixel size.
                        # Note: PDF uses points; Pillow handles mapping. Large images may create large pages.
                        img.save(buffer, format="PDF")
                        buffer.seek(0)
                        img_pdf = PdfReader(buffer)
                        pdf_writer.add_page(img_pdf.pages[0])
                        print(f"  Added image at original resolution as PDF page: {file_path} ({img.width}x{img.height}px)")
            else:
                print(f"  Skipped unsupported file type: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    if len(pdf_writer.pages) == 0:
        print("Error: No pages were added. Nothing to write.")
        sys.exit(1)

    try:
        with open(output_file, 'wb') as output:
            pdf_writer.write(output)
        print(f"\nSuccessfully merged {total_input} file(s) into: {output_file}")
        print(f"Total pages in merged PDF: {len(pdf_writer.pages)}")
    except Exception as e:
        print(f"Error writing output file {output_file}: {e}")
        sys.exit(1)


def select_files_gui():
    """
    Open a file selection dialog to choose PDF files.
    
    Returns:
        tuple: (input_files, output_file) or (None, None) if cancelled
    """
    if not GUI_AVAILABLE:
        print("Error: GUI not available. Please provide files as command line arguments.")
        print("tkinter is required for the file selection dialog.")
        return None, None
    
    # Create a root window but hide it
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Bring dialog to front
    
    try:
        # Select input files
        input_files = filedialog.askopenfilenames(
            title="Select PDF and image files to merge",
            filetypes=[
                ("PDF and Images", "*.pdf *.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp"),
                ("PDF files", "*.pdf"),
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp"),
                ("All files", "*.*"),
            ],
            multiple=True,
        )
        
        if not input_files:
            print("No files selected. Operation cancelled.")
            return None, None
        
        # Validate that selected files are PDFs or supported images
        valid_files = []
        for file_path in input_files:
            suffix = Path(file_path).suffix.lower()
            if suffix == '.pdf' or suffix in SUPPORTED_IMAGE_EXTS:
                if suffix in SUPPORTED_IMAGE_EXTS and not PIL_AVAILABLE:
                    print(f"Warning: Pillow not installed. Skipping image file: {file_path}")
                else:
                    valid_files.append(file_path)
            else:
                print(f"Warning: Skipping unsupported file: {file_path}")
        
        if not valid_files:
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "No valid PDF or image files selected.")
            return None, None
        
        # Allow even a single file (user may want to convert an image to PDF)
        if len(valid_files) == 0:
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "No valid PDF or image files selected.")
            return None, None
        
        # Select output file
        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="merged.pdf"
        )
        
        if not output_file:
            print("No output file specified. Operation cancelled.")
            return None, None

        return valid_files, output_file
        
    except Exception as e:
        print(f"Error in file selection: {e}")
        return None, None
    finally:
        root.destroy()


def validate_input_files(file_paths):
    """Validate input files (PDFs or supported images).

    Args:
        file_paths (list[str]): Paths to validate

    Returns:
        list[str]: Valid file paths
    """
    valid_files = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        if not path.is_file():
            print(f"Warning: Not a file: {file_path}")
            continue
        suffix = path.suffix.lower()
        if suffix == '.pdf' or suffix in SUPPORTED_IMAGE_EXTS:
            if suffix in SUPPORTED_IMAGE_EXTS and not PIL_AVAILABLE:
                print(f"Warning: Pillow not installed. Skipping image: {file_path}")
                continue
            valid_files.append(str(path))
        else:
            print(f"Warning: Unsupported file type: {file_path}")
    return valid_files


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python mergepdf.py file1.pdf file2.pdf file3.pdf
    python mergepdf.py file1.pdf file2.pdf --output combined.pdf
    python mergepdf.py *.pdf --output all_merged.pdf
    python mergepdf.py  # Opens file selection dialog
        """
    )
    
    parser.add_argument(
        'input_files',
        nargs='*',
    help='PDF/image files to merge (if not provided, a file selection dialog will open)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='merged.pdf',
        help='Output filename (default: merged.pdf)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--image-size',
        choices=['a4', 'original'],
        default='a4',
        help='How to place images: a4 (default, resize & center on A4) or original (keep original resolution)'
    )
    
    args = parser.parse_args()
    
    # If no input files provided, use GUI file selection
    if not args.input_files:
        print("No files provided. Opening file selection dialog...")
        selected_files, output_file = select_files_gui()
        if selected_files is None:
            sys.exit(0)
        valid_files = selected_files
        output_filename = output_file
    else:
        # Validate input files from command line
        valid_files = validate_input_files(args.input_files)
        output_filename = args.output
        if not valid_files:
            print("Error: No valid PDF or image files provided")
            sys.exit(1)
        
        # Check if output file already exists
        if os.path.exists(output_filename):
            response = input(f"Output file '{output_filename}' already exists. Overwrite? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Operation cancelled.")
                sys.exit(0)
    
    if args.verbose:
        print(f"Input files: {valid_files}")
        print(f"Output file: {output_filename}")
        print()
    
    # Merge the PDFs & images
    if any(Path(f).suffix.lower() in SUPPORTED_IMAGE_EXTS for f in valid_files) and not PIL_AVAILABLE:
        print("Error: Image files supplied but Pillow is not installed. Install with: pip install Pillow")
        sys.exit(1)
    merge_pdfs_and_images(valid_files, output_filename, image_size=args.image_size)


if __name__ == '__main__':
    main()
