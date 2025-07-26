from Move import Move
from IAgent import IAgent
from GameState import GameState
from Card import Card
from copy import deepcopy
          
class Game:
    agents: list[IAgent]
    game_state: GameState

    def __init__(self):
        self.new_game()

    def new_game(self):
        self.game_state = GameState(2)

        for _ in range(2):
            for player in range(2):
                draw = self.game_state.deck.draw()
                self.agents[player].receive_card(draw)

    def process_move(self):
        self.game_state.current_sequence = self.game_state.current_sequence[1:]

        if not self.game_state.current_sequence:
            print("The processed move has an empty sequence")
            raise RuntimeError()
        
        initialAgent = self.agents[self.game_state.initialPlayer]
        turnAgent = self.agents[(self.game_state.initialPlayer + len(self.game_state.current_sequence) - 1) % len(self.game_state.players)]
        deck = self.game_state.deck
        initialForfeit = False
        turnForfeit = False

        match self.game_state.current_sequence[0]:
            case Move.PLAY_ACE:
                # demand ace, give 3 cards, demand 2 cards back
                initialForfeit = deck.discard(initialAgent.give_card(Card.ACE))
                for _ in range(3):
                    draw = deck.draw()
                    initialAgent.receive_card(draw)
                
                initialAgent.give_card(Card.ANY)
                initialAgent.give_card(Card.ANY)

            case Move.PLAY_KING:
                # give money, demand king
                initialAgent.receive_money(3)
                initialForfeit = deck.discard(initialAgent.give_card(Card.KING))
                initialAgent.receive_card(deck.draw())

            case Move.PLAY_JACK:
                if len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_JACK_WITH_QUEEN:
                    # nothing, demand jack and queen
                    initialForfeit = deck.discard(initialAgent.give_card(Card.JACK))
                    initialAgent.receive_card(deck.draw())

                    turnForfeit = deck.discard(turnAgent.give_card(Card.QUEEN))
                    turnAgent.receive_card(deck.draw())
                else:
                    # pay, demand jack, demand card permanently
                    initialAgent.give_money(3)

                    initialForfeit = deck.discard(initialAgent.give_card(Card.JACK))
                    initialAgent.receive_card(deck.draw())

                    turnForfeit = deck.discard(turnAgent.give_card(Card.ANY))
                    if turnAgent.has_lost():
                        turnForfeit = True

            case Move.PLAY_TWO:
                if len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_TWO_WITH_ACE:
                    # nothing, demand two and ace
                    initialForfeit = deck.discard(initialAgent.give_card(Card.TWO))
                    initialAgent.receive_card(deck.draw())

                    turnForfeit = deck.discard(turnAgent.give_card(Card.ACE))
                    turnAgent.receive_card(deck.draw())
                elif len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_TWO_WITH_TWO:
                    # nothing, demand two and two
                    initialForfeit = deck.discard(initialAgent.give_card(Card.TWO))
                    initialAgent.receive_card(deck.draw())

                    turnForfeit = deck.discard(turnAgent.give_card(Card.TWO))
                    turnAgent.receive_card(deck.draw())
                else:
                    initialAgent.receive_money(2)
                    turnAgent.give_money(2)

            case Move.PLAY_PLUS_ONE:
                initialAgent.receive_money(1)

            case Move.PLAY_PLUS_TWO:
                if len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_PLUS_TWO_WITH_KING:
                    # nothing, demand king
                    turnForfeit = deck.discard(turnAgent.give_card(Card.KING))
                    turnAgent.receive_card(deck.draw())
                else:
                    initialAgent.receive_money(2)

            case Move.PLAY_AFFAIR:
                # demand card permanently
                initialAgent.give_money(7)
                turnForfeit = deck.discard(turnAgent.give_card(Card.ANY))
                if turnAgent.has_lost():
                    turnForfeit = True

            case _:
                print("Invalid move in the sequence")
                raise RuntimeError
        
        self.game_state.initialPlayer = (self.game_state.initialPlayer + 1) % len(self.game_state.players)
        self.game_state.turnPlayer = self.game_state.initialPlayer

        if turnForfeit:
            self.game_state.score[self.game_state.turnPlayer] += 1
        
        if initialForfeit:
            self.game_state.score[self.game_state.initialPlayer] += 1

        if turnForfeit or initialForfeit:
            self.new_game()

    def process_bluff(self):
        pass

    def make_move(self) -> bool:
        move = self.agents[self.game_state.turnPlayer].give_move(deepcopy(self.game_state))
        
        match move:
            case Move.OK:
                self.process_move()
                self.current_sequence = [Move.OK]
            case Move.CALL_BLUFF:
                self.process_bluff()
                self.current_sequence = [Move.OK]
            case _:
                self.game_state.current_sequence.append(move)
                self.game_state.turnPlayer += 1
                self.game_state.turnPlayer %= len(self.game_state.players)

        return True
