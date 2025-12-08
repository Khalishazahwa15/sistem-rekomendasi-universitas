# Linked List untuk riwayat rekomendasi (LIFO)
class RecommendationNode:
    def __init__(self, data):
        self.data = data # nama, kota, nilai, list_rekomendasi
        self.next = None

class RecommendationHistoryLinkedList:
    def __init__(self):
        self.head = None

    def push(self, data):
        node = RecommendationNode(data)
        node.next = self.head
        self.head = node

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result
      
