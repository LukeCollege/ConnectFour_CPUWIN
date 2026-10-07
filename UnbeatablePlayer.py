from abc import ABC, abstractmethod
from board import ConnectFourBoard
import random
import copy


class AbstractPlayer(ABC):
    def __init__(self, symbol, name):
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def move(self, **kwargs):
        """Return an integer representing the column where the player intends to play a piece."""


class ConsolePlayer(AbstractPlayer):
    def move(self, **kwargs):
        """Get which column to play in from the user via text console"""
        return int(input('Enter which column to play in: '))


# TODO: Create an UNBEATABLE CPUPlayer class which selects moves without user intervention
class CPUPlayer(AbstractPlayer):
    def __init__(self, symbol, name):
        super().__init__(symbol, name) #Comes from AbstractPlayer class, purely for naming (self.name, self.symbol)
        self.search_depth = 8 #How many moves ahead the AI will look, much more will cause time delays due to computation
    
    def can_move(self, board, col): #Checks if a move is valid or not
        return 0 <= col < board.num_cols and board.rows[0][col] == ' ' #returns true if col is from 0 to num_cols and the column is empty

    def simulate(self, board, col, symbol): #Simulates a move on a copied board
        for row in reversed(range(board.num_rows)): #Needs to be reversed so as the AI doesn't place a piece on row 0
            if board.rows[row][col] == ' ':
                board.rows[row][col] == symbol
                break
    
    def move(self, board, oponent_symbol, diff="Super Hard"):
        best_score = float('-inf') #defines best score, will be replaced to track best moves
        best_col = None #Will be used to hold value based on best score
        valid_cols = [col for col in range(board.num_cols) if self.can_move(board, col)] #Determines if input column is valid via helper function
        if not valid_cols:
            return 0

        empty_board = True #If it is the first move of the game, Play in the 3rd column
        for row in range(board.num_rows): 
            for col in range(board.num_cols):
                if board.rows[row][col] != ' ': #loops through rows & cols to find a non-empty space
                    empty_board = False
                    break
            if not empty_board: #breaks early if found early to save time
                break
        if empty_board:
            return board.num_cols // 2

