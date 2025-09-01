from .Move import Move
from .Card import Card

class Inventory:
    money: int
    cards: list[Card]

    def __init__(self) -> None:
        self.money = 2
        self.cards = []

    def get_legal_moves(self, last_move: Move) -> list[Move]:
        """Gives list of possible moves based on the last move (any card could be bluffed, cards are not included in checking)

        Args:
            last_move (Move): last move done in sequence (if the sequence is empty Move.OK should be passed)

        Returns:
            list[Move]: list of all legal moves in the players position
        """
        match last_move:
            case Move.OK | Move.CALL_BLUFF:
                possibleMoves: list[Move] = []

                if self.money >= 10:
                    return [Move.PLAY_AFFAIR]
                
                possibleMoves.extend([Move.PLAY_ACE, Move.PLAY_KING, Move.PLAY_TWO, Move.PLAY_PLUS_ONE, Move.PLAY_PLUS_TWO])

                if self.money >= 3:
                    possibleMoves.append(Move.PLAY_JACK)

                if self.money >= 7:
                    possibleMoves.append(Move.PLAY_AFFAIR)

                return possibleMoves

            case Move.PLAY_ACE | Move.PLAY_KING | Move.BLOCK_JACK_WITH_QUEEN | Move.BLOCK_TWO_WITH_ACE | Move.BLOCK_TWO_WITH_TWO | Move.BLOCK_PLUS_TWO_WITH_KING:
                return [Move.OK, Move.CALL_BLUFF]
            
            case Move.PLAY_JACK:
                return [Move.OK, Move.CALL_BLUFF, Move.BLOCK_JACK_WITH_QUEEN]
            
            case Move.PLAY_TWO:
                return [Move.OK, Move.CALL_BLUFF, Move.BLOCK_TWO_WITH_ACE, Move.BLOCK_TWO_WITH_TWO]
            
            case Move.PLAY_PLUS_ONE | Move.PLAY_AFFAIR:
                return [Move.OK]
            
            case Move.PLAY_PLUS_TWO:
                return [Move.OK, Move.BLOCK_PLUS_TWO_WITH_KING]
            
            case Move.FORFEIT:
                return []
            
    def __str__(self) -> str:
        return f"{str(self.cards)}, {self.money} coins" 
