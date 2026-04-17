def is_valid(board, row, col, num):
    """
    检查在 (row, col) 位置填入 num 是否合法
    """
    # 1. 检查同一行是否重复
    for i in range(9):
        if board[row][i] == num:
            return False

    # 2. 检查同一列是否重复
    for i in range(9):
        if board[i][col] == num:
            return False

    # 3. 检查 3×3 小九宫格是否重复
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(board):
    """
    递归回溯求解数独
    """
    # 遍历整个棋盘
    for row in range(9):
        for col in range(9):
            # 找到空位置（0表示空）
            if board[row][col] == 0:
                # 尝试填入 1-9
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        # 递归继续填下一个空
                        if solve_sudoku(board):
                            return True
                        # 回溯：填错了，重置为0
                        board[row][col] = 0
                # 所有数字都尝试过，无解
                return False
    # 所有位置填满，求解成功
    return True


def print_board(board):
    """格式化打印数独棋盘"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(str(board[i][j]) + " ", end="")
        print()


# 测试用例：0代表待填充的空位置
if __name__ == "__main__":
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    print("原始数独：")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\n求解完成：")
        print_board(sudoku_board)
    else:
        print("\n无解")
