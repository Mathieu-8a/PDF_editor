from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QListWidget, QLabel, 
                           QFileDialog, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyPDF2 import PdfReader, PdfWriter
import os
import fitz
import sys
from PIL import Image

class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 500)
        self.pdf_path = None
        self.pages = []
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create top button container
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        
        # Movement buttons
        move_frame = QWidget()
        move_layout = QHBoxLayout(move_frame)
        up_button = QPushButton("↑")
        down_button = QPushButton("↓")
        delete_button = QPushButton("Delete")
                
        up_button.clicked.connect(lambda: self.move_up())
        down_button.clicked.connect(lambda: self.move_down())
        # Define delete_page method before connecting it
                    
        delete_button.clicked.connect(lambda: self.delete_page())
        move_layout.addWidget(up_button)
        move_layout.addWidget(down_button)
        move_layout.addWidget(delete_button)
        top_layout.addWidget(move_frame)
        
        # Center buttons
        center_frame = QWidget()
        center_layout = QHBoxLayout(center_frame)
        self.select_button = QPushButton("Select PDF")
        self.save_button = QPushButton("Save")
        self.save_as_button = QPushButton("Save As")
        self.select_button.clicked.connect(self.select_pdf_file)
        self.save_button.setEnabled(False)  # Remove this line or change to True
        self.save_button.clicked.connect(self.save_pdf)  # Add this line
        self.save_as_button.clicked.connect(self.save_pdf)
        center_layout.addWidget(self.select_button)
        center_layout.addWidget(self.save_button)
        center_layout.addWidget(self.save_as_button)
        top_layout.addWidget(center_frame)
        
        layout.addWidget(top_container)
        
        # Create split view
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side (list)
        self.pages_listbox = QListWidget()
        self.pages_listbox.currentRowChanged.connect(self.on_page_select)
        splitter.addWidget(self.pages_listbox)
        
        # Right side (preview)
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        splitter.addWidget(self.preview_label)
        
        layout.addWidget(splitter)
        
        # Center the window
        self.center_window()

    def move_up(self):
        current_row = self.pages_listbox.currentRow()
        if current_row > 0:
            self.pages[current_row], self.pages[current_row - 1] = \
                self.pages[current_row - 1], self.pages[current_row]
            self.update_listbox()
            self.pages_listbox.setCurrentRow(current_row - 1)
    
    def move_down(self):
        current_row = self.pages_listbox.currentRow()
        if current_row >= 0 and current_row < len(self.pages) - 1:
            self.pages[current_row], self.pages[current_row + 1] = \
                self.pages[current_row + 1], self.pages[current_row]
            self.update_listbox()
            self.pages_listbox.setCurrentRow(current_row + 1)

    def delete_page(self):
        current_row = self.pages_listbox.currentRow()
        if current_row >= 0:
            del self.pages[current_row]
            self.update_listbox()
            if self.pages:
                new_row = min(current_row, len(self.pages) - 1)
                self.pages_listbox.setCurrentRow(new_row)
            else:
                self.preview_label.clear()

    def center_window(self):
        screen = QApplication.screens()[0].availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def load_pdf_pages(self):
        if not self.pdf_path:
            return
            
        reader = PdfReader(self.pdf_path)
        self.pages = list(range(len(reader.pages)))
        self.update_listbox()
        if self.pages:
            self.show_preview(0)
    
    def select_pdf_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF file",
            "",
            "PDF files (*.pdf);;All files (*.*)"
        )
        if file_name:
            self.pdf_path = file_name
            self.load_pdf_pages()

    def show_preview(self, page_idx):
        doc = fitz.open(self.pdf_path)
        page = doc[page_idx]
        
        # Get frame size
        frame_width = self.preview_label.width()
        frame_height = self.preview_label.height()
        
        # Get page size and calculate scale
        page_rect = page.rect
        width_ratio = frame_width / page_rect.width
        height_ratio = frame_height / page_rect.height
        scale = min(width_ratio, height_ratio) * 0.9
        
        # Render page
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        
        # Convert to QPixmap and display
        qim = QImage(img.tobytes(), img.width, img.height, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        self.preview_label.setPixmap(pixmap)
        
        doc.close()

    def update_listbox(self):
        self.pages_listbox.clear()
        for i in self.pages:
            self.pages_listbox.addItem(f"Page {i + 1}")

    def on_page_select(self, current_row):
        if current_row >= 0 and self.pdf_path:
            self.show_preview(self.pages[current_row])

    def save_pdf(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "Warning", "Please open a PDF file first")
            return
            
        # Create new filename
        directory = os.path.dirname(self.pdf_path)
        filename = os.path.basename(self.pdf_path)
        name, ext = os.path.splitext(filename)
        new_path = os.path.join(directory, f"{name}_modified{ext}")
        
        try:
            # Create new PDF with reordered pages
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            
            for page_num in self.pages:
                writer.add_page(reader.pages[page_num])
                
            # Save the new PDF
            with open(new_path, 'wb') as output_file:
                writer.write(output_file)
            
            QMessageBox.information(self, "Success", f"PDF saved as: {new_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")

    def main():
        app = QApplication(sys.argv)
        editor = PDFEditor()
        editor.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    PDFEditor.main()
