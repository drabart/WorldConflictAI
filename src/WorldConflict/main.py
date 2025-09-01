from .Game import Game
from .HumanAgent import HumanAgent

def main():
    agents = [HumanAgent()] * 2
    game = Game(agents)

    while(game.game_state.score[0] < 100 and game.game_state.score[1] < 100):
        game.process_game_step()

if __name__ == "__main__":
    main()