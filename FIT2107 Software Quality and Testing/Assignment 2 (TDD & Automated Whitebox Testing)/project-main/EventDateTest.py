import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class EventDateTest(unittest.TestCase): 
    @patch('MyEventManager.date')
    def test_valid_present_date_format(self, mock_date):
        """
        This test tests the function that in charge of validating the event date's range and format
        Present date (loewr bound on-point) & correct format
        """
        mock_date.today.return_value = date(2022, 9, 23)
        self.assertEqual(MyEventManager.date_format_range_checker('2022-09-23'), '2022-09-23')

    @patch('MyEventManager.date')
    def test_valid_future_date_format(self, mock_date):
        """
        This test tests the function that in charge of validating the event date's range and format
        Future date (upper bound on-point) & correct format (dd-MON-yy)
        """
        mock_date.today.return_value = date(2022, 9, 23)
        self.assertEqual(MyEventManager.date_format_range_checker('23-DEC-50'), '2050-12-23')

    @patch('MyEventManager.date')
    def test_invalid_date_format(self, mock_date):
        """
        This test tests the function that in charge of validating the event date's range and format
        Incorrect date format (dd-MON-yyyy)
        """
        mock_date.today.return_value = date(2022, 9, 23)
        with self.assertRaises(Exception):
            MyEventManager.date_format_range_checker('23-JUN-2023')

    @patch('MyEventManager.date')
    def test_invalid_future_date_range(self,mock_date):
        """
        This test tests the function that's in charge of validating the event date's range
        Incorrect future date range (upper bound off-point)
        """
        mock_date.today.return_value = date(2022, 9, 23)
        with self.assertRaises(Exception):
            MyEventManager.date_format_range_checker('2051-01-01')

    @patch('MyEventManager.date')
    def test_invalid_past_date_range(self,mock_date):
        """
        This test tests the function that's in charge of validating the event date's range
        Incorrect past date range (Lower bound off-point)
        """
        mock_date.today.return_value = date(2022, 1, 1)
        with self.assertRaises(Exception):
            MyEventManager.date_format_range_checker('2021-12-31')
        