from enum import Enum

class Move(Enum):
    OK = 0
    CALL_BLUFF = 1
    PLAY_ACE = 2
    PLAY_KING = 3
    PLAY_JACK = 5
    PLAY_TWO = 6
    BLOCK_JACK_WITH_QUEEN = 7
    BLOCK_TWO_WITH_ACE = 8
    BLOCK_TWO_WITH_TWO = 9
    PLAY_PLUS_ONE = 10
    PLAY_PLUS_TWO = 11
    BLOCK_PLUS_TWO_WITH_KING = 12
    PLAY_AFFAIR = 13
    FORFEIT = 14
