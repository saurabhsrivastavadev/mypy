# PDF & Image Merger Tool

A simple command-line tool to merge multiple PDF files and image files (PNG, JPG, JPEG, BMP, TIFF, WEBP) into a single PDF. Images are automatically centered on an A4-sized (300 DPI) white page so every page in the output PDF has a consistent A4 size. Features both command-line interface and GUI file selection.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install directly (minimum):
```bash
pip install PyPDF2
```

To enable image support install Pillow (already included in `requirements.txt`):
```bash
pip install Pillow
```

Note: The GUI file selection uses tkinter, which is included with most Python installations.

## Usage

### GUI Mode (No Arguments)
```bash
python mergepdf.py
```
This will open a file selection dialog where you can:
1. Select multiple PDF files to merge
2. Choose the output filename and location

### Command Line Mode (PDF + Images)
```bash
python mergepdf.py file1.pdf scan2.pdf photo1.jpg diagram.png
```
This will create a `merged.pdf` file containing all the pages from the input PDFs plus one page per image (images are auto-converted to PDF pages).

### Specify Output Filename
```bash
python mergepdf.py file1.pdf file2.pdf --output combined.pdf
```

### Merge All PDFs & Images in Directory (shell glob depends on OS)
```bash
python mergepdf.py *.pdf *.png *.jpg --output all_merged.pdf
```

### Verbose Output
```bash
python mergepdf.py file1.pdf file2.pdf --verbose
```

## Command Line Arguments

- `input_files`: One or more PDF and/or image files to merge
- `-o, --output`: Output filename (default: merged.pdf)
- `-v, --verbose`: Show verbose output
- `-h, --help`: Show help message

## Examples

1. **GUI Mode - No arguments (easiest)**:
   ```bash
   python mergepdf.py
   ```

2. Merge PDFs and images:
   ```bash
   python mergepdf.py document1.pdf page2.pdf photo.jpg diagram.png
   ```

3. Merge files with custom output name:
   ```bash
   python mergepdf.py report*.pdf --output final_report.pdf
   ```

4. Merge all PDFs & images in current directory:
   ```bash
   python mergepdf.py *.pdf *.jpg *.png --output complete_collection.pdf
   ```

## Features

- ✅ **GUI file selection** - Run without arguments for easy file selection
- ✅ Merge multiple PDF files
- ✅ Merge images (PNG, JPG, JPEG, BMP, TIFF, WEBP) into PDF pages
- ✅ Auto-resize & center images onto A4 pages (uniform output size)
- ✅ Command-line interface
- ✅ Custom output filename
- ✅ Input validation
- ✅ Error handling
- ✅ Progress feedback
- ✅ Overwrite protection
- ✅ Verbose mode
- ✅ Cross-platform compatibility

## Error Handling

The script will:
- Skip files that don't exist
- Skip unsupported file types
- Continue processing even if one file fails
- Ask for confirmation before overwriting existing output files
- Display helpful error messages
