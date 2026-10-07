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
                board.rows[row][col] = symbol
                break

    def check_outcome(self, board, maximizing, opponent_symbol):
        if maximizing: #Same as other player win logic, If can win: place here
            for col in range(board.num_cols):
                if self.can_move(board, col):
                    temp_board = ConnectFourBoard(board.num_rows, board.num_cols)
                    temp_board.rows = [row[:] for row in board.rows]
                    temp_board.add_piece(col, self.symbol)
                    if temp_board.check_winner():
                        return True
                    
        else: #Same as other player block logic, if opponent wins: place here
            for col in range(board.num_cols):
                if self.can_move(board, col):
                    temp_board = ConnectFourBoard(board.num_rows, board.num_cols)
                    temp_board.rows = [row[:] for row in board.rows]
                    temp_board.add_piece(col, opponent_symbol)
                    if temp_board.check_winner():
                        return True
        return False

    
    def minimax(self, board, depth, alpha, beta, maximizing, opponent_symbol):
        #if self.check_outcome(board, maximizing, opponent_symbol):#Is not maximizing = human turn, trying to minimize human score
        #    return float('inf') if not maximizing else float('-inf') #Is maximizing = AI turn, trying to maximize score to beat human
        if board.check_winner():
            return float('inf') if not maximizing else float('-inf')


        if board.is_full() or depth == 0:
            return 0

        if maximizing: #It is the AI's turn, robot looking for highest score, WIN LOGIC
            max_eval = float('-inf') #If I get a score better than this, I want it
            for col in range(board.num_cols):
                if self.can_move(board, col): #If I can move here
                    board_copy = copy.deepcopy(board) #make a deep copy
                    self.simulate(board_copy, col, self.symbol) #Simulate all moves
                    eval = self.minimax(board_copy, depth - 1, alpha, beta, False, opponent_symbol) #Switch to human turn, simulate
                    max_eval = max(max_eval, eval) #Did human turn give a better score than previously?
                    alpha = max(alpha, eval) #Move robot made now becomes new alpha
                    if beta <= alpha: #If human makes a move worse for me than I've seen, stop looking
                        break
            return max_eval #Return highest possible score
        else:
            min_eval = float('inf')#Pretend it is the human turn, BLOCK LOGIC
            for col in range(board.num_cols):
                if self.can_move(board, col): #I want to get the lowest possible score for the bot
                    board_copy = copy.deepcopy(board) #Copy current board
                    self.simulate(board_copy, col, opponent_symbol) #Simulate a move
                    eval = self.minimax(board_copy, depth - 1, alpha, beta, True, opponent_symbol) #Robot turn, what does robot do?
                    min_eval = min(min_eval, eval)#If robot responds in a way that minimizes its own score based on previous human move, it becomes new min
                    beta = min(beta, eval) #Beta is smallest possible score
                    if beta <= alpha: #If AI has a move better for them than I can make negative, stop looking
                        break
            return min_eval #return lowest score
    
    def move(self, board, opponent_symbol, diff="Super Hard"):
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
            return board.num_cols // 2 #If first move, play in third column

        for col in valid_cols:
            board_copy = copy.deepcopy(board) #creates full, independent copy of board
            self.simulate(board_copy, col, self.symbol) #Runs simulation
            score = self.minimax(board_copy, self.search_depth, float('-inf'), float('inf'), False, opponent_symbol) #Defines score based on minimax

            if score > best_score: 
                best_score = score #Finds best score, thus best move
                best_col = col #makes best move based on best col
        return best_col if best_col is not None else valid_cols[0] #Return best move based on minimax


