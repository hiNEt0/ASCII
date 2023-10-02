import tkinter as tk
from tkinter import messagebox


class TextFileViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ASCII result")
        self.geometry("800x600")

        self.font_size = 12
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self.text_widget = tk.Text(self, font=("Courier", self.font_size))
        self.text_widget.grid(row=0, column=0, sticky='nsew')

        self.scrollbar = tk.Scrollbar(self.text_widget)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_widget.yview)

        self.scrollbar_x = tk.Scrollbar(self.text_widget, orient="horizontal")
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_widget.config(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.text_widget.xview)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, sticky='sw')

        self.button_font_inc = tk.Button(self.button_frame, text="A^", command=self.increase_font_size)
        self.button_font_inc.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_font_red = tk.Button(self.button_frame, text="a˅", command=self.reduce_font_size)
        self.button_font_red.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_copy = tk.Button(self.button_frame, text="Copy text", command=self.copy_file)
        self.button_copy.pack(side=tk.LEFT, padx=5, pady=5)

    def print_text(self, text):
        self.text_widget.insert(tk.END, text)

    def increase_font_size(self):
        self.font_size += 2
        self.text_widget.config(font=("Courier", self.font_size))

    def reduce_font_size(self):
        if self.font_size >= 3:
            self.font_size -= 2
            self.text_widget.config(font=("Courier", self.font_size))

    def copy_file(self):
        content = self.text_widget.get(1.0, tk.END)
        try:
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("Copy File", "File copied to clipboard")
        except tk.TclError:
            messagebox.showinfo("Copy File", "Failed to copy file")