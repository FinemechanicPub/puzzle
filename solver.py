import time
from pentamino_pieces import pieces


def visualize(height, width, mask, empty=" ", fill="*"):
    string = (
        f"{mask:0>{height*width}b}".replace("0", empty).replace("1", fill)
    )
    return [string[row*width:(row+1)*width] for row in range(height)]


def probe_masks(height: int, width: int) -> list[int]:
    return [1 << k for k in reversed(range(width * height))]


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


def solutions(piece_set: dict[str, list[int]], board_size: int):

    def advance_position():
        nonlocal position
        while (
            position < len(empty_probes)
            and board & empty_probes[position]
        ):
            position += 1

    def format_solution(history):
        return tuple(
            (pieces[piece_index], direction_index, position)
            for position, piece_index, direction_index, _ in history
        )

    empty_probes = tuple(1 << k for k in reversed(range(board_size)))
    pieces = list(piece_set)
    pieces_on_board = set()
    full_board = 2**len(empty_probes) - 1

    history = []

    board = 0
    position = 0
    next_piece = 0
    next_direction = 0
    while True:
        for piece_index in range(next_piece, len(pieces)):
            if piece_index in pieces_on_board:
                continue
            directions = piece_set[pieces[piece_index]]
            for direction_index in range(next_direction, len(directions)):
                mask = directions[direction_index][position]
                if mask and board & mask == 0:
                    entry = (position, piece_index, direction_index, board)
                    if board | mask == full_board:
                        yield format_solution(history + [entry])
                    else:
                        board |= mask
                        history.append(entry)
                        pieces_on_board.add(piece_index)
                    break
            next_direction = 0
            if piece_index in pieces_on_board:
                next_piece = 0
                break
        else:
            if not history:
                break
            position, piece_index, direction_index, board = history.pop()
            pieces_on_board.remove(piece_index)
            next_piece = piece_index
            next_direction = direction_index + 1

        advance_position()


if __name__ == "__main__":
    height = 15
    width = 4
    piece_set = {
        symbol: tuple(
            position_masks(height, width, transform)
            for transform in transforms(displacements)
        ) for symbol, displacements in pieces.items()
    }
    t1 = time.time()
    s = list(solutions(piece_set, height * width))
    t2 = time.time()
    print(f"Time elapsed: {t2 - t1:.2f}")
    print("Solutions found:", len(s))
