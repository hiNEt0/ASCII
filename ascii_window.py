import tkinter as tk
from tkinter import messagebox


class TextFileViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ASCII result")
        self.geometry("800x600")
        self.resizable(False, False)

        self.font_size = 12
        self.text_widget = tk.Text(self, font=("Courier", self.font_size))
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_widget)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_widget.yview)

        self.scrollbar_x = tk.Scrollbar(self.text_widget, orient="horizontal")
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_widget.config(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.text_widget.xview)

        self.button_font_inc = tk.Button(self, text="A^", command=self.increase_font_size)
        self.button_font_inc.place(x=10, y=574)

        self.button_font_red = tk.Button(self, text="a˅", command=self.reduce_font_size)
        self.button_font_red.place(x=47, y=574)

        self.button_copy = tk.Button(self, text="Copy text", command=self.copy_file)
        self.button_copy.pack(side=tk.BOTTOM)

    def open_file(self, file_path):
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)

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
