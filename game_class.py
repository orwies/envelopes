from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy
from envelope import Envelope

class Game:
    """
    Runs the game
    Lets the player choose a strategy then prints the results and record it
    """
    def start_game():

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


        n = int(input("Choose strategy 1-4: "))
        if n==1:
            player = RandomStrategy()
            value, num = player.play()
            result = GameResult(value, max_value, num)
             
        elif n==2:
            player = StopAfterNOpensStrategy()
            n = int(input("Choose the number of opens 1-100"))
            player.set_n(n)
            value, num = player.play()
            result = GameResult(value, max_value, num)
        
        elif n==3:
            player = BetterThanPercentStrategy()
            p = int(input("Choose the percent of division 0-1"))
            player.set_percent(p)
            value, num = player.play()
            result = GameResult(value, max_value, num)
        
        elif n==4:
            player = MaxAfterNStrategy()
            n = int(input("Choose the number of changes 0-99"))
            player.set_n(n)
            value, num = player.play()
            result = GameResult(value, max_value, num)
        

class GameResult:
    """
    Recording of the game's result
    """
    def __init__(self, value,max,num):
        self.__chosen_value = value
        self.__max_value = max
        self.__num_of_opens = num
        self.__is_win = (value==max)


