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
                if can_place_x_y(board, stone, x, y):
                    # 仮想的に石を置く
                    new_board = [row[:] for row in board]
                    new_board[y][x] = stone
                    flip_stones(new_board, stone, x, y)

                    # ミニマックスでスコアを計算
                    score = self.minimax(new_board, self.depth, False, stone)
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def minimax(self, board, depth, maximizing, stone):
        """
        ミニマックス法を使って局面を評価する。
        depth: 残りの探索深さ
        maximizing: 最大化プレイヤー(True)か最小化プレイヤー(False)か
        stone: 現在のプレイヤーの石
        """
        if depth == 0 or not can_place(board, 1) and not can_place(board, 2):
            return self.evaluate(board, stone)

        opponent = 3 - stone
        if maximizing:
            max_eval = float('-inf')
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if can_place_x_y(board, stone, x, y):
                        new_board = [row[:] for row in board]
                        new_board[y][x] = stone
                        flip_stones(new_board, stone, x, y)

                        eval = self.minimax(new_board, depth - 1, False, stone)
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if can_place_x_y(board, opponent, x, y):
                        new_board = [row[:] for row in board]
                        new_board[y][x] = opponent
                        flip_stones(new_board, opponent, x, y)

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


# 必要な関数: 石をひっくり返す処理
def flip_stones(board, stone, x, y):
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
# 最後に追加する部分
def can_place_x_y(board, stone, x, y):
    """
    指定された座標 (x, y) に、指定された色の石を置けるかどうかを判定する関数
    board: ゲームボードの状態
    stone: 置く石（1: 黒, 2: 白）
    x, y: 置きたい位置
    """
    # ボードの範囲内かチェック
    if not (0 <= x < len(board[0]) and 0 <= y < len(board)):
        return False

    # すでに石が置かれている場所に置けない
    if board[y][x] != 0:
        return False

    # 石を置いた時にひっくり返せる相手の石があるかチェック
    opponent = 3 - stone  # 1なら2（白）、2なら1（黒）
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []

        # 相手の石を見つける
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        # 自分の石があればひっくり返せるので置ける
        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            if stones_to_flip:
                return True

    return False


def can_place(board, stone):
    """
    ボード全体で指定された色の石を置ける場所があるかを確認する関数
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False




