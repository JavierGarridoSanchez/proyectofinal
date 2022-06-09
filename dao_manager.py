from scoreboard_dao_imple import ScoreBoardDaoImple


class DaoManager:

    def __init__(self):
        self.dao_markers = None

    def get_dao_markers(self):
        self.dao_markers = ScoreBoardDaoImple()
        return self.dao_markers
