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
