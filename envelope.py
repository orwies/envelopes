import random


class Envelope:
    """
    Basic Envelope class
    """
    def __init__(self):
        """
        Initiates the class with random value
        """
        self.__value = random.randint(1,1000)

    def get_value(self):
        """
        Value get method
        """
        return self.__value
