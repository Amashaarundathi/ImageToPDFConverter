import tkinter as tk
from tkinter import filedialog, messagebox
import os, random, string
from PIL import Image  # pip install pillow

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.files = []
        self.pdf_name = tk.StringVar()

        # === COLORS ===
        self.blue = "#0078D7"       # Windows blue
        self.button_blue = "#0094FF"  # lighter blue for buttons

        # === HEADER FRAME === (taller for buttons)
        header_frame = tk.Frame(root, bg=self.blue, height=120)
        header_frame.pack(fill=tk.X)

        # Title label
        tk.Label(header_frame,
                 text="Image to PDF Converter",
                 font=("Helvetica", 16, "bold"),
                 bg=self.blue, fg="white").pack(pady=(10, 5))

        # Select Images button (moved to header)
        tk.Button(header_frame, text="Select Images",
                  command=self.select_images,
                  bg=self.button_blue, fg="white").pack(pady=(0, 10))

        # === BODY FRAME ===
        body_frame = tk.Frame(root, bg="white")
        body_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(body_frame, selectmode=tk.MULTIPLE)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # === BOTTOM FRAME ===
        bottom_frame = tk.Frame(root, bg=self.blue)
        bottom_frame.pack(fill=tk.X)

        tk.Label(bottom_frame, text="Output PDF name:",
                 bg=self.blue, fg="white").pack(pady=(10, 0))
        tk.Entry(bottom_frame, textvariable=self.pdf_name).pack(
            pady=5, fill=tk.X, padx=10)

        tk.Button(bottom_frame, text="Convert to PDF",
                  command=self.convert_to_pdf,
                  bg=self.button_blue, fg="white").pack(pady=10)

    def select_images(self):
        ft = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
        names = filedialog.askopenfilenames(title="Select Images", filetypes=ft)
        if names:
            self.files = names
            self.listbox.delete(0, tk.END)
            for f in names:
                self.listbox.insert(tk.END, os.path.basename(f))

    def convert_to_pdf(self):
        if not self.files:
            messagebox.showerror("Error", "No images selected!")
            return

        # if name blank, generate random name
        name = self.pdf_name.get().strip()
        if not name:
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            name = f"output_{rand}"

        # ask user where to save
        save_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            initialfile=name + ".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not save_path:
            return

        images = []
        for f in self.files:
            img = Image.open(f)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)

        try:
            images[0].save(save_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Success", f"PDF saved as:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image to PDF")
    root.geometry("400x550")
    ImageToPDFConverter(root)
    root.mainloop()
