import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class AddressFormatTest(unittest.TestCase): 
    def test_valid_Aus_US_full_address(self):
        """
        This test tests whether the valid Australia/American format full address can be accepted
        """
        event_address = '123 Fake Street Clayton VIC 3400'
        self.assertEqual(MyEventManager.validate_address(event_address), event_address)

    def test_valid_Aus_US_abbreviation_address(self):
        """
        This test tests whether the valid Australia/American format address with abbreviation street type can be accepted
        """
        event_address = '98 Shirley Street PIMPAMA QLD 4209'
        self.assertEqual(MyEventManager.validate_address(event_address), event_address)

    def test_invalid_address_format(self):
        """
        This test tests whether the invalid format address can be accepted
        """
        event_address = 'PT 6765, Tmn Sri Maju, Kg. Kubang Kerian, 47500, Bandar Sunway, Petalling Jaya, Selangor'
        with self.assertRaises(Exception):
            MyEventManager.validate_address(event_address)

    def test_empty_event_address(self):
        """
        This test tests whether the empty address can be accepted
        """
        event_address = ''
        with self.assertRaises(Exception):
            MyEventManager.validate_address(event_address)
