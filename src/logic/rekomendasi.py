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

        kota = kota_input.lower()

        # --- Tree: rekomendasi berdasarkan nilai ---
        rekom_nilai_list = search_threshold_tree(self.threshold_tree_root, nilai)

        # --- Graph + Queue: cari kota atau kota terdekat yang punya universitas ---
        rekom_kota_list = self.universitas_per_kota.get(kota, [])
        if not rekom_kota_list:
            rekom_kota_list = self.find_nearest_city_universities(kota)

        # --- Set: gabungkan & hilangkan duplikasi ---
        combined_set = set(rekom_nilai_list) | set(rekom_kota_list)
        combined_list = list(combined_set)

        # --- Priority Queue: urutkan berdasarkan “kecocokan” nilai ---
        pq = []
        for u in combined_list:
            # heuristik sederhana: kalau muncul di rekom_nilai_list dianggap target 90
            base = 90 if u in rekom_nilai_list else 75
            priority = abs(base - nilai)   # makin kecil makin prioritas
            heapq.heappush(pq, (priority, u))

        sorted_by_priority = []
        while pq:
            sorted_by_priority.append(heapq.heappop(pq)[1])

        # --- Sorting: urutkan alfabet tambahan ---
        sorted_alpha = sorted(combined_list)

        # --- Simpan ke Linked List (riwayat) ---
        self.rec_history_ll.push((nama, kota_input, nilai, sorted_by_priority))

        # --- Tampilkan hasil ---
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Halo {nama} dari {kota_input.capitalize()}!\n")
        self.output_text.insert(tk.END, f"Nilai rata-rata kamu: {nilai}\n\n")

        self.output_text.insert(tk.END, " Rekomendasi:\n")
        for u in sorted_by_priority:
            self.output_text.insert(tk.END, f"- {u}\n")

        self.output_text.insert(tk.END, "\n Universitas berdasarkan kota / kota terdekat:\n")
        for u in rekom_kota_list:
            self.output_text.insert(tk.END, f"- {u}\n")

        self.output_text.insert(tk.END, "\n🔤 Daftar universitas gabungan:\n")
        for u in sorted_alpha:
            self.output_text.insert(tk.END, f"- {u}\n")
