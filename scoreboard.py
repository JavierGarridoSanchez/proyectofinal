class ScoreBoard:
    def __init__(self, name_surname, score, kills, coins, level):
        self.__name_surname = name_surname
        self.__score = score
        self.__kills = kills
        self.__coins = coins
        self.__level = level

    # nombre y apellido
    @property
    def name_surname(self):
        return self.__name_surname

    # setter method
    @name_surname.setter
    def name_surname(self, name_surname):
        self.__name_surname = name_surname

    @property
    def score(self):
        return self.__score

    # setter method
    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def kills(self):
        return self.__kills

    # setter method
    @kills.setter
    def kills(self, kills):
        self.__kills = kills

    @property
    def coins(self):
        return self.__coins

    # setter method
    @coins.setter
    def coins(self, coins):
        self.__coins = coins

    @property
    def level(self):
        return self.__level

    # setter method
    @level.setter
    def level(self, level):
        self.__level = level
