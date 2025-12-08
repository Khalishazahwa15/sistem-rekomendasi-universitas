class ThresholdNode:
    def __init__(self, threshold, universities):
        self.threshold = threshold
        self.universities = universities
        self.left = None
        self.right = None

def build_threshold_tree():
    node0 = ThresholdNode(0, ["Telkom University", "BINUS University", "UMN"])
    node70 = ThresholdNode(70, ["UPN Veteran", "UIN", "Politeknik Negeri"])
    node80 = ThresholdNode(80, ["Universitas Lampung (UNILA)",
                                "Universitas Brawijaya (UB)",
                                "Universitas Diponegoro (UNDIP)",
                                "Universitas Sebelas Maret (UNS)"])
    node90 = ThresholdNode(90, ["Universitas Indonesia (UI)",
                                "Institut Teknologi Bandung (ITB)",
                                "Universitas Gadjah Mada (UGM)"])

    node70.left = node0
    node80.left = node70
    node80.right = node90

    return node80

def search_threshold_tree(node, nilai):
    if node is None:
        return []

    if nilai < node.threshold:
        return search_threshold_tree(node.left, nilai) if node.left else node.universities

    if node.right and nilai >= node.right.threshold:
        return search_threshold_tree(node.right, nilai)

    return node.universities
