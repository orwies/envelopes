from abc import ABC, abstractmethod
from envelope import Envelope
import random

class Strategy(ABC):
    """
    Abstract class for the strategies
    """

    @abstractmethod
    def play(self, envelopes):
        pass


class RandomStrategy(Strategy):
    """
    The random strategy class
    """
    def play(self, envelopes):
        index = random.randint(0,99)
        value = envelopes[index].get_value()
        print(f"The Chosen Envelope's value is {value}.")
        return value, index+1

    
class StopAfterNOpensStrategy(Strategy):
    """
    The N opens strategy class
    """
    def __init__(self):
        self.__n = 1
    
    def set_n(self,n):
        self.__n = n

    def play(self, envelopes):
        value = envelopes[self.__n-1].get_value()
        print(f"The Chosen Envelope's value is {value}.")
        return value, self.__n
    

class BetterThanPercentStrategy(Strategy):
    """
    Finds the max value of the first N% of the envelopes,
    then finds the first larger value from the rest.
    """
    def __init__(self):
        self.__percent = 0.25
        self.__number_of_opens = 0

    def set_percent(self, percent: float):
        self.__percent = percent

    def _find_max(self, lst):
        max_val = lst[0].get_value()
        for e in lst:
            self.__number_of_opens += 1
            if e.get_value() > max_val:
                max_val = e.get_value()
        return max_val

    def _find_first_max(self, lst, max_val):
        for e in lst:
            self.__number_of_opens += 1
            if e.get_value() > max_val:
                return e.get_value()
        return lst[-1].get_value()   # כאן היה באג אצלך, צריך להחזיר value

    def play(self, envelopes):
        split_index = int(len(envelopes) * self.__percent)
        if split_index == 0:  # הגנה אם percent קטן מדי
            split_index = 1

        first_slice = envelopes[:split_index]
        second_slice = envelopes[split_index:]

        first_max = self._find_max(first_slice)
        chosen_value = self._find_first_max(second_slice, first_max)

        print(f"The Chosen Envelope's value is {chosen_value}.")
        return chosen_value, self.__number_of_opens
        
    
def play(self, envelopes):
    split_index = int(len(envelopes) * self.__percent)  # המרה ל-int
    print(split_index)
    first_slice = envelopes[:split_index]
    second_slice = envelopes[split_index:]

    first_max = self._find_max(first_slice)
    second_max = self._find_first_max(second_slice, first_max)
    print(f"The Chosen Envelope's value is {second_max}.")
    return second_max, self.__number_of_opens



class MaxAfterNStrategy(Strategy):
    """
    Finds the largest value after N changes
    """
    def __init__(self):
        self.__n = 0
    
    def set_n(self, n):
        self.__n = n

    def play(self, envelopes):
        count = 0
        number_of_opens = 0
        max_val = envelopes[0].get_value()

        for e in envelopes:
            number_of_opens += 1
            if e.get_value() > max_val:
                count += 1
                max_val = e.get_value()
            if count == self.__n:
                print(f"The Chosen Envelope's value is {max_val}.")
                return max_val, number_of_opens   # ← תמיד מחזיר tuple

        # אם לא הגענו ל־n שינויים, לוקחים את האחרון
        last_val = envelopes[-1].get_value()
        print(f"The Chosen Envelope's value is {last_val}.")
        return last_val, number_of_opens

        


class Testing:
    def main():
        envelopes = []
        for i in range(100):
            envelopes.append(Envelope())
        test = MaxAfterNStrategy()
        test.set_n(2)
        print(test.play(envelopes))
    
