# PDF Editor

A simple and efficient PDF editor that allows you to reorganize, delete, and save PDF pages.

> ⚠️ **Note:** Please use the stable version (PDF_Editor.py) for now.
> The Qt version (PDF_Editor_Qt.py) is currently under development. 

## Features

- View PDF files with page preview
- Reorder pages using up/down buttons
- Delete unwanted pages
- Save modified PDF with new page order
- Modern interface

## Installation

1. Download the latest release from the releases page
2. Run the executable `PDF_Editor.exe`

No additional installation required.

## Usage

1. Click "Select PDF" to open a PDF file
2. Use the preview pane to view pages
3. Reorder pages using the arrow buttons
4. Delete unwanted pages using the Delete button
5. Save your changes using either:
   - "Save" to create a new file with "_modified" suffix
   - "Save As" to choose a custom location and name

## System Requirements

- Windows 10 or later
- No additional software required

## Building from Source

If you want to build from source:

```bash
pip install -r requirements.txt
pyinstaller --name="PDF Editor" --windowed --icon=icon.ico --onefile --hidden-import=PIL._tkinter --collect-all fitz PDF_Editor.py
