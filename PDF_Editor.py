from tkinter import filedialog, ttk
import tkinter as tk
from PyPDF2 import PdfReader, PdfWriter
import os
import fitz
from PIL import Image, ImageTk
from tkinter import messagebox
from version import VERSION

class PDFEditor:
    def center_window(self, window=None, width=800, height=500):
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # If no window specified, use main window
        if window is None:
            window = self.window
        
        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window position
        window.geometry(f"{width}x{height}+{x}+{y}")

    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"PDF Editor v{VERSION}")
        
        # Center main window
        self.center_window()
        
        self.pdf_path = None
        self.pages = []
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top button container
        top_container = ttk.Frame(self.main_frame)
        top_container.pack(pady=5, fill=tk.X)
        
        # Left frame for movement buttons
        move_frame = ttk.Frame(top_container)
        move_frame.pack(side=tk.LEFT, padx=10)
        ttk.Button(move_frame, text="↑", command=self.move_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(move_frame, text="↓", command=self.move_down).pack(side=tk.LEFT, padx=2)
        ttk.Button(move_frame, text="Delete", command=self.delete_page).pack(side=tk.LEFT, padx=2)
        
        # Center frame for Select and Save buttons
        center_frame = ttk.Frame(top_container)
        center_frame.pack(expand=True)
        self.select_button = ttk.Button(center_frame, text="Select PDF", command=self.select_pdf_file)
        self.select_button.pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(center_frame, text="Save", command=self.save_pdf)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.save_as_button = ttk.Button(center_frame, text="Save As", command=self.save_as_pdf)
        self.save_as_button.pack(side=tk.LEFT, padx=5)
        self.get_text_button = ttk.Button(center_frame, text="Get Text", command=self.extract_text)
        self.get_text_button.pack(side=tk.LEFT, padx=5)

        # Create split view
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for list
        self.left_frame = ttk.Frame(self.paned_window, width=200)  # Increased width
        self.left_frame.pack_propagate(False)  # Prevent frame from shrinking
        self.paned_window.add(self.left_frame)
        
        # Create listbox for pages
        self.pages_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
        self.pages_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.pages_listbox.bind('<<ListboxSelect>>', self.on_page_select)
        
        # Right frame for preview
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame)
        
        # Preview label
        self.preview_label = ttk.Label(self.right_frame)
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Center Select PDF button for empty state
        self.center_select_button = ttk.Button(self.right_frame, text="Select PDF", command=self.select_pdf_file)
        self.center_select_button.configure(style='Large.TButton')
        self.center_select_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Create custom style for large button
        style = ttk.Style()
        style.configure('Large.TButton', font=('TkDefaultFont', 14, 'bold'), padding=(20, 10))

    def load_pdf_pages(self):
        if self.pdf_path is None:
            return
            
        # Hide center select button when PDF is loaded
        self.center_select_button.place_forget()
        
        reader = PdfReader(self.pdf_path)
        self.pages = list(range(len(reader.pages)))
        self.update_listbox()
        if self.pages:  # Show first page preview
            self.show_preview(0)
    
    def select_pdf_file(self):
        self.pdf_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if self.pdf_path:
            self.load_pdf_pages()
    
    def on_page_select(self, event):
        if not self.pdf_path:
            return
        
        selection = self.pages_listbox.curselection()
        if not selection:
            return
            
        page_idx = self.pages[selection[0]]
        self.show_preview(page_idx)
    
    def show_preview(self, page_idx):
        doc = fitz.open(self.pdf_path)
        page = doc[page_idx]
        
        # Get frame size
        frame_width = self.right_frame.winfo_width()
        frame_height = self.right_frame.winfo_height()
        
        # Get page size
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Calculate scaling factor to fit the frame while maintaining aspect ratio
        width_ratio = frame_width / page_width
        height_ratio = frame_height / page_height
        scale = min(width_ratio, height_ratio) * 0.9  # 90% of frame size for padding
        
        # Render page to image with calculated scale
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        
        # Convert to PhotoImage and store as instance variable
        self._photo = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=self._photo)
        
        doc.close()
    
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
    
    def delete_page(self):
        idx = self.pages_listbox.curselection()
        if not idx:
            return
            
        current_idx = idx[0]
        del self.pages[current_idx]
        self.update_listbox()
        
        # Select the next page or the last page if we deleted the last one
        if self.pages:
            if current_idx >= len(self.pages):
                self.pages_listbox.selection_set(len(self.pages)-1)
                self.show_preview(self.pages[len(self.pages)-1])
            else:
                self.pages_listbox.selection_set(current_idx)
                self.show_preview(self.pages[current_idx])
    
    def save_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Ouvrez un PDF d'abord")
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
            
        try:
            if new_path:
                messagebox.showinfo("Success", f"PDF enregistré sous :{new_path}")
            else:
                messagebox.showerror("Error", "Échec de l'enregistrement du PDF : Chemin de sortie non défini")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

    def save_as_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Ouvrez un PDF d'abord")
            return
            
        # Open save file dialog
        new_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=os.path.basename(self.pdf_path),
            initialdir=os.path.dirname(self.pdf_path),
            title="Save PDF As",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if new_path:
            # Create new PDF with reordered pages
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            
            for page_num in self.pages:
                writer.add_page(reader.pages[page_num])
                
            # Save the new PDF
            try:
                with open(new_path, 'wb') as output_file:
                    writer.write(output_file)
                messagebox.showinfo("Success", f"PDF saved as: {new_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

    def extract_text(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Please open a PDF first")
            return
            
        try:
            doc = fitz.open(self.pdf_path)
            text = ""
            for page_num in self.pages:
                page = doc[page_num]
                text += f"\n=== Page {page_num + 1} ===\n"
                text += page.get_text("text")
            doc.close()
            
            # Copy text to clipboard automatically
            self.window.clipboard_clear()
            self.window.clipboard_append(text)
            
            # Create a new window to display the text
            text_window = tk.Toplevel(self.window)
            text_window.title("Extracted Text")
            self.center_window(text_window, width=600, height=400)
            
            # Add text widget with scrollbar
            text_frame = ttk.Frame(text_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, text)
            
            scrollbar.config(command=text_widget.yview)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {str(e)}")

def run(self):
    self.window.mainloop()

if __name__ == "__main__":
    app = PDFEditor()
    app.window.mainloop()
    