import time
from pentamino_pieces import pieces


def visualize(height, width, mask, empty=" ", fill="*"):
    string = (
        f"{mask:0>{height*width}b}".replace("0", empty).replace("1", fill)
    )
    return [string[row*width:(row+1)*width] for row in range(height)]


def probe_masks(size: int) -> list[int]:
    return tuple(1 << k for k in reversed(range(size)))


def position_masks(
        height: int, width: int, displacements: tuple[tuple[int, int]]
) -> list[int]:
    max_y = max(y for y, _ in displacements)
    max_x = max(x for _, x in displacements)
    min_x = min(x for _, x in displacements)

    piece_mask = 0
    for y, x in displacements:
        piece_mask |= 1 << ((max_y - y) * width + max_x - x)
    masks = [0] * (width * height)
    for y in reversed(range(height - max_y)):
        for x in reversed(range(-min_x, width - max_x)):
            masks[y*width + x] = piece_mask
            piece_mask <<= 1
        piece_mask <<= max_x - min_x
    return masks


def transpose(piece):
    return tuple((x, y) for y, x in piece)


def flip_vertically(displacements):
    return tuple((-y, x) for y, x in displacements)


def normalize(displacements):
    base_y, base_x = min(displacements)
    return tuple(sorted((y - base_y, x - base_x) for y, x in displacements))


def rotate_counterclockwise(displacements, times=1):
    for _ in range(times):
        displacements = flip_vertically(transpose(displacements))
    return normalize(displacements)


def transforms(displacements, rotate=True, flip=True):
    sides = [displacements]
    if flip:
        sides.append(flip_vertically(displacements))
    result = set(
        rotate_counterclockwise(side, quarter)
        for side in sides
        for quarter in range(4 if rotate else 1)
    )
    return tuple(result)


def count_area(board: int, height: int, width: int, initial_point: int) -> int:
    size = height * width
    if initial_point >= size:
        return -1
    edge = set([initial_point])
    empty_probes = probe_masks(size)
    shifts = (-1, 1, -width, width)
    count = 0

    while edge:
        n = len(edge)
        for _ in range(n):
            point = edge.pop()
            count += not board & empty_probes[point]
            board |= empty_probes[point]
            row = point // width
            for shift in shifts:
                neighbour = point + shift
                if (neighbour >= size or neighbour < 0) or neighbour // width != row and shift in (-1, 1):
                    continue
                if not board & empty_probes[neighbour]:
                    edge.add(neighbour)
    return count


def solutions(piece_set: tuple[tuple[int]], board_size: int):

    def advance_position(board, position):
        while board & empty_probes[position]:
            position += 1
        return position

    def format_solution(history):
        return tuple(
            (piece_index, direction_index, position)
            for position, piece_index, direction_index, *rest in history
        )

    empty_probes = probe_masks(board_size)
    pieces_on_board = set()
    piece_count = len(piece_set)
    full_board = 2**len(empty_probes) - 1

    history = []

    board = 0
    position = 0
    next_piece = 0
    next_direction = 0
    while True:
        placed = False
        for piece_index in range(next_piece, piece_count):
            if piece_index in pieces_on_board:
                continue
            directions = piece_set[piece_index][position]
            for direction_index in range(next_direction, len(directions)):
                mask = directions[direction_index]
                if not (board & mask):
                    entry = (position, piece_index, direction_index, board)
                    new_board = board | mask
                    if new_board == full_board:
                        yield format_solution(history + [entry])
                    else:
                        board = new_board
                        history.append(entry)
                        pieces_on_board.add(piece_index)
                        position = advance_position(board, position)
                        placed = True
                        next_piece = 0
                    break
            next_direction = 0
            if placed:
                break
        else:
            if history:
                position, piece_index, direction_index, board = history.pop()
                pieces_on_board.remove(piece_index)
                next_piece = piece_index
                next_direction = direction_index + 1
            else:
                break


if __name__ == "__main__":
    height = 15
    width = 4
    t1 = time.time()
    for _ in range(1000):
        area = count_area(0, height, width, 0)
    t2 = time.time()
    print(f"Time elapsed: {t2 - t1:.3f}")
    print("Board area:", area)
    piece_set = tuple(
        tuple(
            position_masks(height, width, transform)
            for transform in transforms(displacements)
        ) for _, displacements in pieces.items()
    )
    inversed_piece_set = tuple(
        tuple(
            tuple(
                piece[transform][position]
                for transform in range(len(piece))
                if piece[transform][position]
            )
            for position in range(height * width)
        )
        for piece in piece_set
    )
    t1 = time.time()
    s = list(solutions(inversed_piece_set, height * width))
    t2 = time.time()
    print(f"Time elapsed: {t2 - t1:.2f}")
    print("Solutions found:", len(s))
