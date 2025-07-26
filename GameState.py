from Inventory import Inventory
from CardDeck import CardDeck
from Move import Move

class GameState:
    players: list[Inventory]
    initialPlayer: int
    turnPlayer: int
    deck: CardDeck
    current_sequence: list[Move]
    score: list[int]


    def __init__(self, number_of_players: int = 2) -> None:
        self.players = [Inventory()] * number_of_players
        self.initialPlayer = 0
        self.turnPlayer = 0
        self.deck = CardDeck()
        self.current_sequence = [Move.OK]
        self.score = [0] * number_of_players
