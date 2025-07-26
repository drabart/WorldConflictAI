from Inventory import Inventory
from CardDeck import CardDeck
from Move import Move

class GameState():
    players : list[Inventory]
    initialPlayer : int
    turnPlayer : int
    deck : CardDeck
    currentSequence : list[Move]
    score : list[int]


    def __init__(self, numberOfPlayers : int = 2) -> None:
        self.players = [Inventory()] * numberOfPlayers
        self.initialPlayer = 0
        self.turnPlayer = 0
        self.deck = CardDeck()
        self.currentSequence = [Move.OK]
        self.score = [0] * numberOfPlayers
