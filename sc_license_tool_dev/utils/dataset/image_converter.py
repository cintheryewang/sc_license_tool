#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   image_converter.py
@Project :   
@Time    :   2024/5/31 上午9:19 
@Author  :   Yifei WANG
@Version :   1.0.0
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :   
"""


import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
import os

# Flag to indicate if the process should be canceled
cancel_conversion = False


def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.tif *.tiff")])
    if file_path:
        input_path.set(file_path)


def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        input_path.set(folder_path)


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path.set(folder_path)


def drop(event):
    input_path.set(event.data)


def start_conversion():
    global cancel_conversion
    cancel_conversion = False
    convert_image()


def cancel_conversion_process():
    global cancel_conversion
    cancel_conversion = True


def convert_image():
    global cancel_conversion
    in_path = input_path.get()
    out_format = format_var.get()
    out_dir = output_path.get() or None
    if not in_path:
        messagebox.showerror("Error", "Please select an input image file or folder")
        return
    if not out_format:
        messagebox.showerror("Error", "Please select an output format")
        return

    if os.path.isdir(in_path):
        files_to_convert = []
        for root, _, files in os.walk(in_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff')):
                    files_to_convert.append(os.path.join(root, file))
        if files_to_convert:
            progress_bar["maximum"] = len(files_to_convert)
            for idx, file_path in enumerate(files_to_convert):
                if cancel_conversion:
                    messagebox.showinfo("Cancelled", "Conversion process was cancelled")
                    break
                convert_single_image(file_path, out_format, out_dir)
                progress_bar["value"] = idx + 1
                app.update_idletasks()
            else:
                messagebox.showinfo("Success", "All images successfully converted")
        else:
            messagebox.showinfo("Info", "No image files found in the selected folder")
    else:
        convert_single_image(in_path, out_format, out_dir)
        messagebox.showinfo("Success", f"Image successfully converted to {out_format}")


def convert_single_image(file_path, out_format, out_dir):
    try:
        img = Image.open(file_path)
        output_dir = out_dir or os.path.dirname(file_path)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}.{out_format}")
        img.save(output_file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert image {file_path}: {str(e)}")


app = TkinterDnD.Tk()
app.title("Image Format Converter")

input_path = tk.StringVar()
output_path = tk.StringVar()
format_var = tk.StringVar(value="png")

tk.Label(app, text="Input Image or Folder:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=input_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Select File", command=select_file).grid(row=0, column=2, padx=10, pady=10)
tk.Button(app, text="Select Folder", command=select_folder).grid(row=0, column=3, padx=10, pady=10)

tk.Label(app, text="Output Format:").grid(row=1, column=0, padx=10, pady=10)
tk.Radiobutton(app, text="JPEG", variable=format_var, value="jpg").grid(row=1, column=1, sticky=tk.W)
tk.Radiobutton(app, text="PNG", variable=format_var, value="png").grid(row=1, column=1)
tk.Radiobutton(app, text="TIFF", variable=format_var, value="tif").grid(row=1, column=1, sticky=tk.E)

tk.Label(app, text="Output Directory (Optional):").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=output_path, width=50).grid(row=2, column=1, padx=10, pady=10)
tk.Button(app, text="Browse...", command=select_output_folder).grid(row=2, column=2, padx=10, pady=10)

tk.Button(app, text="Convert", command=start_conversion).grid(row=3, column=1, pady=10)
tk.Button(app, text="Cancel", command=cancel_conversion_process).grid(row=3, column=2, pady=10)

progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=4, pady=10)

app.drop_target_register(DND_FILES)
app.dnd_bind('<<Drop>>', drop)

app.mainloop()
