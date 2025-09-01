from abc import ABC, abstractmethod
from .GameState import PlayerInfo
from .Card import Card
from .Move import Move

class IAgent(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def generate_give_card(self, state: PlayerInfo, card_preference: Card) -> Card:
        """Chooses which card to give

        Args:
            card_preference (Card): 

        Returns:
            Card: 
        """
        pass

    @abstractmethod 
    def generate_move(self, state: PlayerInfo) -> Move:
        """Generates a move based on the game state

        Args:
            state (PlayerInfo): the current state of the game

        Returns:
            Move: The move player wants to make 
        """
        pass
