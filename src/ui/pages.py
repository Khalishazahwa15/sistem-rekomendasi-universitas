import tkinter as tk
from tkinter import ttk, messagebox

from src.logic_linked_list import RecommendationHistoryLinkedList
from src.logic.undo_stack import Undostcak
from src.logic.tree_threshold import build_threshold_tree, search_threshold_tree
from src.logic.graph_bfs import find_nearest_city_universities
from src.data.universitas import UNIVERSITAS_PER_KOTA

class Mainpage:
  def __init__(self, root):
    self.root = root
    self.root.title("Sistem Rekomendasi Universiras")

    self.history = RecomendationHistoryLinkedList()
    self.undo_stack = UndoStack()
    self.tree_root = build_threshold_tree()

    self.setup_ui()

  def setup_ui(self):
    ttk.Label(self.root, text = "Nilai Anda:", font=("Arial", 12)).pack()
    self.nilai_entry = ttk.Entry(self.root)
    self.nilai_entry.pack()
    ttk.Label(self.root, text="Kota Anda:", font=("Arial", 12)).pack()
    self.kota_entry = ttk.Entry(self.root)
    self.kota_entry.pack()
    ttk_Button(self_root, text = "Cari Rekomendasi",command = self.get_recommedation).pack(padt=10)
    ttk.Button(self.root, text = "Undo", command = self.undo_action).pack()

    self.output = tk.Text(self.root, height = 10, width = 50)
    self.output.pack()

  def get_recommendation(self):
    try:
      nilai = int(self.nilai_entry.get())
    except: 
      messagebox.showerror("Error", "Nilai harus angka!")
      return
      
    kota = self.kota_entry.get().lower()

    by_nilai = search_threshold_tree(self.tree_root, nilai)
    by_kota = find_nearest_city_universities(kota, UNIVERSITAS_PER_KOTA)

    hasil = f"Rekomendasi Berdasarkan Nilai: {by_nilai}\n"
    hasil += f"Rekomendasi Berdasarkan Kota Terdekat: {by_kota}\n"

    self.output.insert(tk.END, hasil + "\n")

    self.history.push(hasil)
    self.undo_stack.push(hasil)

  def undo_action(self):
    if self.undo_stack.is_empty():
      messagebox.showinfo("Undo", "Tidak ada tindakan yang bisa di-undo.")
      return

    self.undo_stack.pop()
    self.output.delete("1.0", tk.END)

    history_list = self.history.to_list()
    for item in history_list[::-1]:
      self.output.insert(tk.END, item+"\n")

  
