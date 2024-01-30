import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date

class NotificationTest(unittest.TestCase):
    @patch('MyEventManager.date')
    def test_notification_success_create_event(self, mock_date):
        """
        This test tests whether the notification is sent to the attendees when event is created
        """
        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today
        MyEventManager.create_event(
            mock_api, 'physical event', 'Testing', '123 Fake Street, Clayton VIC 3400', [], '2022-10-30', '2022-10-30', 'stai0007@student.monash.edu')

        args, kwargs = mock_api.events.return_value.insert.call_args_list[0]
        self.assertEqual(kwargs['sendUpdates'], 'all')

    @patch('MyEventManager.date')
    def test_notification_success_cancel_event(self, mock_date):
        """
        This test tests whether the notification is sent to the attendees when event is cancel
        """
        mock_api = Mock()
        mock_today_datetime = date(2022, 9, 20)
        mock_date.today.return_value = mock_today_datetime
        mock_event = {
            'end': {"date": '2022-09-20'}} # An all-day event on today 
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.cancel_event(mock_api, "test_id")
        args, kwargs = mock_api.events.return_value.delete.call_args_list[0]
        self.assertEqual(kwargs['sendUpdates'], 'all')

    def test_notification_success_update_attendee(self):
        """
        This test tests whether the notification is sent to the attendees when attendees are updated (technically part of event is updated)
        """
        mock_api = Mock()
        mock_event = {"attendees": [{'email': 'abcd0001@student.monash.edu'}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.manage_attendees(mock_api, 'test_id', {'email': 'abcd0002@student.monash.edu'}, "add", True)
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['sendUpdates'], 'all')


    def test_notification_success_attendee_response(self):
        """
        This test tests whether the notification is sent to the attendees when they respond to the event invitation
        """
        mock_api = Mock()
        mock_event = {"attendees": [{"email": "abcd0001@student.monash.edu", "responseStatus": "needsAction"}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.attendees_response(mock_api, "test_id", "accepted", "abcd0001@student.monash.edu")
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['sendUpdates'], 'all')

    def test_notification_success_update_event(self):
        """
        This test tests whether the notification is sent to the attendees when the event is updated
        """
        mock_api = Mock()
        mock_event = {'eventType': 'official meeting'}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.update_event(mock_api, "test id", 'eventType', 'physical event')
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['sendUpdates'], 'all')

