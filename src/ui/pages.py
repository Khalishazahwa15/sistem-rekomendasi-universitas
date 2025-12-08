import tkinter as tk
from tkinter import ttk, messagebox
from array import array

from src.logic.linked_list import RecommendationHistoryLinkedList
from src.logic.tree_threshold import build_threshold_tree
from src.logic.graph_bfs import find_nearest_city_universities
from src.logic.rekomendasi import get_rekomendasi
from src.logic.undo_stack import UndoStack

from src.data.universitas import universitas_per_kota
from src.data.kota_graph import kota_graph


class RekomendasiUniversitasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Rekomendasi Universitas + Struktur Data")

        # styling
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure("TFrame", background="#f4f4f4")
        style.configure("TLabel", background="#f4f4f4", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure(
            "Title.TLabel",
            background="#2c3e50",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )
        self.root.configure(bg="#dfe6e9")

        # Data
        self.universitas_per_kota = universitas_per_kota
        self.kota_graph = kota_graph

        # Struktur Data
        self.threshold_tree_root = build_threshold_tree()
        self.rec_history_ll = RecommendationHistoryLinkedList()
        self.nilai_history_array = array('f')
        self.undo_stack = UndoStack()

        self.edit_item = None

        self.setup_ui()

    # == UI ==
    def setup_ui(self):
        container = ttk.Frame(self.root, padding=10)
        container.grid(row=0, column=0, sticky="nsew")

        self.notebook = ttk.Notebook(container)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.page_input = ttk.Frame(self.notebook, padding=15)
        self.page_rekom = ttk.Frame(self.notebook, padding=15)
        self.page_riwayat = ttk.Frame(self.notebook, padding=15)

        self.notebook.add(self.page_input, text="Input Data")
        self.notebook.add(self.page_rekom, text="Rekomendasi")
        self.notebook.add(self.page_riwayat, text="Riwayat Data")

        self.build_input_page()
        self.build_rekom_page()
        self.build_riwayat_page()

    def build_input_page(self):
        frame = self.page_input

        ttk.Label(frame, text="Form Input Calon Mahasiswa", style="Title.TLabel",
                  anchor="w").grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 10))

        ttk.Label(frame, text="Nama").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.nama_entry = ttk.Entry(frame, width=30)
        self.nama_entry.grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(frame, text="Asal Kota").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.kota_entry = ttk.Entry(frame, width=30)
        self.kota_entry.grid(row=2, column=1, sticky="w", pady=3)

        ttk.Label(frame, text="Nilai Rata-rata").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.nilai_entry = ttk.Entry(frame, width=30)
        self.nilai_entry.grid(row=3, column=1, sticky="w", pady=3)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")
        btn_frame.columnconfigure((0, 1, 2), weight=1)

        self.simpan_button = ttk.Button(btn_frame, text="Simpan Data", command=self.simpan_data)
        self.simpan_button.grid(row=0, column=0, padx=5, sticky="we")

        ttk.Button(btn_frame, text="Dapatkan Rekomendasi",
                   command=self.btn_rekomendasi_clicked).grid(row=0, column=1, padx=5, sticky="we")

        ttk.Button(btn_frame, text="Undo Simpan",
                   command=self.undo_last).grid(row=0, column=2, padx=5, sticky="we")

    def build_rekom_page(self):
        frame = self.page_rekom

        ttk.Label(frame, text="Hasil Rekomendasi Universitas", style="Title.TLabel",
                  anchor="w").grid(row=0, column=0, sticky="we", pady=(0, 10))

        self.output_text = tk.Text(frame, width=70, height=18, font=("Consolas", 10))
        self.output_text.grid(row=1, column=0, sticky="nsew")

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Lihat Riwayat Rekomendasi",
                   command=self.show_history_linked_list).grid(row=2, column=0, pady=10, sticky="we")

    def build_riwayat_page(self):
        frame = self.page_riwayat
        ttk.Label(frame, text="Riwayat Data Calon Mahasiswa", style="Title.TLabel",
                  anchor="w").grid(row=0, column=0, columnspan=3, sticky="we", pady=(0, 10))

        columns = ("nama", "kota", "nilai")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        self.tree.heading("nama", text="Nama")
        self.tree.heading("kota", text="Kota")
        self.tree.heading("nilai", text="Nilai")
        self.tree.column("nama", width=150)
        self.tree.column("kota", width=150)
        self.tree.column("nilai", width=80, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns")

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure((0, 1), weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")
        btn_frame.columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="Edit", command=self.edit_data).grid(row=0, column=0, padx=5, sticky="we")
        ttk.Button(btn_frame, text="Delete", command=self.delete_data).grid(row=0, column=1, padx=5, sticky="we")

    # = CRUD + UNDO STACK =
    def simpan_data(self):
        nama = self.nama_entry.get().strip()
        kota = self.kota_entry.get().strip()
        nilai_str = self.nilai_entry.get().strip()

        if not nama or not kota or not nilai_str:
            messagebox.showwarning("Input Salah", "Semua kolom harus diisi.")
            return

        try:
            float(nilai_str)
        except ValueError:
            messagebox.showwarning("Input Salah", "Nilai harus berupa angka.")
            return

        record = (nama, kota, nilai_str)

        if self.edit_item is None:
            item_id = self.tree.insert("", "end", values=record)
            self.undo_stack.push(("insert", item_id))
        else:
            old_values = self.tree.item(self.edit_item, "values")
            self.tree.item(self.edit_item, values=record)
            self.undo_stack.push(("update", self.edit_item, old_values))

            self.edit_item = None
            self.simpan_button.config(text="Simpan Data")

        self.nilai_history_array.append(float(nilai_str))
        messagebox.showinfo("Sukses", "Data berhasil disimpan.")

    def undo_last(self):
        if self.undo_stack.is_empty():
            messagebox.showinfo("Kembali", "Tidak ada aksi yang bisa dikembalikan")
            return

        action = self.undo_stack.pop()
        kind = action[0]

        if kind == "insert":
            item_id = action[1]
            if self.tree.exists(item_id):
                self.tree.delete(item_id)

        elif kind == "update":
            item_id, old_values = action[1], action[2]
            if self.tree.exists(item_id):
                self.tree.item(item_id, values=old_values)

        elif kind == "delete":
            values = action[1]
            self.tree.insert("", "end", values=values)

    def edit_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Silakan pilih data di tabel dulu.")
            return

        item = selected[0]
        nama, kota, nilai = self.tree.item(item, "values")

        self.nama_entry.delete(0, tk.END); self.nama_entry.insert(0, nama)
        self.kota_entry.delete(0, tk.END); self.kota_entry.insert(0, kota)
        self.nilai_entry.delete(0, tk.END); self.nilai_entry.insert(0, nilai)

        self.edit_item = item
        self.simpan_button.config(text="Update Data")
        self.notebook.select(self.page_input)

    def delete_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Silakan pilih data di tabel dulu.")
            return

        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return

        for item in selected:
            values = self.tree.item(item, "values")
            self.undo_stack.push(("delete", values))
            self.tree.delete(item)

        messagebox.showinfo("Sukses", "Data berhasil dihapus.")

    # ===================== NAVIGASI DARI RIWAYAT =====================
    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = selected[0]
        nama, kota, nilai = self.tree.item(item, "values")

        self.nama_entry.delete(0, tk.END); self.nama_entry.insert(0, nama)
        self.kota_entry.delete(0, tk.END); self.kota_entry.insert(0, kota)
        self.nilai_entry.delete(0, tk.END); self.nilai_entry.insert(0, nilai)

        self.rekomendasi(from_tree=True)
        self.notebook.select(self.page_rekom)

    def btn_rekomendasi_clicked(self):
        self.rekomendasi(from_tree=False)
        self.notebook.select(self.page_rekom)

    #  LOGIKA REKOMENDASI 
    def rekomendasi(self, from_tree=False):
        nama = self.nama_entry.get().strip()
        kota_input = self.kota_entry.get().strip()
        nilai_str = self.nilai_entry.get().strip()

        if not nama or not kota_input or not nilai_str:
            if not from_tree:
                messagebox.showwarning("Input Salah", "Semua kolom harus diisi.")
            return

        try:
            nilai = float(nilai_str)
        except ValueError:
            if not from_tree:
                messagebox.showwarning("Input Salah", "Nilai harus berupa angka.")
            return

        rekom_nilai_list, rekom_kota_list, sorted_by_priority, sorted_alpha = get_rekomendasi(
            nilai=nilai,
            kota_input=kota_input,
            threshold_tree_root=self.threshold_tree_root,
            universitas_per_kota=self.universitas_per_kota,
            kota_graph=self.kota_graph,
            bfs_func=find_nearest_city_universities
        )

        # simpan riwayat ke Linked List
        self.rec_history_ll.push((nama, kota_input, nilai, sorted_by_priority))

        # tampilkan output
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Halo {nama} dari {kota_input.capitalize()}!\n")
        self.output_text.insert(tk.END, f"Nilai rata-rata kamu: {nilai}\n\n")

        self.output_text.insert(tk.END, " Rekomendasi :\n")
        for u in sorted_by_priority:
            self.output_text.insert(tk.END, f"- {u}\n")

        self.output_text.insert(tk.END, "\n Universitas berdasarkan kota / kota terdekat:\n")
        for u in rekom_kota_list:
            self.output_text.insert(tk.END, f"- {u}\n")

        self.output_text.insert(tk.END, "\n Daftar universitas gabungan :\n")
        for u in sorted_alpha:
            self.output_text.insert(tk.END, f"- {u}\n")

    def show_history_linked_list(self):
        history = self.rec_history_ll.to_list()
        if not history:
            messagebox.showinfo("Riwayat", "Belum ada riwayat rekomendasi.")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Riwayat rekomendasi :\n\n")
        for nama, kota, nilai, rekom_list in history:
            self.output_text.insert(tk.END, f"Nama: {nama}, Kota: {kota}, Nilai: {nilai}\n")
            self.output_text.insert(tk.END, "Rekomendasi: " + ", ".join(rekom_list) + "\n\n")
