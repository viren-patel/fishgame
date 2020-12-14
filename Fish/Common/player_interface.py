from Common.state import State


class Player_Interface:
    """
    Player_Interface - An abstract class designed to represent the basic functionality necessary for communication between players and the referee component.  The referee with use the functions of the class to
        communicate with players, sending games states and error messages, while recieving player moves and identification.
    """

    def get_placement(self):
        pass

    def get_next_move(self):
        pass

    def update_state(self, state: State):
        pass

    def decrement_turn_idx(self):
        pass
