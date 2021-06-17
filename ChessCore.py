import math

class Piece:
    def __init__(self, name):
        self.name = name
        self.hasmoved = False #for castling checks
        self.enpassant = False #is eligible for an enpassant capture
        self.isking = name[1] == "k" #checkers king

    def str(self, padstr=True, padlen=10, noneblank = True):
        if not padstr:
            if noneblank and self.name == "none":
                return ""
            else:
                return str(self.name)

        else:
            if noneblank and self.name == "none":
                return " " * padlen
            else:
                l = len(self.name)
                l = (padlen - l)/2
                return " " * math.floor(l) + str(self.name) + " " * math.ceil(l)


class BoardState:
    def __init__(self):
        self.board = []
        for i in range(0, 8):
            self.board.append([Piece('none')]*8)

    def reset(self):
        for row in self.board:
            for i in range(0, len(row)):
                row[i] = Piece('none')

        for i in range(0, len(self.board[0])):
            self.board[1][i] = Piece('bp') #black pawn
            self.board[6][i] = Piece('wp') #white pawn

        self.board[0][0] = Piece('br')  # black rook
        self.board[0][1] = Piece('bn')  # black knight
        self.board[0][2] = Piece('bb')  # black bishop
        self.board[0][3] = Piece('bq')  # black queen
        self.board[0][4] = Piece('bk')  # black king
        self.board[0][5] = Piece('bb')  # black bishop
        self.board[0][6] = Piece('bn')  # black knight
        self.board[0][7] = Piece('br')  # black rook

        self.board[7][0] = Piece('wr')  # white rook
        self.board[7][1] = Piece('wn')  # white knight
        self.board[7][2] = Piece('wb')  # white bishop
        self.board[7][3] = Piece('wq')  # white queen
        self.board[7][4] = Piece('wk')  # white king
        self.board[7][5] = Piece('wb')  # white bishop
        self.board[7][6] = Piece('wn')  # white knight
        self.board[7][7] = Piece('wr')  # white rook


    def __str__(self):
        outstr = ""
        rowstr = ""
        for row in self.board:
            rowstr = ""
            for item in row:
                rowstr += '|' + item.str()

            outstr += rowstr + '|\n'
            outstr += len(rowstr) * "-" + '\n'

        return len(rowstr) * "-" + '\n' + outstr

    def clearEnpassant(self):
        for row in self.board:
            for piece in row:
                piece.enpassant = False

    def promoteAndKing(self):
        for piece in self.board[0]:
            if piece.name == "wp":
                piece.name = "wq"
                piece.hasmoved = False
                piece.isking = True

            elif piece.name[0] == "w":
                piece.isking = True

        for piece in self.board[7]:
            if piece.name == "bp":
                piece.name = "bq"
                piece.hasmoved = False
                piece.isking = True

            elif piece.name[0] == "b":
                piece.isking = True

    def checkWin(self):
        wking = False
        bking = False
        for row in self.board:
            for piece in row:
                if piece.name == "wk":
                    wking = True
                elif piece.name == "bk":
                    bking = True

        if not wking:
            return True, "Black wins!"

        if not bking:
            return True, "White wins!"

        return False, ""