import unittest
from unittest.mock import Mock
import MyEventManager

class SetRemindersTest(unittest.TestCase):
    def test_success_set_reminder(self):
        """
        This function tests if a reminder is set successfully
        """
        mock_api = Mock()
        mock_minutes = 1
        mock_event = {"reminders": {}} 
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.set_reminder(mock_api,"Test ID", mock_minutes)
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)
    
    def test_fail_set_reminder(self):
        """
        This function tests if a reminder is set unsuccessfully
        """
        mock_api = Mock()
        mock_minutes = 40325
        with self.assertRaises(Exception):
            MyEventManager.set_reminder(mock_api,"Test ID", mock_minutes)
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 0)

