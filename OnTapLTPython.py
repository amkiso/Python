import re
import os, sys
import tkinter as tk
from tkinter import END, Button, filedialog, messagebox, Scrollbar, ttk
import json

global QL_NV, tree, file_data
file_data = "Nhanvien.json"

class Nhanvien:
    def __init__(self, ma_nv, ten_nv, pban, email):
        self.ma_nv = ma_nv
        self.ten_nv = ten_nv
        self.pban = pban
        self.email = email

    def to_dict(self):
        return {
            "ma_nv": self.ma_nv,
            "ten_nv": self.ten_nv,
            "pban": self.pban,
            "email": self.email
        }

class quanlynhanvien:
    def __init__(self, file_name):
        self.file_name = file_name

    def file_read(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    Nhan_vien = []
                    for d in data:
                        Nhan_vien.append(Nhanvien(
                            d.get("ma_nv", ""),
                            d.get("ten_nv", ""),
                            d.get("pban", ""),
                            d.get("email", "")
                        ))
                except json.JSONDecodeError:
                    return []
                except FileNotFoundError:
                    return []
                return Nhan_vien
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file: {e}")
            return []

    def file_save(self, ds_nhanvien):
        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                data = [nv.to_dict() for nv in ds_nhanvien]
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu file: {e}")
            return False
        return True

def Them_nhan_vien(current_windows, tree, QL_NV):
    add_windows = tk.Toplevel(current_windows)
    add_windows.geometry("350x250")
    add_windows.title("Thêm nhân viên")
    add_windows.configure(bg="lightblue")

    tk.Label(add_windows, text="Mã nhân viên:", bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_ma = tk.Entry(add_windows)
    entry_ma.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_windows, text="Tên nhân viên:", bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_ten = tk.Entry(add_windows)
    entry_ten.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_windows, text="Phòng ban:", bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_pban = tk.Entry(add_windows)
    entry_pban.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_windows, text="Email:", bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_email = tk.Entry(add_windows)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    def save_nv():
        ma_nv = entry_ma.get().strip()
        ten_nv = entry_ten.get().strip()
        pban = entry_pban.get().strip()
        email = entry_email.get().strip()

        if not ma_nv or not ten_nv or not pban or not email:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showwarning("Lỗi", "Email không hợp lệ.")
            return

        ds_nv = QL_NV.file_read()
        if any(nv.ma_nv == ma_nv for nv in ds_nv):
            messagebox.showwarning("Trùng mã", "Mã nhân viên đã tồn tại.")
            return

        nv = Nhanvien(ma_nv, ten_nv, pban, email)
        ds_nv.append(nv)
        if QL_NV.file_save(ds_nv):
            messagebox.showinfo("Thành công", "Đã thêm nhân viên mới.")
            add_windows.destroy()
            load_NV()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu nhân viên.")

    tk.Button(add_windows, text="Lưu", command=save_nv, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=15)

def load_NV():
    global QL_NV, tree, file_data
    QL_NV = quanlynhanvien(file_data)
    tree.delete(*tree.get_children())
    Nhan_Vien = QL_NV.file_read()
    for nv in Nhan_Vien:
        tree.insert("", "end", values=(nv.ma_nv, nv.ten_nv, nv.pban, nv.email))

def show_gui():
    global tree, QL_NV
    root = tk.Tk()
    root.title("Quản lý nhân viên")
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", padx=10, pady=5)
    tk.Button(button_frame, text="Tìm kiếm").pack(side="left", padx=5, pady=5)
    tk.Entry(button_frame).pack(side="left", fill="x", padx=5, pady=5)
    tk.Button(button_frame, text="Xóa").pack(side="right", padx=5, pady=5)
    tk.Button(button_frame, text="sắp xếp").pack(side="right", padx=5, pady=5)
    tk.Button(button_frame, text="lọc").pack(side="right", padx=5, pady=5)
    tk.Button(button_frame, text="Tải lại", command=lambda: load_NV()).pack(side="right", padx=5, pady=5)
    tk.Button(button_frame, text="Thêm", command=lambda: Them_nhan_vien(root, tree, QL_NV)).pack(side="right", padx=5, pady=5)
    tk.Button(button_frame, text="Sửa").pack(side="right", padx=5, pady=5)
    tree = ttk.Treeview(root, columns=("ma", "ten", "pban", "email"), show="headings")
    tree.heading("ma", text="Mã nhân viên")
    tree.heading("ten", text="Tên nhân viên")
    tree.heading("pban", text="Phòng ban")
    tree.heading("email", text="Email")
    tree.pack(fill=tk.BOTH, expand=True)

    load_NV()
    root.mainloop()

if __name__ == "__main__":
    show_gui()