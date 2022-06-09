from abc import ABCMeta, abstractmethod


class ScoreBoardDao(metaclass=ABCMeta):

    @abstractmethod
    def insert_player(self, markers):
        pass

    @abstractmethod
    def insert_default_players(self, markers):
        pass

    @abstractmethod
    def read_players(self):
        pass

    @abstractmethod
    def read_player(self, name_surname):
        pass

    @abstractmethod
    def delete_player(self, player):
        pass

    @abstractmethod
    def get_player_level(self, player):
        pass

    @abstractmethod
    def top_players(self):
        pass

