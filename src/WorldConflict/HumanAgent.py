from .GameState import PlayerInfo
from .IAgent import IAgent
from .Card import Card
from .Move import Move

class HumanAgent(IAgent):
    player_info: PlayerInfo

    def __init__(self) -> None:
        super().__init__()

    def generate_give_card(self, state: PlayerInfo, card_preference: Card) -> Card:
        self.player_info = state
        
        print(f"Player {self.player_info.playerId + 1}")
        print(f"You are requested to give {card_preference}\nYou have {self.player_info.player}")
        raw_card = input()
        match raw_card:
            case "two":
                return Card.TWO
            case "jack":
                return Card.JACK
            case "queen":
                return Card.QUEEN
            case "king":
                return Card.KING
            case "ace":
                return Card.ACE
            case _:
                return Card.ANY
    
    def generate_move(self, state: PlayerInfo) -> Move:
        self.player_info = state

        print(f"Player {self.player_info.playerId + 1}")    
        print(f"""You are requested to choose a move out of
{state.player.get_legal_moves(Move.OK) \
if len(state.current_sequence) == 0 \
else state.player.get_legal_moves(state.current_sequence[-1])}""")
        print(state)
        raw_move = input()
        match raw_move:
            case "ok":
                return Move.OK
            case "cb":
                return Move.CALL_BLUFF
            case "p2":
                return Move.PLAY_TWO
            case "pj":
                return Move.PLAY_JACK
            case "pk":
                return Move.PLAY_KING
            case "pa":
                return Move.PLAY_ACE
            case "a":
                return Move.PLAY_AFFAIR
            case "p1":
                return Move.PLAY_PLUS_ONE
            case "p2":
                return Move.PLAY_PLUS_TWO
            case "bjwq":
                return Move.BLOCK_JACK_WITH_QUEEN
            case "bp2wk":
                return Move.BLOCK_PLUS_TWO_WITH_KING
            case "b2wa":
                return Move.BLOCK_TWO_WITH_ACE
            case "b2w2":
                return Move.BLOCK_TWO_WITH_TWO
            case _:
                return Move.FORFEIT
