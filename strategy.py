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
        return value

    
class StopAfterNOpensStrategy(Strategy):
    """
    The N opens strategy class
    """
    def __init__(self):
        self.__n = 0
    
    def set_n(self,n):
        self.__n = n

    def play(self, envelopes):
        value = envelopes[self.__n].get_value()
        print(f"The Chosen Envelope's value is {value}.")
        return value
    

class BetterThanPercentStrategy(Strategy):
    """
    Finds the max value of the first N% of the envelopes, then finds the first larger value from the rest envelopes
    """
    def __init__(self):
        self.__percent = 0.25
    
    def set_percent(self,percent):
        self.__percent = percent

    def _find_max(lst):
            max = lst[0].get_value()
            for e in lst:
                if e.get_value() > max:
                    max = e.get_value()
            return max
    
    def _find_first_max(lst,max):
        for e in lst:
            if e.get_value() > max:
                return e.get_value()
        return lst[-1]
        
    
    def play(self, envelopes):
        split_index = len(envelopes)*self.__percent
        first_slice = envelopes[:split_index]
        second_slice = envelopes[split_index:]

        first_max = self._find_max(first_slice)
        second_max = self._find_first_max(second_slice, first_max)
        print(f"The Chosen Envelope's value is {second_max}.")
        return second_max



class MaxAfterNStrategy(Strategy):
    """
    Finds the largest value after N changes
    """
    def __init__(self):
        self.__n = 0
    
    def set_n(self,n):
        self.__n = n

    def play(self, envelopes):
        count = 0
        max = envelopes[0].get_value()
        for e in envelopes:
            if e.get_value() > max:
                count += 1
                max = e.get_value()
            if (count == self.__n):
                print(f"The Chosen Envelope's value is {max}.")
                return max
        print(f"The Chosen Envelope's value is {envelopes[-1].get_value()}.")
        return envelopes[-1].get_value()
        


class Testing:
    def main():
        envelopes = []
        for i in range(100):
            envelopes.append(Envelope())
        test = MaxAfterNStrategy()
        test.set_n(2)
        test.play(envelopes)
    main()
    
