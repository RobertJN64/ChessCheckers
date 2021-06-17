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

def horizontalList(board, x, y, color, maxl=8):
    vmoves = []
    vcaptures = []

    #right
    for x1 in range(x + 1, x + 1 + maxl):
        if valid(x1, y) and not occupied(board, x1, y, color):
            if capture(board, x1, y, color):
                vcaptures.append([x1, y])
                break
            else:
                vmoves.append([x1, y])
        else:
            break

    #left
    for x1 in range(x - 1, x - maxl - 1, -1):
        if valid(x1, y) and not occupied(board, x1, y, color):
            if capture(board, x1, y, color):
                vcaptures.append([x1, y])
                break
            else:
                vmoves.append([x1, y])
        else:
            break

    #up
    for y1 in range(y + 1, y + 1 + maxl):
        if valid(x, y1) and not occupied(board, x, y1, color):
            if capture(board, x, y1, color):
                vcaptures.append([x, y1])
                break
            else:
                vmoves.append([x, y1])
        else:
            break

    #down
    for y1 in range(y - 1, y - maxl - 1, -1):
        if valid(x, y1) and not occupied(board, x, y1, color):
            if capture(board, x, y1, color):
                vcaptures.append([x, y1])
                break
            else:
                vmoves.append([x, y1])
        else:
            break

    return vmoves, vcaptures

def diagonalList(board, x, y, color, maxl=8):
    vcaptures = []
    vmoves = []
    for i in range(1, maxl + 1):
        x1 = x + i
        y1 = y + i
        if valid(x1, y1) and not occupied(board, x1, y1, color):
            if capture(board, x1, y1, color):
                vcaptures.append([x1, y1])
                break
            else:
                vmoves.append([x1, y1])
        else:
            break

    for i in range(1, maxl + 1):
        x1 = x - i
        y1 = y + i
        if valid(x1, y1) and not occupied(board, x1, y1, color):
            if capture(board, x1, y1, color):
                vcaptures.append([x1, y1])
                break
            else:
                vmoves.append([x1, y1])
        else:
            break

    for i in range(1, maxl + 1):
        x1 = x - i
        y1 = y - i
        if valid(x1, y1) and not occupied(board, x1, y1, color):
            if capture(board, x1, y1, color):
                vcaptures.append([x1, y1])
                break
            else:
                vmoves.append([x1, y1])
        else:
            break

    for i in range(1, maxl + 1):
        x1 = x + i
        y1 = y - i
        if valid(x1, y1) and not occupied(board, x1, y1, color):
            if capture(board, x1, y1, color):
                vcaptures.append([x1, y1])
                break
            else:
                vmoves.append([x1, y1])
        else:
            break
    return vmoves, vcaptures

def getValidKingMoves(board, x, y, color):
    movesD, capturesD = diagonalList(board, x, y, color, maxl=1)
    movesH, capturesH = horizontalList(board, x, y, color, maxl=1)

    vmoves = movesD + movesH
    vcaptures = capturesD + capturesH

    #castling
    if not board[y][x].hasmoved:

        if (not board[y][7].hasmoved) and board[y][6].name == "none" and board[y][5].name == "none": #king side
            vcaptures.append([6, y])

        if (not board[y][0].hasmoved) and board[y][1].name == "none" and board[y][2].name == "none" and board[y][3].name == "none": #queen side
            vcaptures.append([2, y])

    return vmoves, vcaptures


def getValidQueenMoves(board, x, y, color):
    movesD, capturesD = diagonalList(board, x, y, color)
    movesH, capturesH = horizontalList(board, x, y, color)
    vmoves = movesD + movesH
    vcaptures = capturesD + capturesH
    return vmoves, vcaptures

def getValidRookMoves(board, x, y, color):
    #Castling is handled kingside
    vmoves, vcaptures = horizontalList(board, x, y, color)
    return vmoves, vcaptures


def getValidBishopMoves(board, x, y, color):
    vmoves, vcaptures = diagonalList(board, x, y, color)
    return vmoves, vcaptures

def getValidKnightMoves(board, x, y, color):
    moves = [[x+1, y+2], [x+2, y+1], [x-1, y-2], [x-2, y-1],
             [x+1, y-2], [x+2, y-1], [x-1, y+2], [x-2, y+1]]

    vmoves = []
    vcaptures = []
    for move in moves:
        x1 = move[0]
        y1 = move[1]
        if valid(x1, y1) and not occupied(board, x1, y1, color):
            if capture(board, x1, y1, color):
                vcaptures.append(move)
            else:
                vmoves.append(move)
    return vmoves, vcaptures

def getValidPawnMoves(board, x, y, color):
    piece = board[y][x]
    if color:
        posdif = -1
    else:
        posdif = 1

    vmoves = []
    vcaptures = []
    if (valid(x, y + posdif) and (not capture(board, x, y + posdif, color))
            and (not occupied(board, x, y + posdif, color))):
        vmoves.append([x, y + posdif])

    if (valid(x, y + posdif * 2) and (not capture(board, x, y + posdif * 2, color))
            and (not piece.hasmoved) and (not occupied(board, x, y + posdif * 2, color))
            and (not occupied(board, x, y + posdif, color))):
        vmoves.append([x, y + posdif * 2])

    if valid(x + 1, y + posdif) and capture(board, x + 1, y + posdif, color):
        vcaptures.append([x + 1, y + posdif])

    if valid(x - 1, y + posdif) and capture(board, x - 1, y + posdif, color):
        vcaptures.append([x - 1, y + posdif])

    if valid(x - 1, y) and capture(board, x - 1, y, color) and board[y][x-1].enpassant:
        vcaptures.append([x - 1, y + posdif])

    if valid(x + 1, y) and capture(board, x + 1, y, color) and board[y][x+1].enpassant:
        vcaptures.append([x + 1, y + posdif])

    return vmoves, vcaptures


def getValidMoves(GameState, pieceLoc):
    """moves, captures"""
    x = pieceLoc[0]
    y = pieceLoc[1]

    board = GameState.board

    piece = board[y][x]

    if piece.name == "none":
        warnings.warn("ERROR: No piece at location!")
        return [], []

    color = piece.name[0] == "w"

    if piece.name[1] == "b": #bishop
        return getValidBishopMoves(board, x, y, color)

    elif piece.name[1] == "k": #king
        return getValidKingMoves(board, x, y, color)

    elif piece.name[1] == "n": #knight
        return getValidKnightMoves(board, x, y, color)

    elif piece.name[1] == "p": #pawn
        return getValidPawnMoves(board, x, y, color)

    elif piece.name[1] == "q":  # queen
        return getValidQueenMoves(board, x, y, color)

    elif piece.name[1] == "r":  # rook
        return getValidRookMoves(board, x, y, color)

    else:
        warnings.warn("Piece name not found")
