from abc import ABC, abstractmethod
from GameState import GameState
from Inventory import Inventory
from Card import Card
from Move import Move

class IAgent(ABC):
    _inventory : Inventory

    def hasLost(self) -> bool:
        return self._inventory.cards == []

    def receiveCard(self, card : Card) -> None:
        """Called by the game when a player receives a card

        Args:
            card (Card): Card type that the player receives
        """
        self._inventory.cards.append(card)

    def receiveMoney(self, income : int) -> None:
        """Called by the game when a player receives money

        Args:
            income (int): amount of income
        """
        self._inventory.money += income

    def giveMoney(self, cost : int) -> int:
        """Called by the game, when a player has to pay

        Args:
            cost (int): amount to pay

        Returns:
            int: the paid amount (can be not full for the steal action)
        """

        cost = min(cost, self._inventory.money)
        self._inventory.money -= cost
        return cost

    
    def giveCard(self, cardPreference : Card) -> Card:
        """Called by the game when the player is forced to discard

        Args:
            cardPreference (Card): 
                The card that the player should discard, if they have it on their hand
                If the cardPreference is Card.ANY, or if the player does not have the 
                preferred card (e.g. After bluffing), they can discard any one of their cards.

        Returns:
            Card: The card player decides to discard
        """
        card = self.generateGiveCard(cardPreference)
        if card not in self._inventory.cards or (cardPreference != Card.ANY and card != cardPreference and cardPreference in self._inventory.cards):
            # will be interpreted as forfeit
            return Card.ANY
        
        self._inventory.cards.remove(card)
        return card

    @abstractmethod
    def generateGiveCard(self, cardPreference : Card) -> Card:
        """Choses which card to give

        Args:
            cardPreference (Card): 

        Returns:
            Card: 
        """
        pass

    def giveMove(self, state : GameState) -> Move:
        """Called by the game when player has to make a move

        Args:
            state (GameState): the current state of the game

        Returns:
            Move: The move player wants to make 
        """
        move = self.generateMove(state)
        if move not in self._inventory.getLegalMoves(state.currentSequence[-1]):
            return Move.FORFEIT
        
        return move

    @abstractmethod 
    def generateMove(self, state : GameState) -> Move:
        """Generates a move based on the gamestate

        Args:
            state (GameState): the current state of the game

        Returns:
            Move: The move player wants to make 
        """
        pass
