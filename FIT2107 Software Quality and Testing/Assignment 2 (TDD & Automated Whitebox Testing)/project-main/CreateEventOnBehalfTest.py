import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import date 

class CreateEventOnBehalfTest(unittest.TestCase):
    @patch('MyEventManager.date')
    def test_success_create_event_on_behalf(self, mock_date):
        """
        This test tests whether the user can create the event on behalf of the other user 
        """
        mock_api = Mock()

        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        expected_output = {
        'eventType': 'physical event', 
        'summary': 'Testing', 
        'location': '123 Fake Street, Clayton VIC 3400',
        'attendees': [],              
        'start': {'date': '2022-10-30'},
        'end': {'date': '2022-10-30'},
        'guestsCanInviteOthers': False,
        'organizer': {'email': 'stai0007@student.monash.edu'}, 
        'creator': {'email': 'stai0007@student.monash.edu'}                          
        }

        MyEventManager.create_event(
            mock_api, 'physical event', 'Testing', '123 Fake Street, Clayton VIC 3400', [], '2022-10-30', '2022-10-30', "stai0007@student.monash.edu")

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 1)
        args, kwargs = mock_api.events.return_value.insert.call_args_list[0]
        self.assertEqual(kwargs['body'], expected_output)