swaps = 0

def swap(board, i, j):
    board[i], board[j] = board[j], board[i]
    global swaps
    swaps += 1

def print_board(board):
    print(f"\nSolution {len(solutions)}:")
    n = len(board)
    for i in range(n):
        row = ""
        for j in range(n):
            if board[i] == j:
                row += "Q "
            else:
                row += "_ "
        print(row)

def is_safe(board, n):
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                return False
    return True

def solve_n_queens_swap(board, l, r, n, solutions):
    if l == r:
        if is_safe(board, n):
            solutions.append(board.copy())
            print_board(board)
    else:
        for i in range(l, r):
            swap(board, l, i)
            solve_n_queens_swap(board, l+1, r, n, solutions)
            swap(board, l, i)

if __name__ == "__main__":
    n = 4
    board = list(range(n))
    solutions = []
    print("Finding all solutions using Swapping approach:")
    solve_n_queens_swap(board, 0, n, n, solutions)
    print(f"\nTotal solutions found: {len(solutions)}")
    print(f"\nTotal swaps made: {swaps}")