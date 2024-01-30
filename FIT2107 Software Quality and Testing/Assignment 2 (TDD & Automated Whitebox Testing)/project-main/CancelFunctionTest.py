import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class CancelFunctionTest(unittest.TestCase):    
    @patch('MyEventManager.date')
    def test_success_cancel_present_event(self, mock_date):
        """ 
        This test tests cancel function on present event
        """
        mock_api = Mock()
        mock_today_datetime = date(2022, 9, 20)
        mock_date.today.return_value = mock_today_datetime
        mock_event = {
            'end': {"date": '2022-09-20'}} # An all-day event on today 
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.cancel_event(mock_api, "test_id")
        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 1)

    @patch('MyEventManager.date')
    def test_success_cancel_future_event(self, mock_date):
        """ 
        This test tests delete function on future event
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 21)
        mock_event = {
            'end': {"date": '2022-10-30'}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.cancel_event(mock_api, "test_id")
        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 1)

    @patch('MyEventManager.date')
    def test_fail_cancel_past_event(self, mock_date):
        """ 
        This test tests delete function on past event
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 22)
        mock_event = {
            'end': {"date": '2022-08-30'}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        with self.assertRaises(Exception):  
            MyEventManager.cancel_event(mock_api, "test_id")

        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 0)
