import json
from copy import deepcopy


class Player:
    def __init__(self, color: str, score: int, penguins: list):
        self.color = color
        self.score = score
        self.penguin_locations = []
        for penguin in penguins:
            self.penguin_locations.append((penguin[0], penguin[1]))

    def get_penguin_locations(self):
        return self.penguin_locations

    def get_color(self):
        return self.color

    def get_score(self):
        return self.score

    @staticmethod
    def dictToPlayer(player_dict: dict):
        return Player(player_dict['color'],
                      player_dict['score'],
                      player_dict['places'])

    def toDict(self):
        return {
            "color": self.color,
            "score": self.score,
            "places": self.penguin_locations
        }

    def add_penguin(self, location: tuple):
        if location not in self.penguin_locations:
            self.penguin_locations.append((location[0], location[1]))

    def remove_penguin(self, location: tuple):
        for i in range(len(self.penguin_locations)):
            if self.penguin_locations[i] == location:
                self.penguin_locations.pop(i)
                return

    def move_penguin(self, origin: tuple, destination: tuple):
        if origin in self.penguin_locations:
            idx = self.penguin_locations.index(origin)
            self.penguin_locations[idx] = destination

    def add_score(self, score: int):
        self.score = self.score + score

    @staticmethod
    def fromPlayer(player: 'Player'):
        return deepcopy(player)

    def __str__(self):
        return json.dumps(self.toDict())

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.get_color() == other.get_color() \
               and self.get_score() == other.get_score() \
               and self.get_penguin_locations() == other.get_penguin_locations()
