import warnings

def valid(x, y):
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    else:
        return True

def capture(board, x, y, color):
    piece = board[y][x].name
    return piece[0] == "w" and not color or piece[0] == "b" and color

def occupied(board, x, y, color):
    """Occupied by same color"""
    piece = board[y][x].name
    return piece[0] == "w" and color or piece[0] == "b" and not color

def getValidMoves(GameState, loc):
    """moves, captures"""
    x = loc[0]
    y = loc[1]

    board = GameState.board

    piece = board[y][x]
    color = piece.name[0] == "w"

    if piece.isking:
        directions = [[1,1], [1,-1], [-1,1], [-1,-1]]

    elif piece.name[0] == "w":
        directions = [[1,-1], [-1,-1]]

    elif piece.name[0] == "b":
        directions = [[1,1], [-1,1]]

    else:
        warnings.warn("Error, piece not found")
        return

    vmoves = []
    vcaptures = []

    for move in directions:
        x1 = x + move[0]
        y1 = y + move[1]

        if valid(x1, y1):
            if (not capture(board, x1, y1, color)) and (not occupied(board, x1, y1, color)):
                vmoves.append([x1, y1])

            elif capture(board, x1, y1, color):
                x1 = x + move[0] * 2
                y1 = y + move[1] * 2

                if valid(x1, y1):
                    if (not capture(board, x1, y1, color)) and (not occupied(board, x1, y1, color)):
                        vcaptures.append([x1, y1])
    return vmoves, vcaptures