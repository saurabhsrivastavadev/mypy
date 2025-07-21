# PDF Merger Tool

A simple command-line tool to merge multiple PDF files into one. Features both command-line interface and GUI file selection.

## Installation

1. Install the required dependency:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install PyPDF2
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

### Command Line Mode
```bash
python mergepdf.py file1.pdf file2.pdf file3.pdf
```
This will create a `merged.pdf` file containing all the pages from the input files.

### Specify Output Filename
```bash
python mergepdf.py file1.pdf file2.pdf --output combined.pdf
```

### Merge All PDFs in Directory
```bash
python mergepdf.py *.pdf --output all_merged.pdf
```

### Verbose Output
```bash
python mergepdf.py file1.pdf file2.pdf --verbose
```

## Command Line Arguments

- `input_files`: One or more PDF files to merge (required)
- `-o, --output`: Output filename (default: merged.pdf)
- `-v, --verbose`: Show verbose output
- `-h, --help`: Show help message

## Examples

1. **GUI Mode - No arguments (easiest)**:
   ```bash
   python mergepdf.py
   ```

2. Merge three specific files:
   ```bash
   python mergepdf.py document1.pdf document2.pdf document3.pdf
   ```

3. Merge files with custom output name:
   ```bash
   python mergepdf.py report*.pdf --output final_report.pdf
   ```

4. Merge all PDFs in current directory:
   ```bash
   python mergepdf.py *.pdf --output complete_collection.pdf
   ```

## Features

- ✅ **GUI file selection** - Run without arguments for easy file selection
- ✅ Merge multiple PDF files
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
- Skip non-PDF files
- Continue processing even if one file fails
- Ask for confirmation before overwriting existing output files
- Display helpful error messages
