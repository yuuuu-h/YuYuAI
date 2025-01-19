def can_place(board, stone):
    """
    ボードに現在のプレイヤーが石を置ける場所があるかを判定する。
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False
