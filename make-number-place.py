import random
import copy

GRID_SIZE = 9

def is_valid(board, row, col, num):
    # 行と列をチェック
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    # 3x3 ブロックをチェック
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve(board, count_solutions=False):
    """数独を解く。解の数もカウント可能。"""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                solutions = 0
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        result = solve(board, count_solutions)
                        if count_solutions:
                            solutions += result
                            if solutions > 1:
                                board[row][col] = 0
                                return solutions
                        else:
                            board[row][col] = 0
                            return True
                        board[row][col] = 0
                return solutions if count_solutions else False
    return 1 if count_solutions else True

def fill_board(board):
    """ランダムに数字を入れて完全な解を作成"""
    nums = list(range(1, 10))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def remove_numbers(board, attempts=50):
    """マスを削除して一意解の問題を作成"""
    positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
    random.shuffle(positions)

    while attempts > 0 and positions:
        row, col = positions.pop()
        backup = board[row][col]
        board[row][col] = 0

        # 一意解性の確認
        board_copy = copy.deepcopy(board)
        if solve(board_copy, count_solutions=True) != 1:
            board[row][col] = backup  # 解が一意でないなら戻す
        attempts -= 1

def generate_sudoku():
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    fill_board(board)
    puzzle = copy.deepcopy(board)
    remove_numbers(puzzle, attempts=60)
    return puzzle, board  # 問題と解答

def print_board(board):
    for i in range(GRID_SIZE):
        line = ""
        for j in range(GRID_SIZE):
            num = board[i][j]
            line += f"{num if num != 0 else '.'} "
            if j % 3 == 2 and j != 8:
                line += "| "
        print(line)
        if i % 3 == 2 and i != 8:
            print("-" * 21)

if __name__ == "__main__":
    puzzle, solution = generate_sudoku()
    print("=== 問題 ===")
    print_board(puzzle)
    print("\n=== 解答 ===")
    print_board(solution)
