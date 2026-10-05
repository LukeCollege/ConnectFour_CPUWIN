from abc import ABC, abstractmethod
from board import ConnectFourBoard
import random


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


# TODO: Create a CPUPlayer class which selects moves without user intervention
class CPUPlayer(AbstractPlayer):
    #TBD

    
