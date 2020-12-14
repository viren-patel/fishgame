import unittest
from unittest import mock
import sys
sys.path.insert(1, '../../')
from Remote.server import FishServer, FishClient, is_move, is_posn


class TestServerHelpers(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_is_posn(self):
        good_posn = [0, 1]
        bad_posn_wrong_len = [1, 2, 3]
        bad_posn_wrong_type = ['a', 'b'] 

        self.assertTrue(is_posn(good_posn))
        self.assertFalse(is_posn(bad_posn_wrong_len))
        self.assertFalse(is_posn(bad_posn_wrong_type))

    def test_is_move(self):
        good_move = [[1, 2], [2, 1]]
        bad_move_wrong_len = [[1, 2]]
        bad_move_wrong_type = [[1, 2], [1]]

        self.assertTrue(is_move(good_move))
        self.assertFalse(is_move(bad_move_wrong_len))
        self.assertFalse(is_move(bad_move_wrong_type))


class TestFishClient(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.mock_client = None

    def setUp(self):
        mock_socket = mock.Mock()
        self.mock_client = FishClient(mock_socket, ("localhost", 12345))

    def test_get_player_name(self):
        self.mock_client.client_socket.recv.return_value="mike"
        self.assertEqual("mike", self.mock_client.get_player_name())

        self.mock_client.client_socket.recv.return_value="#7&!"
        self.assertTrue(self.mock_client.get_player_name() is None)

    def test_end_connection(self):
        self.mock_client.end_connection()
        self.mock_client.client_socket.close.assert_called()
        self.assertTrue(self.mock_client.closed)



class TestFishServer(unittest.TestCase):
    pass
