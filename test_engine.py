from engine.piece import produce_rotations
from pentamino_pieces import pieces
from engine.board import Board, invert
from engine.solver import solutions


def visualize(board: Board, mask, empty=" ", fill="*"):
    height = board.height
    width = board.width
    string = (
        f"{mask:0>{height*width}b}".replace("0", empty).replace("1", fill)
    )
    return [string[row*width:(row+1)*width] for row in range(height)]


if __name__ == "__main__":
    board = Board(15, 4)
    # piece_masks = {
    #     name: board.piece_masks(points) for name, points in pieces.items()
    # }
    # for mask in piece_masks["L"]:
    #     s = visualize(board, mask)
    #     print("".join(["="] * board.width))
    #     print(*s, sep="\n")
    #     print("".join(["="] * board.width))
    #     print("")

    piece_set = tuple(
        invert(tuple(
            board.piece_masks(rotation)
            for rotation in produce_rotations(piece)
        ))
        for piece in pieces.values()
    )
    s = list(solutions(board, piece_set))
    print(f"Solutions found: {len(s)}")
