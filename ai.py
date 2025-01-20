import math
from kogi_canvas.othello import play_othello

class DreamAI:
    def __init__(self, depth=3):
        """
        depth: 先読みの深さ
        """
        self.depth = depth

    def face(self):
        return "👾"

    def place(self, board, stone):
        """
        ミニマックス法で最適な手を計算する。
        """
        best_move = None
        best_score = float('-inf')

        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    # 仮想的に石を置く
                    new_board = [row[:] for row in board]
                    new_board[y][x] = stone
                    self.flip_stones(new_board, stone, x, y)

                    # ミニマックスでスコアを計算
                    score = self.minimax(new_board, self.depth, False, stone)
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def minimax(self, board, depth, maximizing, stone):
        """
        ミニマックス法を使って局面を評価する。
        """
        if depth == 0 or (not self.can_place(board, 1) and not self.can_place(board, 2)):
            return self.evaluate(board, stone)

        opponent = 3 - stone
        if maximizing:
            max_eval = float('-inf')
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if self.can_place_x_y(board, stone, x, y):
                        new_board = [row[:] for row in board]
                        new_board[y][x] = stone
                        self.flip_stones(new_board, stone, x, y)

                        eval = self.minimax(new_board, depth - 1, False, stone)
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if self.can_place_x_y(board, opponent, x, y):
                        new_board = [row[:] for row in board]
                        new_board[y][x] = opponent
                        self.flip_stones(new_board, opponent, x, y)

                        eval = self.minimax(new_board, depth - 1, True, stone)
                        min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self, board, stone):
        """
        評価関数: ボード上の位置に基づいて評価を行う。
        """
        evaluation_map = [
            [100, -20, 10, 10, -20, 100],
            [-20, -50, -2, -2, -50, -20],
            [10, -2, 0, 0, -2, 10],
            [10, -2, 0, 0, -2, 10],
            [-20, -50, -2, -2, -50, -20],
            [100, -20, 10, 10, -20, 100],
        ]

        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += evaluation_map[y][x]
                elif board[y][x] == 3 - stone:
                    score -= evaluation_map[y][x]
        return score

    def can_place_x_y(self, board, stone, x, y):
        """
        (x, y) に石を置けるか判定する。
        """
        if board[y][x] != 0:
            return False  # 既に石が置かれている場所には置けない

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            has_opponent = False

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                has_opponent = True
                nx += dx
                ny += dy

            if has_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                return True  # 相手の石を挟めるなら有効

        return False

    def can_place(self, board, stone):
        """
        石を置ける場所があるかどうかチェック。
        """
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    return True
        return False

    def flip_stones(self, board, stone, x, y):
        """
        石を置いた後にひっくり返す処理。
        """
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy

            if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                for fx, fy in stones_to_flip:
                    board[fy][fx] = stone


