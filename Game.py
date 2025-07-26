from Move import Move
from IAgent import IAgent
from GameState import GameState
from Card import Card
from copy import deepcopy
          
class Game():
    agents : list[IAgent]
    gameState : GameState

    def __init__(self):
        self.newGame()

    def newGame(self):
        self.gameState = GameState(2)

        for _ in range(2):
            for player in range(2):
                draw = self.gameState.deck.draw()
                self.agents[player].receiveCard(draw)

    def processMove(self):
        self.gameState.currentSequence = self.gameState.currentSequence[1:]

        if self.gameState.currentSequence == []:
            print("The processed move has an empty sequence")
            raise RuntimeError()
        
        initialAgent = self.agents[self.gameState.initialPlayer]
        turnAgent = self.agents[(self.gameState.initialPlayer + len(self.gameState.currentSequence) - 1) % len(self.gameState.players)]
        deck = self.gameState.deck
        initialForfeit = False
        turnForfeit = False

        match self.gameState.currentSequence[0]:
            case Move.PLAY_ACE:
                # demand ace, give 3 cards, demand 2 cards back
                initialForfeit = deck.discard(initialAgent.giveCard(Card.ACE))
                for _ in range(3):
                    draw = deck.draw()
                    initialAgent.receiveCard(draw)
                
                initialAgent.giveCard(Card.ANY)
                initialAgent.giveCard(Card.ANY)

            case Move.PLAY_KING:
                # give money, demand king
                initialAgent.receiveMoney(3)
                initialForfeit = deck.discard(initialAgent.giveCard(Card.KING))
                initialAgent.receiveCard(deck.draw())

            case Move.PLAY_JACK:
                if len(self.gameState.currentSequence) > 1 and self.gameState.currentSequence[1] == Move.BLOCK_JACK_WITH_QUEEN:
                    # nothing, demand jack and queen
                    initialForfeit = deck.discard(initialAgent.giveCard(Card.JACK))
                    initialAgent.receiveCard(deck.draw())

                    turnForfeit = deck.discard(turnAgent.giveCard(Card.QUEEN))
                    turnAgent.receiveCard(deck.draw())
                else:
                    # pay, demand jack, demand card permamently
                    initialAgent.giveMoney(3)

                    initialForfeit = deck.discard(initialAgent.giveCard(Card.JACK))
                    initialAgent.receiveCard(deck.draw())

                    turnForfeit = deck.discard(turnAgent.giveCard(Card.ANY))
                    if turnAgent.hasLost():
                        turnForfeit = True

            case Move.PLAY_TWO:
                if len(self.gameState.currentSequence) > 1 and self.gameState.currentSequence[1] == Move.BLOCK_TWO_WITH_ACE:
                    # nothing, demand two and ace
                    initialForfeit = deck.discard(initialAgent.giveCard(Card.TWO))
                    initialAgent.receiveCard(deck.draw())

                    turnForfeit = deck.discard(turnAgent.giveCard(Card.ACE))
                    turnAgent.receiveCard(deck.draw())
                elif len(self.gameState.currentSequence) > 1 and self.gameState.currentSequence[1] == Move.BLOCK_TWO_WITH_TWO:
                    # nothing, demand two and two
                    initialForfeit = deck.discard(initialAgent.giveCard(Card.TWO))
                    initialAgent.receiveCard(deck.draw())

                    turnForfeit = deck.discard(turnAgent.giveCard(Card.TWO))
                    turnAgent.receiveCard(deck.draw())
                else:
                    initialAgent.receiveMoney(2)
                    turnAgent.giveMoney(2)

            case Move.PLAY_PLUS_ONE:
                initialAgent.receiveMoney(1)

            case Move.PLAY_PLUS_TWO:
                if len(self.gameState.currentSequence) > 1 and self.gameState.currentSequence[1] == Move.BLOCK_PLUS_TWO_WITH_KING:
                    # nothing, demand king
                    turnForfeit = deck.discard(turnAgent.giveCard(Card.KING))
                    turnAgent.receiveCard(deck.draw())
                else:
                    initialAgent.receiveMoney(2)

            case Move.PLAY_AFFAIR:
                # demand card permamently
                initialAgent.giveMoney(7)
                turnForfeit = deck.discard(turnAgent.giveCard(Card.ANY))
                if turnAgent.hasLost():
                    turnForfeit = True

            case _:
                print("Invalid move in the sequence")
                raise RuntimeError
        
        self.gameState.initialPlayer = (self.gameState.initialPlayer + 1) % len(self.gameState.players)
        self.gameState.turnPlayer = self.gameState.initialPlayer

        if turnForfeit:
            self.gameState.score[self.gameState.turnPlayer] += 1
        
        if initialForfeit:
            self.gameState.score[self.gameState.initialPlayer] += 1

        if turnForfeit or initialForfeit:
            self.newGame()

    def processBluff(self):
        pass

    def makeMove(self) -> bool:
        move = self.agents[self.gameState.turnPlayer].giveMove(deepcopy(self.gameState))
        
        match move:
            case Move.OK:
                self.processMove()
                self.currentSequence = [Move.OK]
            case Move.CALL_BLUFF:
                self.processBluff()
                self.currentSequence = [Move.OK]
            case _:
                self.gameState.currentSequence.append(move)
                self.gameState.turnPlayer += 1
                self.gameState.turnPlayer %= len(self.gameState.players)

        return True
