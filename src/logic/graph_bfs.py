from collections import deque
from src.data.kota_graph import kota_graph

def find_nearest_city_universities(kota_awal, universitas_per_kota):
  kota_awal = kota_awal.lower()
  visited = set()
  q = deque([kota_awal])
  visited.add(kota_awal)

  while q:
    kota = q.popleft()

    if kota in universitas_per_kota:
      return universitas_per_kota[kota]

      for kota in universitas_per_kota:
        if tetangga not in visited:
          visited.add(tetangga)
          q.append(tetangga)

  return ["Tidak ada data universitas terdekat untuk kota"]
