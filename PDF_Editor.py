from tkinter import filedialog, ttk
import tkinter as tk
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PDF Editor")
        self.window.geometry("400x500")
        self.pdf_path = None
        self.pages = []
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.select_button = ttk.Button(self.main_frame, text="Select PDF", command=self.select_pdf_file)
        self.select_button.pack(pady=5)
        
        # Create listbox for pages
        self.pages_listbox = tk.Listbox(self.main_frame, selectmode=tk.SINGLE)
        self.pages_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create movement buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="↑", command=self.move_up).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="↓", command=self.move_down).pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = ttk.Button(self.main_frame, text="Save", command=self.save_pdf)
        self.save_button.pack(pady=5)
        
    def select_pdf_file(self):
        self.pdf_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if self.pdf_path:
            self.load_pdf_pages()
    
    def load_pdf_pages(self):
        reader = PdfReader(self.pdf_path)
        self.pages = list(range(len(reader.pages)))
        self.update_listbox()
    
    def update_listbox(self):
        self.pages_listbox.delete(0, tk.END)
        for i in self.pages:
            self.pages_listbox.insert(tk.END, f"Page {i + 1}")
    
    def move_up(self):
        idx = self.pages_listbox.curselection()
        if idx and idx[0] > 0:
            current_idx = idx[0]
            self.pages[current_idx], self.pages[current_idx-1] = \
                self.pages[current_idx-1], self.pages[current_idx]
            self.update_listbox()
            self.pages_listbox.selection_set(current_idx-1)
    
    def move_down(self):
        idx = self.pages_listbox.curselection()
        if idx and idx[0] < len(self.pages) - 1:
            current_idx = idx[0]
            self.pages[current_idx], self.pages[current_idx+1] = \
                self.pages[current_idx+1], self.pages[current_idx]
            self.update_listbox()
            self.pages_listbox.selection_set(current_idx+1)
    
    def save_pdf(self):
        if not self.pdf_path:
            return
            
        # Create new filename
        directory = os.path.dirname(self.pdf_path)
        filename = os.path.basename(self.pdf_path)
        name, ext = os.path.splitext(filename)
        new_path = os.path.join(directory, f"{name}_modified{ext}")
        
        # Create new PDF with reordered pages
        reader = PdfReader(self.pdf_path)
        writer = PdfWriter()
        
        for page_num in self.pages:
            writer.add_page(reader.pages[page_num])
            
        # Save the new PDF
        with open(new_path, 'wb') as output_file:
            writer.write(output_file)
            
        tk.messagebox.showinfo("Success", f"PDF saved as: {new_path}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PDFEditor()
    app.run()

