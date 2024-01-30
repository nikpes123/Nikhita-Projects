import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class RequestChangeTest(unittest.TestCase):
    def test_success_request(self):
        """
        This test tests whether the attendee can request for change of time or venue for the respective event
        """
        mock_api = Mock()
        mock_event = {"attendees": [{"email": "abcd0001@student.monash.edu", "comment": ""}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.request_change_time_venue(mock_api, "test id", "Request changing event location to Sunway Pyramid", "abcd0001@student.monash.edu")

        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['body']['attendees'], [{"email": "abcd0001@student.monash.edu", "comment": "Request changing event location to Sunway Pyramid"}])
