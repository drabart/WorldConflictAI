from Card import Card
from random import shuffle

class CardDeck:
    drawPile : list[Card]
    discardPile : list[Card]

    def __init__(self):
        self.drawPile = [Card.ACE, Card.KING, Card.QUEEN, Card.JACK, Card.TWO] * 3
        self.discardPile = []

    def draw(self) -> Card:
        if not self.drawPile:
            print("No cards left to draw or reshuffle.")
            raise RuntimeError
        
        drawnCard = self.drawPile.pop()
        if len(self.drawPile) == 1:
            self.drawPile.extend(self.discardPile)
            self.discardPile = []
            self.shuffle()

        return drawnCard

    def shuffle(self) -> None:
        shuffle(self.drawPile)

    def discard(self, discardedCard : Card) -> bool:
        """Adds card to discard pile

        Args:
            discardedCard (Card): discarded card

        Returns:
            bool: if the discarded card is Card.ANY, match is forfeited
        """
        if discardedCard == Card.ANY:
            return True
        
        self.discardPile.append(discardedCard)
        return False
