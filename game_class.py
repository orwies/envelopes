from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy
from envelope import Envelope

class Game:
    """
    Runs a single game between a player strategy and the envelopes
    """
    @staticmethod
    def start_game(player):
        envelopes = []
        used_values = []
        max_value = 0

        while len(envelopes) < 100:
            new = Envelope()
            new_value = new.get_value()
            if new_value not in used_values:
                envelopes.append(new)
                used_values.append(new_value)
                if new_value > max_value:
                    max_value = new_value

        value, num = player.play(envelopes)
        return GameResult(value, max_value, num)

        

class GameResult:
    """
    Recording of the game's result
    """
    def __init__(self, value,max,num):
        self.__chosen_value = value
        self.__max_value = max
        self.__num_of_opens = num
        self.__is_win = (value==max)


