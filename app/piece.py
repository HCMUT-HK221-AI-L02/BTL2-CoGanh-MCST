# Định nghĩa một quân cờ, có màu, tọa độ, nước đi có thể đi
class Piece:
    def __init__(self, team, pos):
        self.team = team
        self.pos = pos
        # posibleMove là danh sách các tuple, mỗi tuple là một move có thể đi
        self.posibleMove = []