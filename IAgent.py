from abc import ABC, abstractmethod
from GameState import GameState
from Inventory import Inventory
from Card import Card
from Move import Move

class IAgent(ABC):
    _inventory: Inventory

    def has_lost(self) -> bool:
        return self._inventory.cards == []

    def receive_card(self, card: Card) -> None:
        """Called by the game when a player receives a card

        Args:
            card (Card): Card type that the player receives
        """
        self._inventory.cards.append(card)

    def receive_money(self, income: int) -> None:
        """Called by the game when a player receives money

        Args:
            income (int): amount of income
        """
        self._inventory.money += income

    def give_money(self, cost: int) -> int:
        """Called by the game, when a player has to pay

        Args:
            cost (int): amount to pay

        Returns:
            int: the paid amount (can be not full for the steal action)
        """

        cost = min(cost, self._inventory.money)
        self._inventory.money -= cost
        return cost

    
    def give_card(self, card_preference: Card) -> Card:
        """Called by the game when the player is forced to discard

        Args:
            card_preference (Card): 
                The card that the player should discard, if they have it on their hand
                If the cardPreference is Card.ANY, or if the player does not have the 
                preferred card (e.g. After bluffing), they can discard any one of their cards.

        Returns:
            Card: The card player decides to discard
        """
        card = self.generate_give_card(card_preference)
        if card not in self._inventory.cards or (card_preference != Card.ANY and card != card_preference and card_preference in self._inventory.cards):
            # will be interpreted as forfeit
            return Card.ANY
        
        self._inventory.cards.remove(card)
        return card

    @abstractmethod
    def generate_give_card(self, card_preference: Card) -> Card:
        """Chooses which card to give

        Args:
            card_preference (Card): 

        Returns:
            Card: 
        """
        pass

    def give_move(self, state: GameState) -> Move:
        """Called by the game when player has to make a move

        Args:
            state (GameState): the current state of the game

        Returns:
            Move: The move player wants to make 
        """
        move = self.generate_move(state)
        if move not in self._inventory.get_legal_moves(state.current_sequence[-1]):
            return Move.FORFEIT
        
        return move

    @abstractmethod 
    def generate_move(self, state: GameState) -> Move:
        """Generates a move based on the game state

        Args:
            state (GameState): the current state of the game

        Returns:
            Move: The move player wants to make 
        """
        pass
