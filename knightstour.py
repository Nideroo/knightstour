from math import log10


def ask_board_dims():
    ask_board_dims_msg = "Enter your board dimensions: "
    dims = ask_int_tuple(ask_board_dims_msg)
    while contains_non_int(dims) or contains_not_two(dims) or contains_zero_or_negative(dims):
        print("Invalid dimensions!")
        dims = ask_int_tuple(ask_board_dims_msg)
    return dims


def ask_pos(dims, current_pos=(0, 0), board_to_use=None, cell_size=0, start=False,):
    if start:
        ask_pos_msg = "Enter the knight's starting position: "
        pos = ask_int_tuple(ask_pos_msg)
        while contains_non_int(pos) or contains_not_two(pos) or pos_out_of_bounds(pos, dims):
            print("Invalid position!")
            pos = ask_int_tuple(ask_pos_msg)
    else:
        ask_pos_msg = "Enter your next move: "
        pos = ask_int_tuple(ask_pos_msg)
        while (contains_non_int(pos) or contains_not_two(pos) or pos_out_of_bounds(pos, dims)
               or pos not in calculate_possible_moves(current_pos, board_to_use, dims, cell_size)):
            print("Invalid move!", end="")
            pos = ask_int_tuple(ask_pos_msg)
    return pos


def ask_int_tuple(msg):
    result = ""
    while not isinstance(result, tuple):
        try:
            result = tuple(map(int, input(msg).split()))
        except ValueError:
            return -1,
    return result


def contains_non_int(tuple_to_check):
    return any(not isinstance(element, int) for element in tuple_to_check)


def contains_not_two(tuple_to_check):
    return len(tuple_to_check) != 2


def contains_zero_or_negative(tuple_to_check):
    return any(element <= 0 for element in tuple_to_check)


def pos_out_of_bounds(pos_to_check, dims):
    return not 0 < pos_to_check[0] <= dims[0] or not 0 < pos_to_check[1] <= dims[1]


def make_board(dims, cell_size):
    cell = "_" * cell_size
    return [[cell for _ in range(dims[0])] for _ in range(dims[1])]


def get_cell_size(dims):
    return len(str(dims[0] * dims[1]))


def print_board(board_to_print, dims, cell_size):
    n_col = dims[0]
    n_row = dims[1]
    rownums_format = f">{int(log10(n_row)) + 1}"
    border_length = n_col * (cell_size + 1) + 3
    i = n_row
    rows_to_print = []
    for row in board_to_print:
        rows_to_print.append(f"{str(i): {rownums_format}}| {' '.join(row)} |")
        i -= 1
    border_format = f">{len(rows_to_print[0])}"
    colnums_format = f">{len(rows_to_print[0]) - 2}"
    print(f"{'-' * border_length: {border_format}}")
    for row in rows_to_print:
        print(row)
    print(f"{'-' * border_length: {border_format}}")
    print(f"{''.join([(' '*(cell_size-int(log10(i)))) + str(i) for i in range(1, n_col+1)]): {colnums_format}}")


def place_marker(marker, pos, board_to_use, dims, cell_size):
    marker_format = f">{cell_size}"
    board_to_use[dims[1] - pos[1]][pos[0] - 1] = f"{marker: {marker_format}}"


def ask_puzzle():
    ask_puzzle_msg = "Do you want to try the puzzle? (y/n): "
    answer = input(ask_puzzle_msg)
    while answer not in ["y", "n"]:
        print("Invalid input!")
        answer = input(ask_puzzle_msg)
    return answer == "y"


def show_possible_moves(current_pos, board_to_use, dims, cell_size):
    possible_moves = calculate_possible_moves(current_pos, board_to_use, dims, cell_size)
    for pos in possible_moves:
        n_possible_moves_from_pos = len(calculate_possible_moves(pos, board_to_use, dims, cell_size))
        place_marker(str(n_possible_moves_from_pos), pos, board_to_use, dims, cell_size)
    print("Here are the possible moves:")
    print_board(board_to_use, dims, cell_size)
    for pos in possible_moves:
        place_marker(("_" * cell_size), pos, board_to_use, dims, cell_size)


def calculate_possible_moves(current_pos, board_to_use, dims, cell_size):
    if current_pos == (0, 0):
        return []
    current_pos_x = current_pos[0]
    current_pos_y = current_pos[1]
    positions = [(current_pos_x + 2, current_pos_y + 1),
                 (current_pos_x + 2, current_pos_y - 1),
                 (current_pos_x - 2, current_pos_y + 1),
                 (current_pos_x - 2, current_pos_y - 1),
                 (current_pos_x + 1, current_pos_y + 2),
                 (current_pos_x + 1, current_pos_y - 2),
                 (current_pos_x - 1, current_pos_y + 2),
                 (current_pos_x - 1, current_pos_y - 2)]
    positions = [pos for pos in positions if (not pos_out_of_bounds(pos, dims)
                                              and not already_visited(pos, board_to_use, dims, cell_size))]
    return positions


def already_visited(pos, board_to_use, dims, cell_size):
    pos_x = pos[0]
    pos_y = pos[1]
    cell = board_to_use[dims[1] - pos_y][pos_x - 1]
    return not cell == f"{'_' * cell_size}"


def result_of_attempt(board_to_use, dims, cell_size):
    n_visited_squares = count_visited_squares(board_to_use, cell_size)
    if n_visited_squares == dims[0] * dims[1]:
        print(f"Congratulations, you managed to visit all {n_visited_squares} squares in one knight's tour!")
    else:
        print(f"Your knight visited {n_visited_squares} squares!")


def count_visited_squares(board_to_use, cell_size):
    count = 0
    for row in board_to_use:
        for cell in row:
            if cell != "_" * cell_size:
                count += 1
    return count


def find_solution(start, board_to_use, dims, cell_size, move_count=2):
    if count_visited_squares(board_to_use, cell_size) == dims[0] * dims[1]:
        return True
    possible_moves = calculate_possible_moves(start, board_to_use, dims, cell_size)
    for move in possible_moves:
        place_marker(str(move_count), move, board_to_use, dims, cell_size)
        print_board(board_to_use, dims, cell_size)
        if find_solution(move, board_to_use, dims, cell_size, move_count+1):
            return True
        place_marker("_" * cell_size, move, board_to_use, dims, cell_size)
    return False


board_dims = ask_board_dims()
board_cell_size = get_cell_size(board_dims)
board = make_board(board_dims, board_cell_size)

start_pos = ask_pos(board_dims, start=True)
wants_to_try_puzzle = ask_puzzle()
if wants_to_try_puzzle:
    place_marker("1", start_pos, board, board_dims, board_cell_size)
    if not find_solution(start_pos, board, board_dims, board_cell_size):
        print("No solution exists!")
    else:
        board = make_board(board_dims, board_cell_size)
        place_marker("X", start_pos, board, board_dims, board_cell_size)
        show_possible_moves(start_pos, board, board_dims, board_cell_size)

        place_marker("*", start_pos, board, board_dims, board_cell_size)
        knight_pos = ask_pos(board_dims, start_pos, board, board_cell_size)
        place_marker("X", knight_pos, board, board_dims, board_cell_size)
        show_possible_moves(knight_pos, board, board_dims, board_cell_size)

        while calculate_possible_moves(knight_pos, board, board_dims, board_cell_size):
            place_marker("*", knight_pos, board, board_dims, board_cell_size)
            knight_pos = ask_pos(board_dims, knight_pos, board, board_cell_size)
            place_marker("X", knight_pos, board, board_dims, board_cell_size)
            show_possible_moves(knight_pos, board, board_dims, board_cell_size)
        print("No more possible moves!")
        result_of_attempt(board, board_dims, board_cell_size)
else:
    place_marker("1", start_pos, board, board_dims, board_cell_size)
    if not find_solution(start_pos, board, board_dims, board_cell_size):
        print("No solution exists!")
    else:
        print("Here's the solution!")
        print_board(board, board_dims, board_cell_size)
