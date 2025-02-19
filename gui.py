import tkinter as tk
from tkinter import simpledialog, messagebox
import re

def select_month_gui():
    root = tk.Tk()
    root.withdraw()
    while True:
        selected_month = simpledialog.askstring("年月選択", "選択したい年月を入力してください (例: 2025-05):")
        if selected_month is None:
            return None
        if re.match(r'^\d{4}-\d{2}$', selected_month):
            return selected_month
        messagebox.showerror("エラー", "正しい形式で年月を入力してください (例: 2025-05)")
