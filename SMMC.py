import tkinter as tk
from tkinter import filedialog, messagebox, ttk
# import PyPDF2  # Removed unused dependency
# from reportlab.pdfgen import canvas  # Removed unused dependency
# from reportlab.lib.pagesizes import letter, A4  # Removed unused dependency
# from reportlab.lib.units import inch  # Removed unused dependency
import os
import tempfile
import fitz  # PyMuPDF
from pathlib import Path
import subprocess
import platform
import atexit
import threading
import time
from PIL import Image

class PDFMarginAdjuster:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Top Margin Adjuster with Watermark")
        self.root.geometry("700x500")
        self.root.configure(bg='#f0f0f0')
        
        self.input_file = ""
        self.output_file = ""
        self.logo_file = ""
        self.temp_files = []  # Keep track of temporary files
        
        # Check for logo.png in the same directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_logo = os.path.join(script_dir, "logo.png")
        if os.path.exists(default_logo):
            self.logo_file = default_logo
            
        # Check for default background in root or tool/background.pdf
        self.background_file = ""
        self.use_background = tk.BooleanVar(value=False)
        
        possible_bgs = [
            os.path.join(script_dir, "background.pdf"),
            os.path.join(script_dir, "tool", "background.pdf")
        ]
        
        for bg_path in possible_bgs:
            if os.path.exists(bg_path):
                self.background_file = bg_path
                # DEFAULT DISABLED: self.use_background.set(True)
                break
        
        # Register cleanup function
        atexit.register(self.cleanup_temp_files)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="PDF Top Margin Adjuster with Watermark", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0'
        )
        title_label.pack(pady=20)
        
        # Input file selection
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            input_frame, 
            text="Select Input PDF:", 
            font=("Arial", 10, "bold"),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        input_button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        input_button_frame.pack(fill='x', pady=5)
        
        self.input_label = tk.Label(
            input_button_frame, 
            text="No file selected", 
            bg='white', 
            relief='sunken',
            anchor='w',
            padx=10,
            pady=5
        )
        self.input_label.pack(side='left', fill='x', expand=True)
        
        input_btn = tk.Button(
            input_button_frame,
            text="Browse",
            command=self.select_input_file,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='raised',
            padx=20
        )
        input_btn.pack(side='right', padx=(10, 0))
        
        # Logo file selection
        logo_frame = tk.Frame(self.root, bg='#f0f0f0')
        logo_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            logo_frame, 
            text="Select Logo for Watermark (Optional):", 
            font=("Arial", 10, "bold"),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        logo_button_frame = tk.Frame(logo_frame, bg='#f0f0f0')
        logo_button_frame.pack(fill='x', pady=5)
        
        self.logo_label = tk.Label(
            logo_button_frame, 
            text="logo.png (found)" if self.logo_file else "No logo selected", 
            bg='white', 
            relief='sunken',
            anchor='w',
            padx=10,
            pady=5
        )
        self.logo_label.pack(side='left', fill='x', expand=True)
        
        logo_btn = tk.Button(
            logo_button_frame,
            text="Browse",
            command=self.select_logo_file,
            bg='#9C27B0',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='raised',
            padx=20
        )
        logo_btn.pack(side='right', padx=(10, 0))
        
        # Background file selection
        bg_frame = tk.Frame(self.root, bg='#f0f0f0')
        bg_frame.pack(pady=10, padx=20, fill='x')
        
        bg_header_frame = tk.Frame(bg_frame, bg='#f0f0f0')
        bg_header_frame.pack(fill='x')
        
        tk.Checkbutton(
            bg_header_frame,
            text="Apply Background PDF",
            variable=self.use_background,
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(side='left')
        
        bg_button_frame = tk.Frame(bg_frame, bg='#f0f0f0')
        bg_button_frame.pack(fill='x', pady=5)
        
        self.bg_label = tk.Label(
            bg_button_frame, 
            text="background.pdf (found)" if self.background_file else "No background selected", 
            bg='white', 
            relief='sunken',
            anchor='w',
            padx=10,
            pady=5
        )
        self.bg_label.pack(side='left', fill='x', expand=True)
        
        bg_btn = tk.Button(
            bg_button_frame,
            text="Browse",
            command=self.select_background_file,
            bg='#607D8B',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='raised',
            padx=20
        )
        bg_btn.pack(side='right', padx=(10, 0))
        
        # Options frame
        options_frame = tk.LabelFrame(
            self.root, 
            text="Options", 
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        options_frame.pack(pady=20, padx=20, fill='x')
        
        # Line spacing option
        spacing_frame = tk.Frame(options_frame, bg='#f0f0f0')
        spacing_frame.pack(fill='x', pady=5)
        
        tk.Label(
            spacing_frame, 
            text="Number of lines to add at top:", 
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.line_count = tk.IntVar(value=4)
        line_spinbox = tk.Spinbox(
            spacing_frame,
            from_=1,
            to=10,
            textvariable=self.line_count,
            width=5
        )
        line_spinbox.pack(side='right')
        
        # Watermark opacity option
        opacity_frame = tk.Frame(options_frame, bg='#f0f0f0')
        opacity_frame.pack(fill='x', pady=5)
        
        tk.Label(
            opacity_frame, 
            text="Watermark Opacity (0.1-1.0):", 
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.opacity = tk.DoubleVar(value=0.1)
        opacity_spinbox = tk.Spinbox(
            opacity_frame,
            from_=0.1,
            to=1.0,
            increment=0.1,
            textvariable=self.opacity,
            width=5,
            format="%.1f"
        )
        opacity_spinbox.pack(side='right')
        
        # Watermark start line option
        start_line_frame = tk.Frame(options_frame, bg='#f0f0f0')
        start_line_frame.pack(fill='x', pady=5)
        
        tk.Label(
            start_line_frame, 
            text="Watermark starts from line:", 
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.watermark_start_line = tk.IntVar(value=6)
        start_line_spinbox = tk.Spinbox(
            start_line_frame,
            from_=1,
            to=20,
            textvariable=self.watermark_start_line,
            width=5
        )
        start_line_spinbox.pack(side='right')
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # Process and Open button
        process_open_btn = tk.Button(
            button_frame,
            text="Process & Open PDF",
            command=self.process_and_open_pdf,
            bg='#FF5722',
            fg='white',
            font=("Arial", 12, "bold"),
            relief='raised',
            padx=30,
            pady=10
        )
        process_open_btn.pack(side='left', padx=10)
        
        # Process and Save button
        process_save_btn = tk.Button(
            button_frame,
            text="Process & Save PDF",
            command=self.process_and_save_pdf,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12, "bold"),
            relief='raised',
            padx=30,
            pady=10
        )
        process_save_btn.pack(side='left', padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root, 
            length=400, 
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root, 
            text="Ready to process PDF", 
            bg='#f0f0f0',
            font=("Arial", 9)
        )
        self.status_label.pack(pady=5)
    
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.input_label.config(text=os.path.basename(file_path))
    
    def select_logo_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.logo_file = file_path
            self.logo_label.config(text=os.path.basename(file_path))
            
    def select_background_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Background PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.background_file = file_path
            self.bg_label.config(text=os.path.basename(file_path))
            self.use_background.set(True)
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()
    
    def cleanup_temp_files(self):
        """Clean up temporary files when the application exits"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass  # Ignore errors during cleanup
    
    def monitor_pdf_and_cleanup(self, temp_file_path):
        """Monitor if PDF is still open and cleanup when closed"""
        def check_file_usage():
            while True:
                time.sleep(2)  # Check every 2 seconds
                try:
                    # Try to rename the file - if it fails, it's probably still open
                    temp_name = temp_file_path + ".tmp_check"
                    os.rename(temp_file_path, temp_name)
                    os.rename(temp_name, temp_file_path)
                    
                    # If we reach here, file is not in use - wait a bit more then delete
                    time.sleep(5)
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                        if temp_file_path in self.temp_files:
                            self.temp_files.remove(temp_file_path)
                    break
                except (OSError, IOError):
                    # File is still in use, continue monitoring
                    continue
                except Exception:
                    # Some other error, stop monitoring
                    break
        
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=check_file_usage, daemon=True)
        monitor_thread.start()
    
    def open_pdf_with_default_app(self, file_path):
        """Open PDF with the default system application"""
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF: {str(e)}")
            return False
    
    def process_pdf(self, output_path=None, is_temp=False):
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input PDF file.")
            return None
        
        try:
            self.update_status("Processing PDF...")
            self.progress['value'] = 0
            
            # Create output path if not provided
            if output_path is None:
                if is_temp:
                    temp_fd, output_path = tempfile.mkstemp(suffix='.pdf', prefix='pdf_margin_')
                    os.close(temp_fd)  # Close the file descriptor
                    self.temp_files.append(output_path)
                else:
                    if not self.output_file:
                        messagebox.showerror("Error", "Please select an output location.")
                        return None
                    output_path = self.output_file
            
            # Open the input PDF
            pdf_document = fitz.open(self.input_file)
            total_pages = len(pdf_document)

            # Load background PDF if enabled
            bg_document = None
            bg_page = None
            if self.use_background.get() and self.background_file and os.path.exists(self.background_file):
                # print(f"DEBUG: Background Enabled. File: {self.background_file}")
                try:
                    bg_document = fitz.open(self.background_file)
                    if len(bg_document) > 0:
                        bg_page = bg_document[0]  # Use first page as background
                except Exception as e:
                    print(f"Warning: Could not load background PDF: {e}")
            # else:
            #     print(f"DEBUG: Background Disabled per checkbox (Value: {self.use_background.get()})")
            
            # Calculate line height and margins
            line_height = 16  # points
            top_margin = self.line_count.get() * line_height
            watermark_start_y = self.watermark_start_line.get() * line_height
            
            # Create a new PDF document
            new_pdf = fitz.open()
            
            for page_num in range(total_pages):
                self.update_status(f"Processing page {page_num + 1} of {total_pages}...")
                self.progress['value'] = (page_num / total_pages) * 90
                
                # Get the original page
                original_page = pdf_document[page_num]
                original_rect = original_page.rect
                
                # Create a new page with the SAME size as original
                new_page = new_pdf.new_page(width=original_rect.width, height=original_rect.height)
                
                # Calculate the area where content should be placed (reduced by top margin)
                content_rect = fitz.Rect(0, top_margin, original_rect.width, original_rect.height)
                
                # Scale factor to fit original content in the smaller area
                scale_factor = (original_rect.height - top_margin) / original_rect.height
                
                # Create transformation matrix: scale down and move down by top_margin
                transform = fitz.Matrix(1, 0, 0, scale_factor, 0, top_margin)
                
                # Insert the original page content with scaling and positioning
                new_page.show_pdf_page(
                    content_rect,
                    pdf_document,
                    page_num,
                    clip=original_rect
                )
                
                # Apply Background if active (Overlay Mode - Middle Layer)
                if bg_page:
                    # print("DEBUG: Applying Background Overlay")
                    # Draw background page as overlay
                    new_page.show_pdf_page(
                        new_page.rect,
                        bg_document,
                        0, # page number 0 of background doc
                        clip=None
                    )
                
                # Add watermark if logo is selected (Applies on TOP of everything)
                # This ensures it is always visible, even if background/content is opaque
                if self.logo_file and os.path.exists(self.logo_file):
                    # print("DEBUG: Applying Logo Watermark")
                    self.add_watermark_to_page(new_page, original_rect, watermark_start_y)
            
            self.update_status("Saving output file...")
            self.progress['value'] = 95
            
            # Save the new PDF
            new_pdf.save(output_path)
            new_pdf.close()
            pdf_document.close()
            if bg_document:
                bg_document.close()
            
            self.progress['value'] = 100
            self.update_status("PDF processed successfully!")
            
            return output_path
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"An error occurred while processing the PDF:\n{str(e)}\n\nPlease ensure:\n1. The input file is a valid PDF\n2. The output location is writable\n3. PyMuPDF (fitz) is installed\n4. PIL is installed for image processing"
            )
            self.update_status("Error occurred during processing")
            return None
    
    def create_transparent_logo(self, opacity):
        """Create a transparent version of the logo with specified opacity"""
        try:
            # Load the original image
            img = Image.open(self.logo_file)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a new image with the same size
            transparent_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
            
            # Get pixel data
            data = img.getdata()
            new_data = []
            
            # Apply opacity to each pixel
            for item in data:
                if len(item) == 4:  # RGBA
                    # Keep RGB values, but multiply alpha by opacity
                    new_alpha = int(item[3] * opacity)
                    new_data.append((item[0], item[1], item[2], new_alpha))
                else:  # RGB
                    # Add alpha channel with opacity
                    new_alpha = int(255 * opacity)
                    new_data.append((item[0], item[1], item[2], new_alpha))
            
            transparent_img.putdata(new_data)
            
            # Save to temporary file
            temp_fd, temp_logo_path = tempfile.mkstemp(suffix='.png', prefix='logo_transparent_')
            os.close(temp_fd)
            transparent_img.save(temp_logo_path, 'PNG')
            self.temp_files.append(temp_logo_path)
            
            return temp_logo_path
            
        except Exception as e:
            print(f"Warning: Could not create transparent logo: {str(e)}")
            return self.logo_file  # Fallback to original
    
    def add_watermark_to_page(self, page, page_rect, start_y):
        """Add watermark logo to the page starting from specified line"""
        try:
            # Calculate watermark area (from start_y to bottom of page)
            watermark_area_height = page_rect.height - start_y
            
            if watermark_area_height <= 0:
                return  # No space for watermark
            
            # Create transparent version of the logo
            transparent_logo_path = self.create_transparent_logo(self.opacity.get())
            
            # Load and get image dimensions
            img = Image.open(transparent_logo_path)
            img_width, img_height = img.size
            
            # Calculate scaling to fit the watermark area while maintaining aspect ratio
            # Make watermark very large - 90% of page width and 90% of available height
            max_width = page_rect.width * 0.9  # 90% of page width (increased from 70%)
            max_height = watermark_area_height * 0.9  # 90% of available height (increased from 80%)
            
            scale_w = max_width / img_width
            scale_h = max_height / img_height
            scale = min(scale_w, scale_h)
            
            # Calculate final dimensions
            final_width = img_width * scale
            final_height = img_height * scale
            
            # Center the watermark horizontally and position it in the available vertical space
            x = (page_rect.width - final_width) / 2
            y = start_y + (watermark_area_height - final_height) / 2
            
            # Create rectangle for the watermark
            watermark_rect = fitz.Rect(x, y, x + final_width, y + final_height)
            
            # Insert the pre-processed transparent image
            page.insert_image(
                watermark_rect,
                filename=transparent_logo_path
            )
            
        except Exception as e:
            print(f"Warning: Could not add watermark: {str(e)}")
    
    def process_and_open_pdf(self):
        """Process PDF and open it temporarily"""
        temp_file_path = self.process_pdf(is_temp=True)
        if temp_file_path:
            if self.open_pdf_with_default_app(temp_file_path):
                # Start monitoring for when PDF is closed
                self.monitor_pdf_and_cleanup(temp_file_path)
                messagebox.showinfo(
                    "Success", 
                    "PDF processed and opened successfully!\n\nThe temporary file will be automatically deleted when you close the PDF viewer."
                )
    
    def process_and_save_pdf(self):
        """Process PDF and save it permanently"""
        # Ask for output location
        file_path = filedialog.asksaveasfilename(
            title="Save Output PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            result = self.process_pdf(output_path=file_path, is_temp=False)
            if result:
                messagebox.showinfo(
                    "Success", 
                    f"PDF processed and saved successfully!\n\nOutput saved to:\n{file_path}"
                )
    
    def run(self):
        self.root.mainloop()
        # Clean up any remaining temp files when GUI is closed
        self.cleanup_temp_files()

# Installation instructions and requirements check
def check_requirements():
    required_modules = ['fitz', 'PIL']
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'fitz':
                import fitz
            elif module == 'PIL':
                from PIL import Image
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("Missing required modules. Please install them using:")
        if 'fitz' in missing_modules:
            print("pip install PyMuPDF")
        if 'PIL' in missing_modules:
            print("pip install Pillow")
        return False
    return True

if __name__ == "__main__":
    if check_requirements():
        app = PDFMarginAdjuster()
        app.run()
    else:
        print("\nPlease install the required modules and run the script again.")