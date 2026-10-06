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
    def move(self, board, oponent_symbol, diff="Super Hard"):
        best_score = float('-inf') #defines best score, will be replaced to track best moves
        best_col = None #Will be used to track best col
