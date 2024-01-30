import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date

class AttendeesResponeTest(unittest.TestCase):
    def test_accept_invitation(self):
        """
        This test tests whether the attendee can accept the event invitation or not
        """
        mock_api = Mock()
        mock_event = {"attendees": [{"email": "abcd0001@student.monash.edu", "responseStatus": "needsAction"}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.attendees_response(mock_api, "test_id", "accepted", "abcd0001@student.monash.edu")
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)                # Check whether we call the update method once
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['body']['attendees'], [{"email": "abcd0001@student.monash.edu", "responseStatus": "accepted"}])   # Check whether the updated response status is pass into the argument

    def test_declined_invitation(self):
        """
        This test tests whether the attendee can decline the event invitation or not
        """
        mock_api = Mock()
        mock_event = {"attendees": [{"email": "abcd0001@student.monash.edu", "responseStatus": "needsAction"}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.attendees_response(mock_api, "test_id", "declined", "abcd0001@student.monash.edu")
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)                # Check whether we call the update method once
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['body']['attendees'], [{"email": "abcd0001@student.monash.edu", "responseStatus": "declined"}])   # Check whether the updated response status is pass into the argument

    def test_invalid_respone_status(self):
        """
        This test tests whether the attendee can respone other status other than accepted and declined to the event invitation
        """
        mock_api = Mock()
        mock_event = {"attendees": [{"email": "abcd0001@student.monash.edu", "responseStatus": "needsAction"}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        with self.assertRaises(Exception):
            MyEventManager.attendees_response(mock_api, "test_id", "Not sure", "abcd0001@student.monash.edu")
        
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 0) 

