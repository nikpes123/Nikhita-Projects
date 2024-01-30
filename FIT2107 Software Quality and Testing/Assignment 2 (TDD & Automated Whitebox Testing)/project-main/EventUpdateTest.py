import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class EventUpdateTest(unittest.TestCase):
    def test_valid_event_attribute_update(self):
        """
        This test tests if we can update the start date of an event successfully
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'start':{'date':"2022-08-12"}, 'end':{'date':"2023-09-1"}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.update_event(mock_api, mock_id, 'start', "2022-12-12")
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value['start']['date'], "2022-12-12")

    def test_invalid_event_attribute_update(self):
        """
        This test tests if we can update an invalid end date of an event
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'start':{'date':"2022-08-12"}, 'end':{'date':"2023-09-1"}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.update_event(mock_api, mock_id, 'end', "2021-12-12")

# -----------------------------------------------------------------------------------------------
# using WHITE BOX TESING(Branch Coverage)    
    def test_valid_event_attribute_update_WB1(self):
        """
        This test tests if we can update the summary of the event successfully
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'summary':"Football Tournment"}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.update_event(mock_api, mock_id, 'summary', "Futsal Match")
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value['summary'], "Futsal Match")

    def test_valid_event_attribute_update_WB2(self):
        """
        This test tests if we can update the location of an event
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'eventType': "physical meeting", 'location':"98 Shirley Street PIMPAMA QLD 4209 AUSTRALIA"}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.update_event(mock_api, mock_id, 'location', "11 Banks Av WAGGA WAGGA NSW 2650 AUSTRALIA")

    def test_valid_event_attribute_update_WB3(self):
        """
        This test tests if we can update invalid start date in the event
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'start':{'date':"2022-08-12"}, 'end':{'date':"2023-09-1"}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.update_event(mock_api, mock_id, 'start', "2051-12-12")


    def test_valid_event_attribute_update_WB4(self):
        """
        This test tests if we can update valid end date in the event
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'start':{'date':"2022-08-12"}, 'end':{'date':"2023-09-1"}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.update_event(mock_api, mock_id, 'end', "2022-12-12")
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value['end']['date'], "2022-12-12")

    def test_valid_event_attribute_update_WB5(self):
        """
        This test tests if we can update an invalid attribute in the event
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'start':{'date':"2022-08-12"}, 'end':{'date':"2023-09-1"}}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.update_event(mock_api, mock_id, 'summay', "2051-12-12")

    def test_valid_event_attribute_update_WB6(self):
        """
        This test tests if we can update the event type of an event successfully
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event = {'eventType':'official meeting' }
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        MyEventManager.update_event(mock_api, mock_id, 'eventType', 'online meeting')
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value['eventType'], 'online meeting')


    def test_valid_event_attribute_update_WB7(self):
        """
        This test tests if we can update an attendees email in the event
        """
        mock_api = Mock()
        mock_id = "31361552"
        mock_event =  {"attendees": [{"email": "abcd0001@student.monash.edu", "responseStatus": "needsAction"}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event
        with self.assertRaises(Exception):
            MyEventManager.update_event(mock_api, mock_id, "attendees", 'npes0002@student.monash.edu')
