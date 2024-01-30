import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class DeleteFunctionTest(unittest.TestCase):
    @patch('MyEventManager.date')
    def test_success_delete_event_past_date(self, mock_date):
        """ 
        This test tests delete function on event on past date 
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 21)
        mock_event = {
            'end': {"date": '2022-09-19'}} 
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.delete_event(mock_api, "test_id")                                         # Called the delete_event method with a random event id that does exists
        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 1) # Check whether the delete method is called (i.e. called -> successfully deleted)

    @patch('MyEventManager.date')
    def test_fail_delete_event_present_date(self, mock_date):
        """ 
        This test tests delete function on event on present date 
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 21)
        mock_event = {
            'end': {"dateTime": '2022-09-21'}} 
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        with self.assertRaises(Exception):
            MyEventManager.delete_event(mock_api, "test_id")

        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 0)

    @patch('MyEventManager.date')
    def test_fail_delete_event_future_date(self, mock_date):
        """ 
        This test tests delete function on event on future date
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 21)
        mock_event = {
            'end': {"date": '2022-10-22'}}     
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        with self.assertRaises(Exception):
            MyEventManager.delete_event(mock_api, "test_id")

        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 0)