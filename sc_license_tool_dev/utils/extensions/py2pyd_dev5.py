#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   py2pyd_dev4.py
@Project :   
@Time    :   2024/1/30 9:12 
@Author  :   Yifei WANG
@Version :   
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :   
"""

import os
import tempfile
import tkinter as tk
from tkinter import filedialog, Label, Button, StringVar
from distutils.core import setup
from Cython.Build import cythonize
import shutil
import glob
import functools
import traceback

import sys
sys.setrecursionlimit(3000)


def catch_and_log(func):
    """A decorator that catches and logs exceptions in a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 获取完整的错误堆栈信息
            error_info = traceback.format_exc()
            print(f"Exception occurred in function {func.__name__}\n{error_info}")
            # 可以选择重新抛出异常或返回一个错误值
            # raise  # 可选：重新抛出异常
            # return -1  # 或返回特定的值
    return wrapper


@catch_and_log
def find_pyd_file(directory, module_name):
    try:
        for file in glob.glob(os.path.join(directory, module_name + ".*.pyd")):
            if module_name in file:
                print(">>> Found file: " + file)
                return file
        return None
    except Exception as e:
        print(f"Error in find_pyd_file: {e}")
        return None


@catch_and_log
def py_to_pyd(py_file, output_dir):
    base_name = os.path.basename(py_file)
    module_name, _ = os.path.splitext(base_name)

    abs_py_file = os.path.abspath(py_file)
    abs_output_dir = os.path.abspath(output_dir)

    # 保存当前工作目录
    original_cwd = os.getcwd()

    # 使用临时目录进行编译
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_py_file = os.path.join(tmp_dir, base_name)
        shutil.copy2(abs_py_file, temp_py_file)

        # 设置临时工作目录
        os.chdir(tmp_dir)

        try:
            setup(
                ext_modules=cythonize(temp_py_file),
                script_args=["build_ext", "--inplace"]
            )

            pyd_file = find_pyd_file(tmp_dir, module_name)
            if not pyd_file:
                print(f"Error: Unable to find a .pyd file for {module_name}")
                return

            if not os.path.exists(abs_output_dir):
                os.makedirs(abs_output_dir)

            output_pyd_file = os.path.join(abs_output_dir, os.path.basename(pyd_file))
            shutil.copy2(pyd_file, output_pyd_file)

        finally:
            # 恢复原始工作目录
            os.chdir(original_cwd)

    print(f"{py_file} has been compiled to .pyd and moved to {output_pyd_file}")


def browse_files():
    filenames = filedialog.askopenfilenames(
        title="Select Python files",
        filetypes=[("Python files", "*.py")]
    )
    if filenames:
        input_path.set(';'.join(filenames))


def browse_folder():
    foldername = filedialog.askdirectory(title="Select a Folder")
    if foldername:
        output_path.set(foldername)


def on_run():
    py_files = input_path.get().split(';')
    for py_file in py_files:
        py_to_pyd(py_file, output_path.get())


# 创建主窗口
root = tk.Tk()
root.title("Py to Pyd Converter")

# 设置输入输出路径变量
input_path = StringVar()
output_path = StringVar()

# 创建和放置窗口组件
Label(root, text="Input Python Files:").grid(row=0, column=0, sticky='w')
input_entry = tk.Entry(root, textvariable=input_path, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_files).grid(row=0, column=2)

Label(root, text="Output Directory:").grid(row=1, column=0, sticky='w')
output_entry = tk.Entry(root, textvariable=output_path, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_folder).grid(row=1, column=2)

run_button = Button(root, text="Run", command=on_run)
run_button.grid(row=2, column=1, pady=10)

# 启动事件循环
root.mainloop()
