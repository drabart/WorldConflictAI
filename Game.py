from Move import Move
from IAgent import IAgent
from GameState import GameState, PlayerInfo
from Card import Card
from CardDeck import CardDeck
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

def take_card(card_preference: Card, inventory: Inventory, player: IAgent, state: PlayerInfo) -> Card:
    """Called by the game when the player is forced to discard

    Args:
        card_preference (Card): 
            The card that the player should discard, if they have it on their hand
            If the cardPreference is Card.ANY, or if the player does not have the 
            preferred card (e.g. After bluffing), they can discard any one of their cards.

    Returns:
        Card: The card player decides to discard
    """
    card = player.generate_give_card(state, card_preference)
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
        self.game_state.reset()

        for _ in range(2):
            for player in range(2):
                draw = self.game_state.deck.draw()
                give_card(draw, self.game_state.players[player])

    def two_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        sequence = self.game_state.current_sequence
        if len(sequence) > 2:
            raise RuntimeError("Too many moves in a sequence")
        
        response = None if len(sequence) == 1 else sequence[1]

        initial_player_info = PlayerInfo(self.game_state, initial_player_id)
        turn_player_info = PlayerInfo(self.game_state, turn_player_id)

        match response:
            case Move.BLOCK_TWO_WITH_ACE:
                # nothing, demand two and ace
                initial_forfeit = deck.discard(take_card(Card.TWO, initial_inventory, initial_agent, initial_player_info))
                give_card(deck.draw(), initial_inventory)

                turn_forfeit = deck.discard(take_card(Card.ACE, turn_inventory, turn_agent, turn_player_info))
                give_card(deck.draw(), turn_inventory)
            case Move.BLOCK_TWO_WITH_TWO:
                # nothing, demand two and two
                initial_forfeit = deck.discard(take_card(Card.TWO, initial_inventory, initial_agent, initial_player_info))
                give_card(deck.draw(), initial_inventory)

                turn_forfeit = deck.discard(take_card(Card.TWO, turn_inventory, turn_agent, turn_player_info))
                give_card(deck.draw(), turn_inventory)
            case None:
                give_money(2, initial_inventory)
                take_money(2, turn_inventory)
            case _:
                raise RuntimeError("Invalid response")

        return initial_forfeit, turn_forfeit

    def jack_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        sequence = self.game_state.current_sequence
        if len(sequence) > 2:
            raise RuntimeError("Too many moves in a sequence")
        
        response = None if len(sequence) == 1 else sequence[1]

        initial_player_info = PlayerInfo(self.game_state, initial_player_id)
        turn_player_info = PlayerInfo(self.game_state, turn_player_id)

        match response:
            case Move.BLOCK_JACK_WITH_QUEEN:
                # nothing, demand jack and queen
                initial_forfeit = deck.discard(take_card(Card.JACK, initial_inventory, initial_agent, initial_player_info))
                give_card(deck.draw(), initial_inventory)

                turn_forfeit = deck.discard(take_card(Card.QUEEN, turn_inventory, turn_agent, turn_player_info))
                give_card(deck.draw(), turn_inventory)

            case None:
                # pay, demand jack, demand card permanently
                take_money(3, initial_inventory)

                initial_forfeit = deck.discard(take_card(Card.JACK, initial_inventory, initial_agent, initial_player_info))
                give_card(deck.draw(), initial_inventory)

                turn_forfeit = deck.discard(take_card(Card.ANY, turn_inventory, turn_agent, turn_player_info))
                if has_lost(turn_inventory):
                    turn_forfeit = True
        
            case _:
                raise RuntimeError("Invalid response")

        return initial_forfeit, turn_forfeit

    def king_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        # give money, demand king
        give_money(3, initial_inventory)
        initial_forfeit = deck.discard(take_card(Card.KING, initial_inventory, initial_agent, PlayerInfo(self.game_state, initial_player_id)))
        give_card(deck.draw(), initial_inventory)

        return initial_forfeit, turn_forfeit

    def ace_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        initial_player_info = PlayerInfo(self.game_state, initial_player_id)

        # demand ace, give 3 cards, demand 2 cards back
        initial_forfeit = deck.discard(take_card(Card.ACE, initial_inventory, initial_agent, initial_player_info))
        for _ in range(3):
            draw = deck.draw()
            give_card(draw, initial_inventory)
        
        take_card(Card.ANY, initial_inventory, initial_agent, initial_player_info)
        take_card(Card.ANY, initial_inventory, initial_agent, initial_player_info)

        return initial_forfeit, turn_forfeit
    
    def affair_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        # demand card permanently
        take_money(7, initial_inventory)
        turn_forfeit = deck.discard(take_card(Card.ANY, turn_inventory, turn_agent, PlayerInfo(self.game_state, turn_player_id)))
        if has_lost(turn_inventory):
            turn_forfeit = True

        return initial_forfeit, turn_forfeit

    def plus_one_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        give_money(1, initial_inventory)

        return initial_forfeit, turn_forfeit
    
    def plus_two_start(self, deck: CardDeck, initial_player_id: int, initial_agent: IAgent, initial_inventory: Inventory,
                  turn_player_id: int, turn_agent: IAgent, turn_inventory: Inventory) -> tuple[bool, bool]:
        initial_forfeit = False
        turn_forfeit = False

        sequence = self.game_state.current_sequence
        if len(sequence) > 2:
            raise RuntimeError("Too many moves in a sequence")
        
        response = None if len(sequence) == 1 else sequence[1]

        turn_player_info = PlayerInfo(self.game_state, turn_player_id)

        match response:
            case Move.BLOCK_PLUS_TWO_WITH_KING:
                # nothing, demand king
                turn_forfeit = deck.discard(take_card(Card.KING, turn_inventory, turn_agent, turn_player_info))
                give_card(deck.draw(), turn_inventory)

            case None:
                give_money(2, initial_inventory)
        
            case _:
                raise RuntimeError("Invalid response")

        return initial_forfeit, turn_forfeit      

    def process_move(self):
        if not self.game_state.current_sequence:
            print("The processed move has an empty sequence")
            raise RuntimeError()
        
        initial_player_id = self.game_state.initial_player
        initial_agent = self.agents[initial_player_id]
        initial_inventory = self.game_state.players[initial_player_id]

        turn_player_id = self.game_state.turnPlayer
        turn_agent = self.agents[turn_player_id]
        turn_inventory = self.game_state.players[turn_player_id]

        deck = self.game_state.deck

        start_functions = {
            Move.PLAY_TWO: self.two_start,
            Move.PLAY_JACK: self.jack_start,
            Move.PLAY_KING: self.king_start,
            Move.PLAY_ACE: self.ace_start,
            Move.PLAY_AFFAIR: self.affair_start,
            Move.PLAY_PLUS_ONE: self.plus_one_start,
            Move.PLAY_PLUS_TWO: self.plus_two_start
        }

        try:
            return start_functions[self.game_state.current_sequence[0]](
                deck, initial_player_id, initial_agent, initial_inventory, 
                turn_player_id, turn_agent, turn_inventory)
        except KeyError:
            print("Invalid move in the sequence")
            raise RuntimeError

    def process_bluff(self):
        self.game_state.current_sequence = self.game_state.current_sequence[1:]

        if not self.game_state.current_sequence:
            print("The processed move has an empty sequence")
            raise RuntimeError()
        
        previous_player_id = (self.game_state.initial_player + len(self.game_state.current_sequence) - 2) % len(self.game_state.players)
        previous_inventory = self.game_state.players[previous_player_id]
        previous_agent = self.agents[previous_player_id]
        previous_player_info = PlayerInfo(self.game_state, previous_player_id)

        turn_player_id = self.game_state.turnPlayer
        turn_inventory = self.game_state.players[turn_player_id]
        turn_agent = self.agents[turn_player_id]
        turn_player_info = PlayerInfo(self.game_state, turn_player_id)

        if has_bluffed(self.game_state.current_sequence[-1], previous_inventory):
            take_card(Card.ANY, previous_inventory, previous_agent, previous_player_info)
            
            if has_lost(previous_inventory):
                self.new_game()
        else:
            take_card(Card.ANY, turn_inventory, turn_agent, turn_player_info)
            
            if has_lost(turn_inventory):
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


