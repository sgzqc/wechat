import os
import sys

# Initialize a 2-D list with initial values described by the problem. Returns board
def setBoard():
    board = list()
    sudokuBoard = '''200080300
    060070084
    030500209
    000105408
    000000000
    402706000
    301007040
    720040060
    004010003'''
    rows = sudokuBoard.split('\n')
    for row in rows:
        column = list()
        for character in row:
            if character == ' ':
                continue
            digit = int(character)
            column.append(digit)
        board.append(column)
    return board


# Find next empty space in Sudoku board and return dimensions
def findEmpty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0 :
                return row,col
    return None


# Print the Sudoku Board
def printBoard(board):
    for row in range(9):
        for col in range(9):
            print(board[row][col],end='')
        print()


# Check whether a specific number can be used for specific dimensions
def isValid(board, num, pos):

    row, col = pos
    # Check if all row elements include this number
    for j in range(9):
        if board[row][j] == num:
            return False

    # Check if all column elements include this number
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if the number is already included in the block
    rowBlockStart = 3* (row // 3)
    colBlockStart = 3* (col // 3)

    rowBlockEnd = rowBlockStart + 3
    colBlockEnd = colBlockStart + 3
    for i in range(rowBlockStart, rowBlockEnd):
        for j in range(colBlockStart, colBlockEnd):
            if board[i][j] == num:
                return False

    return True


def allowedValues(board,row,col):

    numbersList = list()

    for number in range(1,10):

        found = False
        # Check if all row elements include this number
        for j in range(9):
            if board[row][j] == number:
                found = True
                break
        # Check if all column elements include this number
        if found == True:
            continue
        else:
            for i in range(9):
                if board[i][col] == number:
                    found = True
                    break

        # Check if the number is already included in the block
        if found == True:
            continue
        else:
            rowBlockStart = 3* (row // 3)
            colBlockStart = 3* (col // 3)

            rowBlockEnd = rowBlockStart + 3
            colBlockEnd = colBlockStart + 3
            for i in range(rowBlockStart, rowBlockEnd):
                for j in range(colBlockStart, colBlockEnd):
                    if board[i][j] == number:
                        found = True
                        break
        if found == False:
            numbersList.append(number)
    return numbersList


# Store in a dictionary the legitimate values for each individual cell
def cacheValidValues(board):
    cache = dict()
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                cache[(i,j)] = allowedValues(board,i,j)
    return cache



def solveWithCache(board, cache):
    blank = findEmpty(board)
    if not blank:
        return True
    else:
        row, col = blank

    for value in cache[(row,col)]:
        if isValid(board, value, blank):
            board[row][col] = value

            if solveWithCache(board, cache):
                return True

            board[row][col] = 0
    return False


if __name__ == "__main__":
    board = setBoard()
    cache = cacheValidValues(board)
    print("init status  as below:")
    printBoard(board)
    solveWithCache(board, cache)
    print("result is as below:")
    printBoard(board)