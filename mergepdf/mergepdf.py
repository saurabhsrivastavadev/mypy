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

try:
    from PyPDF2 import PdfWriter, PdfReader
except ImportError:
    print("Error: PyPDF2 is required. Install it with: pip install PyPDF2")
    sys.exit(1)

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def merge_pdfs(input_files, output_file):
    """
    Merge multiple PDF files into one.
    
    Args:
        input_files (list): List of input PDF file paths
        output_file (str): Output PDF file path
    """
    pdf_writer = PdfWriter()
    
    for file_path in input_files:
        try:
            print(f"Processing: {file_path}")
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                
                # Add all pages from the current PDF
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
                    
                print(f"  Added {len(pdf_reader.pages)} pages from {file_path}")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    # Write the merged PDF to output file
    try:
        with open(output_file, 'wb') as output:
            pdf_writer.write(output)
        print(f"\nSuccessfully merged {len(input_files)} files into: {output_file}")
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
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            multiple=True
        )
        
        if not input_files:
            print("No files selected. Operation cancelled.")
            return None, None
        
        # Validate that selected files are PDFs
        valid_files = []
        for file_path in input_files:
            if Path(file_path).suffix.lower() == '.pdf':
                valid_files.append(file_path)
            else:
                print(f"Warning: Skipping non-PDF file: {file_path}")
        
        if not valid_files:
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "No valid PDF files selected.")
            return None, None
        
        if len(valid_files) < 2:
            if GUI_AVAILABLE:
                messagebox.showwarning("Warning", "Please select at least 2 PDF files to merge.")
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
    """
    Validate that input files exist and are PDF files.
    
    Args:
        file_paths (list): List of file paths to validate
        
    Returns:
        list: List of valid PDF file paths
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
            
        if path.suffix.lower() != '.pdf':
            print(f"Warning: Not a PDF file: {file_path}")
            continue
            
        valid_files.append(str(path))
    
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
        help='PDF files to merge (if not provided, a file selection dialog will open)'
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
            print("Error: No valid PDF files provided")
            sys.exit(1)
        
        if len(valid_files) < 2:
            print("Warning: Only one valid PDF file found. No merging needed.")
            if len(valid_files) == 1:
                print(f"You can copy {valid_files[0]} to {output_filename} if needed.")
            sys.exit(0)
        
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
    
    # Merge the PDFs
    merge_pdfs(valid_files, output_filename)


if __name__ == '__main__':
    main()
