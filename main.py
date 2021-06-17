import ChessCore as CC
import ChessMoveValidator as ChessMV
import CheckersMoveValidator as CheckersMV
import ChessRender as CR

import pygame
import time
import math

pygame.init()

def AdvanceTurn(t, c, m):
    c -= 1
    if c == 0:
        c = 10
        if m == "CHESS":
            m = "CHECKERS"
        else:
            m = "CHESS"
    if t == "w":
        return "b", c, m
    else:
        return "w", c, m

SQUARE_SIZE = CR.SQUARE_SIZE
board = CC.BoardState()
board.reset()

screen = CR.ChessRender(pygame)

vmoves = []
vcaptures = []
loc = None

mode = "CHESS"
turn = "w"
modeSwapCounter = 10

done = False
endmessage = ""
movelock = False
while not done:
    screen.clearScreen()
    info = CR.InfoGroup(mode, turn, modeSwapCounter)
    screen.renderGroup(board, loc, vmoves, vcaptures, info)

    time.sleep(0.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                pos = [math.floor(pos[0]/SQUARE_SIZE), math.floor(pos[1]/SQUARE_SIZE)]
                if movelock and pos not in vcaptures:
                    vcaptures = []
                    turn, modeSwapCounter, mode = AdvanceTurn(turn, modeSwapCounter, mode)
                    movelock = False

                elif mode == "CHESS":
                    if ChessMV.valid(pos[0], pos[1]):
                        if board.board[pos[1]][pos[0]].name[0] == turn:
                            loc = pos
                            vmoves, vcaptures = ChessMV.getValidMoves(board, pos)

                        else:
                            if pos in vmoves or pos in vcaptures:
                                board.clearEnpassant()
                                piece = board.board[loc[1]][loc[0]]
                                rpiece = board.board[pos[1]][pos[0]]
                                board.board[loc[1]][loc[0]] = CC.Piece("none")
                                if rpiece.name == "none" and pos in vcaptures:
                                    #En passant
                                    if piece.name == "wp":
                                        board.board[pos[1] + 1][pos[0]] = CC.Piece("none")
                                    elif piece.name == "bp":
                                        board.board[pos[1] - 1][pos[0]] = CC.Piece("none")

                                    #castle
                                    elif piece.name[1] == "k":
                                        if pos[0] == 6:
                                            #king side
                                            board.board[pos[1]][5] = board.board[pos[1]][7]
                                            board.board[pos[1]][7] = CC.Piece("none")
                                        else:
                                            #queen side
                                            board.board[pos[1]][3] = board.board[pos[1]][0]
                                            board.board[pos[1]][0] = CC.Piece("none")

                                board.board[pos[1]][pos[0]] = piece
                                if piece.name[1] == "p" and abs(loc[1]-pos[1]) == 2:
                                    piece.enpassant = True
                                else:
                                    piece.enpassant = False
                                piece.hasmoved = True
                                vmoves = []
                                vcaptures = []
                                loc = None
                                turn, modeSwapCounter, mode = AdvanceTurn(turn, modeSwapCounter, mode)
                                board.promoteAndKing()
                                done, endmessage = board.checkWin()

                elif mode == "CHECKERS":
                    if CheckersMV.valid(pos[0], pos[1]):
                        if board.board[pos[1]][pos[0]].name[0] == turn:
                            loc = pos
                            vmoves, vcaptures = CheckersMV.getValidMoves(board, pos)

                        else:
                            if pos in vcaptures:
                                board.board[round((loc[1] + pos[1]) / 2)][round((loc[0] + pos[0]) / 2)] = CC.Piece("none")

                            if pos in vmoves or pos in vcaptures:
                                board.clearEnpassant()
                                piece = board.board[loc[1]][loc[0]]
                                board.board[loc[1]][loc[0]] = CC.Piece("none")
                                board.board[pos[1]][pos[0]] = piece
                                piece.hasmoved = True

                                ms, cs = CheckersMV.getValidMoves(board, pos)
                                movelock = False
                                if len(cs) > 0 and pos in vcaptures:
                                    vcaptures = cs
                                    movelock = True

                                else:
                                    vcaptures = []
                                    turn, modeSwapCounter, mode = AdvanceTurn(turn, modeSwapCounter, mode)

                                vmoves = []
                                loc = None

                                board.promoteAndKing()
                                done, endmessage = board.checkWin()



    pygame.display.update()

print(endmessage)