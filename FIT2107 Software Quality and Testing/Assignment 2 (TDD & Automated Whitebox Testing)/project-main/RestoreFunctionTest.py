import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class RestoreFunctionTest(unittest.TestCase):  
    @patch('MyEventManager.date')
    @patch("MyEventManager.cancelled_events", ["test_id"])  # Mocking the global variable in the module
    def test_success_restore_cancelled_event(self, mock_date):
        """ 
        This test tests restore function on cancelled event that have not ended (present or future event)
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 22)
        mock_event = {
            'status': 'cancelled',
            'end': {"date": '2022-10-30'}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.restore_event(mock_api, "test_id")
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)

    @patch("MyEventManager.cancelled_events", [])
    def test_fail_restore_uncancelled_event(self):
        """ 
        This test tests restore function on uncancelled event
        """
        mock_api = Mock()
        mock_event = {
            'status': 'confirmed'}
        
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.restore_event(mock_api, "test_id")

        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 0)

    @patch('MyEventManager.date')
    @patch("MyEventManager.cancelled_events", ["test_id"])
    def test_fail_restore_cancelled_past_event(self, mock_datetime):
        """ 
        This test tests restore function on cancalled event that is already a past event when the user try to restore
        """
        mock_api = Mock()
        mock_datetime.today.return_value = date(2022, 9, 21)
        mock_event = {
            'status': 'cancelled',
            'end': {"date": '2022-08-30'}}
        
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.restore_event(mock_api, "test_id")

        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 0)
