import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import os

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)
        load_columns()

def load_columns():
    folder_path = folder_entry.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("错误", "请选择一个有效的文件夹")
        return

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not csv_files:
        messagebox.showinfo("信息", "文件夹中没有CSV文件")
        return

    # 读取第一个CSV文件的表头
    file_path = os.path.join(folder_path, csv_files[0])
    df = pd.read_csv(file_path)
    columns = list(df.columns)

    # 清除旧的复选框
    for widget in columns_frame.winfo_children():
        widget.destroy()

    # 创建新的复选框
    global check_vars
    check_vars = []
    for col in columns:
        var = tk.BooleanVar()
        check = tk.Checkbutton(columns_frame, text=col, variable=var)
        check.pack(anchor='w')
        check_vars.append((col, var))

    analyze_button.config(state=tk.NORMAL)

def save_results(df):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        messagebox.showinfo("保存成功", f"结果已保存到 {save_path}")

def analyze_csv_files():
    folder_path = folder_entry.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("错误", "请选择一个有效的文件夹")
        return

    selected_columns = [col for col, var in check_vars if var.get()]
    if not selected_columns:
        messagebox.showerror("错误", "请选择至少一个列进行分析")
        return

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not csv_files:
        messagebox.showinfo("信息", "文件夹中没有CSV文件")
        return

    analysis_results = []

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)

        # 检查用户选择的列是否存在
        for col in selected_columns:
            if col not in df.columns:
                messagebox.showerror("错误", f"列 {col} 不存在于文件 {csv_file} 中")
                return

        sub_df = df[selected_columns]

        # 进行统计性分析
        result = {
            '文件名': csv_file,
            '行数': len(sub_df),
            '列数': len(sub_df.columns),
            '缺失值总数': sub_df.isnull().sum().sum()
        }
        for col in sub_df.columns:
            result[f'{col}_均值'] = sub_df[col].mean() if sub_df[col].dtype in ['float64', 'int64'] else 'N/A'
            result[f'{col}_中位数'] = sub_df[col].median() if sub_df[col].dtype in ['float64', 'int64'] else 'N/A'
            result[f'{col}_标准差'] = sub_df[col].std() if sub_df[col].dtype in ['float64', 'int64'] else 'N/A'

        analysis_results.append(result)

    analysis_df = pd.DataFrame(analysis_results)

    # 显示分析结果
    result_window = tk.Toplevel()
    result_window.title("分析结果")

    result_frame = tk.Frame(result_window)
    result_frame.pack(expand=True, fill='both')

    cols = list(analysis_df.columns)
    tree = ttk.Treeview(result_frame, columns=cols, show='headings')

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    for _, row in analysis_df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill='both')

    # 添加导出按钮
    save_button = tk.Button(result_window, text="导出结果", command=lambda: save_results(analysis_df))
    save_button.pack(pady=10)

# 创建主窗口
root = tk.Tk()
root.title("量测统计")

# 创建选择文件夹部分
folder_frame = tk.Frame(root)
folder_frame.pack(pady=10)

folder_label = tk.Label(folder_frame, text="选择文件夹:")
folder_label.pack(side=tk.LEFT)

folder_entry = tk.Entry(folder_frame, width=50)
folder_entry.pack(side=tk.LEFT)

folder_button = tk.Button(folder_frame, text="浏览", command=select_folder)
folder_button.pack(side=tk.LEFT)

# 创建列选择部分
columns_frame = tk.Frame(root)
columns_frame.pack(pady=10)

columns_label = tk.Label(columns_frame, text="选择要分析的列:")
columns_label.pack(anchor='w')

# 创建分析按钮
analyze_button = tk.Button(root, text="分析CSV文件", command=analyze_csv_files)
analyze_button.pack(pady=10)
analyze_button.config(state=tk.DISABLED)

# 显示版权信息
copyright_label = tk.Label(root, text="© 2024 AMEC SIMULATION & CONTROL", font=("Arial", 8))
copyright_label.pack(side=tk.BOTTOM, pady=5)

# 运行主循环
root.mainloop()
