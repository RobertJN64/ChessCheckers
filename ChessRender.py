#CONFIG
SQUARE_SIZE = 70
SQUARE_COLOR_A = (200,0,0)
SQUARE_COLOR_B = (100,0,0)
MOVE_SQUARE_COLOR = (0,200,0)
CAPTURE_SQUARE_COLOR = (0,0,200)
HIGHLIGHT_SQUARE_COLOR = (200,200,200)
BACKGROUND_COLOR = (50,50,50)
SQUARE_BORDER = (0,0,0)
KING_HIGHLIGHT_COLOR = (0, 0, 100)

INFOBOX_SIZE = 400

def text_objects(text, font):
    textSurface = font.render(text, True, (200,200,200))
    return textSurface, textSurface.get_rect()

class InfoGroup:
    def __init__(self, mode, turn, counter):
        self.mode = mode
        self.turn = turn
        self.counter = counter
        if turn == "w":
            self.turnstr = "White"
        else:
            self.turnstr = "Black"

class ChessRender:
    def __init__(self, pygame):
        self.pygame = pygame
        self.screen = self.pygame.display.set_mode((SQUARE_SIZE * 8 + INFOBOX_SIZE, SQUARE_SIZE * 8))
        self.pygame.display.set_caption('Chess / Checkers')

        pieceList = ["bb", "bk", "bn", "bp", "br", "bq", "wb", "wk", "wn", "wp", "wr", "wq"]
        self.pieceImgs = {}
        for piece in pieceList:
            self.pieceImgs[piece] = self.pygame.transform.scale(self.pygame.image.load("chessicons/" + piece + '.svg'),
                                                                (round(SQUARE_SIZE), round(SQUARE_SIZE)))

    def messageDisplay(self, text, loc, size):
        largeText = self.pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = (loc[0], loc[1])
        self.screen.blit(TextSurf, TextRect)

    def clearScreen(self):
        self.screen.fill(BACKGROUND_COLOR)

    def renderBoardSquares(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if i % 2 == j % 2:
                    color = SQUARE_COLOR_A
                else:
                    color = SQUARE_COLOR_B
                self.pygame.draw.rect(self.screen, color, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def renderMoveSquares(self, loc, moves, captures):
        for msquare in moves:
            x = msquare[0]
            y = msquare[1]
            self.pygame.draw.rect(self.screen, MOVE_SQUARE_COLOR,
                                  (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            self.pygame.draw.rect(self.screen, SQUARE_BORDER,
                                  (x * SQUARE_SIZE - 1, y * SQUARE_SIZE - 1, SQUARE_SIZE + 2, SQUARE_SIZE + 2), width=2)

        for msquare in captures:
            x = msquare[0]
            y = msquare[1]
            self.pygame.draw.rect(self.screen, CAPTURE_SQUARE_COLOR,
                                  (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            self.pygame.draw.rect(self.screen, SQUARE_BORDER,
                                  (x * SQUARE_SIZE - 1, y * SQUARE_SIZE - 1, SQUARE_SIZE + 2, SQUARE_SIZE + 2), width=2)

        if loc is not None:
            self.pygame.draw.rect(self.screen, HIGHLIGHT_SQUARE_COLOR,
                                  (loc[0] * SQUARE_SIZE, loc[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            self.pygame.draw.rect(self.screen, SQUARE_BORDER,
                                  (loc[0] * SQUARE_SIZE - 1, loc[1] * SQUARE_SIZE - 1,
                                   SQUARE_SIZE + 2, SQUARE_SIZE + 2),
                                  width = 2)

    def renderPieces(self, board):
        for y, row in enumerate(board.board):
            for x, piece in enumerate(row):
                if piece.name != "none":
                    if piece.isking:
                        self.pygame.draw.circle(self.screen, KING_HIGHLIGHT_COLOR,
                                                (round(x * SQUARE_SIZE + SQUARE_SIZE/2),
                                                 round(y * SQUARE_SIZE+ SQUARE_SIZE/2)),
                                                round(SQUARE_SIZE/3))
                    self.screen.blit(self.pieceImgs[piece.name], (x * SQUARE_SIZE, y * SQUARE_SIZE))

    def renderInfo(self, infoGroup):
        self.messageDisplay("Current Mode: " + infoGroup.mode, (8 * SQUARE_SIZE + INFOBOX_SIZE/2,50), 25)
        self.messageDisplay("Mode Switch in: " + str(infoGroup.counter) + " turns", (8 * SQUARE_SIZE + INFOBOX_SIZE/2,75), 20)
        self.messageDisplay("Current Turn: " + infoGroup.turnstr, (8 * SQUARE_SIZE + INFOBOX_SIZE / 2, 150), 20)


    def renderGroup(self, board, loc, moves, captures, infoGroup):
        """Calls all render + reset funcs"""
        self.clearScreen()
        self.renderBoardSquares()
        self.renderMoveSquares(loc, moves, captures)
        self.renderPieces(board)
        self.renderInfo(infoGroup)

