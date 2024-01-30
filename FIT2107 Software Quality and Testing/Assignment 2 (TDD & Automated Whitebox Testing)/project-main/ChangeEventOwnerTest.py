import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager

class ChangeEventOwnerTest(unittest.TestCase):

    def test_success_change_event_owner(self):
        """
        This test tests whether the user can reassign the owner of the event
        """
        mock_api = Mock()
        MyEventManager.change_event_owner(mock_api, "test id", "DestinationCalendarId")
        self.assertEqual(mock_api.events.return_value.move.return_value.execute.call_count, 1) # Check whether the move function is called

    def test_fail_change_event_owner(self):
        """
        This test tests whether the user can reassign the owner of the event with invalid destination calendar id
        """
        mock_api = Mock()
        mock_api.events.return_value.move.return_value.execute.side_effect = Exception

        with self.assertRaises(Exception):
            MyEventManager.change_event_owner(mock_api, "test id", "DestinationCalendarId")