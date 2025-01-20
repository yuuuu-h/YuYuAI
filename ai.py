def can_place_x_y(board, stone, x, y):
    """
    指定した位置 (x, y) に stone を配置できるか判定する関数。
    """
    if board[y][x] != 0:
        return False
    
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        has_opponent_stone = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if board[ny][nx] == opponent:
                has_opponent_stone = True
            elif board[ny][nx] == stone:
                if has_opponent_stone:
                    return True
                break
            else:
                break
            nx += dx
            ny += dy
    return False

def can_place(board, stone):
    """
    盤面に stone を置ける場所があるか確認。
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

class DreamAI:
    def __init__(self, depth=3):
        self.depth = depth

    def face(self):
        return "\ud83d\udc7e"

    def place(self, board, stone):
        best_move = None
        best_score = float('-inf')

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    new_board = [row[:] for row in board]
                    new_board[y][x] = stone
                    flip_stones(new_board, stone, x, y)
                    
                    score = minimax(new_board, self.depth, False, stone)
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        
        return best_move
