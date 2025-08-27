from Move import Move
from IAgent import IAgent
from GameState import GameState, PlayerInfo
from Card import Card
from copy import deepcopy
from typing import Sequence
from Inventory import Inventory

def has_lost(inventory: Inventory) -> bool:
        return inventory.cards == []
    
def has_bluffed(move: Move, inventory: Inventory) -> bool:
    """checks whether the player has required card

    Args:
        move (Move): move to check against

    Returns:
        bool: true if the player does not have required card
    """
    match move:
        case Move.PLAY_ACE | Move.BLOCK_TWO_WITH_ACE:
            return Card.ACE in inventory.cards
        case Move.PLAY_KING | Move.BLOCK_PLUS_TWO_WITH_KING:
            return Card.KING in inventory.cards
        case Move.BLOCK_JACK_WITH_QUEEN:
            return Card.QUEEN in inventory.cards
        case Move.PLAY_JACK:
            return Card.JACK in inventory.cards
        case Move.PLAY_TWO | Move.BLOCK_TWO_WITH_TWO:
            return Card.TWO in inventory.cards
        case _:
            print("Move should not have been possible to call bluff on")
            return False

def give_money(income: int, inventory: Inventory) -> None:
    """Called by the game when a player receives money

    Args:
        income (int): amount of income
    """
    inventory.money += income

def give_card(card: Card, inventory: Inventory) -> None:
    inventory.cards.append(card)

def take_money(cost: int, inventory: Inventory) -> int:
    """Called by the game, when a player has to pay

    Args:
        cost (int): amount to pay

    Returns:
        int: the paid amount (can be not full for the steal action)
    """

    cost = min(cost, inventory.money)
    inventory.money -= cost
    return cost

def take_card(state: GameState, player_id: int, card_preference: Card, inventory: Inventory, player: IAgent) -> Card:
    """Called by the game when the player is forced to discard

    Args:
        card_preference (Card): 
            The card that the player should discard, if they have it on their hand
            If the cardPreference is Card.ANY, or if the player does not have the 
            preferred card (e.g. After bluffing), they can discard any one of their cards.

    Returns:
        Card: The card player decides to discard
    """
    playerState = PlayerInfo(state, player_id)
    card = player.generate_give_card(playerState, card_preference)
    if card not in inventory.cards or (card_preference != Card.ANY and card != card_preference and card_preference in inventory.cards):
        # will be interpreted as forfeit
        return Card.ANY
    
    inventory.cards.remove(card)
    return card

def take_move(state: GameState, inventory: Inventory, player: IAgent) -> Move:
    """Called by the game when player has to make a move

    Args:
        state (GameState): the current state of the game

    Returns:
        Move: The move player wants to make 
    """
    playerState = PlayerInfo(state, state.turnPlayer)
    move = player.generate_move(playerState)
    if (len(state.current_sequence) == 0 and move not in inventory.get_legal_moves(Move.OK)) or \
        (len(state.current_sequence) != 0 and move not in inventory.get_legal_moves(state.current_sequence[-1])):
        return Move.FORFEIT
    
    return move
          
class Game:
    agents: Sequence[IAgent]
    game_state: GameState

    def __init__(self, agents: Sequence[IAgent]):
        self.agents = agents
        self.new_game()

    
    def new_game(self):
        self.game_state = GameState(2)

        for _ in range(2):
            for player in range(2):
                draw = self.game_state.deck.draw()
                give_card(draw, self.game_state.players[player])

    def process_move(self):
        if not self.game_state.current_sequence:
            print("The processed move has an empty sequence")
            raise RuntimeError()
        initial_player_id = self.game_state.initial_player
        initialAgent = self.agents[initial_player_id]
        initialAgentInventory = self.game_state.players[initial_player_id]

        turn_player_id = self.game_state.turnPlayer
        turnAgent = self.agents[turn_player_id]
        turnAgentInventory = self.game_state.players[turn_player_id]

        deck = self.game_state.deck
        initialForfeit = False
        turnForfeit = False

        match self.game_state.current_sequence[0]:
            case Move.PLAY_ACE:
                # demand ace, give 3 cards, demand 2 cards back
                initialForfeit = deck.discard(take_card(self.game_state, initial_player_id, Card.ACE, initialAgentInventory, initialAgent))
                for _ in range(3):
                    draw = deck.draw()
                    give_card(draw, initialAgentInventory)
                
                take_card(self.game_state, initial_player_id, Card.ANY, initialAgentInventory, initialAgent)
                take_card(self.game_state, initial_player_id, Card.ANY, initialAgentInventory, initialAgent)

            case Move.PLAY_KING:
                print("aaa", self.game_state.initial_player, self.game_state.current_sequence, initialAgentInventory)
                # give money, demand king
                give_money(3, initialAgentInventory)
                initialForfeit = deck.discard(take_card(self.game_state, initial_player_id, Card.KING, initialAgentInventory, initialAgent))
                give_card(deck.draw(), initialAgentInventory)

            case Move.PLAY_JACK:
                if len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_JACK_WITH_QUEEN:
                    # nothing, demand jack and queen
                    initialForfeit = deck.discard(take_card(self.game_state, initial_player_id, Card.JACK, initialAgentInventory, initialAgent))
                    give_card(deck.draw(), initialAgentInventory)

                    turnForfeit = deck.discard(take_card(self.game_state, turn_player_id, Card.QUEEN, turnAgentInventory, turnAgent))
                    give_card(deck.draw(), turnAgentInventory)
                else:
                    # pay, demand jack, demand card permanently
                    take_money(3, initialAgentInventory)

                    initialForfeit = deck.discard(take_card(self.game_state, initial_player_id, Card.JACK, initialAgentInventory, initialAgent))
                    give_card(deck.draw(), initialAgentInventory)

                    turnForfeit = deck.discard(take_card(self.game_state, turn_player_id, Card.ANY, turnAgentInventory, turnAgent))
                    if has_lost(turnAgentInventory):
                        turnForfeit = True

            case Move.PLAY_TWO:
                if len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_TWO_WITH_ACE:
                    # nothing, demand two and ace
                    initialForfeit = deck.discard(take_card(self.game_state, initial_player_id, Card.TWO, initialAgentInventory, initialAgent))
                    give_card(deck.draw(), initialAgentInventory)

                    turnForfeit = deck.discard(take_card(self.game_state, turn_player_id, Card.ACE, turnAgentInventory, turnAgent))
                    give_card(deck.draw(), turnAgentInventory)
                elif len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_TWO_WITH_TWO:
                    # nothing, demand two and two
                    initialForfeit = deck.discard(take_card(self.game_state, initial_player_id, Card.TWO, initialAgentInventory, initialAgent))
                    give_card(deck.draw(), initialAgentInventory)

                    turnForfeit = deck.discard(take_card(self.game_state, turn_player_id, Card.TWO, turnAgentInventory, turnAgent))
                    give_card(deck.draw(), turnAgentInventory)
                else:
                    give_money(2, initialAgentInventory)
                    take_money(2, turnAgentInventory)

            case Move.PLAY_PLUS_ONE:
                give_money(1, initialAgentInventory)

            case Move.PLAY_PLUS_TWO:
                if len(self.game_state.current_sequence) > 1 and self.game_state.current_sequence[1] == Move.BLOCK_PLUS_TWO_WITH_KING:
                    # nothing, demand king
                    turnForfeit = deck.discard(take_card(self.game_state, turn_player_id, Card.KING, turnAgentInventory, turnAgent))
                    give_card(deck.draw(), turnAgentInventory)
                else:
                    give_money(2, initialAgentInventory)

            case Move.PLAY_AFFAIR:
                # demand card permanently
                take_money(7, initialAgentInventory)
                turnForfeit = deck.discard(take_card(self.game_state, turn_player_id, Card.ANY, turnAgentInventory, turnAgent))
                if has_lost(turnAgentInventory):
                    turnForfeit = True

            case _:
                print("Invalid move in the sequence")
                raise RuntimeError
            
        return initialForfeit, turnForfeit
        

    def process_bluff(self):
        self.game_state.current_sequence = self.game_state.current_sequence[1:]

        if not self.game_state.current_sequence:
            print("The processed move has an empty sequence")
            raise RuntimeError()
        
        previousAgentID = (self.game_state.initial_player + len(self.game_state.current_sequence) - 2) % len(self.game_state.players)
        previousAgentInventory = self.game_state.players[previousAgentID]
        previousAgent = self.agents[previousAgentID]

        turn_player_id = self.game_state.turnPlayer
        turnAgentInventory = self.game_state.players[turn_player_id]
        turnAgent = self.agents[turn_player_id]

        if has_bluffed(self.game_state.current_sequence[-1], previousAgentInventory):
            take_card(self.game_state, previousAgentID, Card.ANY, previousAgentInventory, previousAgent)
            
            if has_lost(previousAgentInventory):
                self.new_game()
        else:
            take_card(self.game_state, turn_player_id, Card.ANY, turnAgentInventory, turnAgent)
            
            if has_lost(turnAgentInventory):
                self.new_game()
            else:
                self.process_move()

    def make_move(self, move: Move) -> bool:
        match move:
            case Move.FORFEIT:
                self.game_state.score[self.game_state.turnPlayer] += 1
                return True
            case Move.OK:
                initial_forfeit, turn_orfeit = self.process_move()

                self.game_state.initial_player = (self.game_state.initial_player + 1) % len(self.game_state.players)
                self.game_state.turnPlayer = self.game_state.initial_player

                if turn_orfeit:
                    self.game_state.score[self.game_state.turnPlayer] += 1
                
                if initial_forfeit:
                    self.game_state.score[self.game_state.initial_player] += 1

                if turn_orfeit or initial_forfeit:
                    return True
                
                self.game_state.current_sequence = []
            case Move.CALL_BLUFF:
                self.process_bluff()
                self.game_state.current_sequence = []
            case _:
                self.game_state.current_sequence.append(move)
                self.game_state.turnPlayer += 1
                self.game_state.turnPlayer %= len(self.game_state.players)

        return False
    
    def process_game(self):
        move = take_move(deepcopy(self.game_state), self.game_state.players[self.game_state.turnPlayer], self.agents[self.game_state.turnPlayer])
        game_ended = self.make_move(move)

        if game_ended:
            self.game_state.reset()


