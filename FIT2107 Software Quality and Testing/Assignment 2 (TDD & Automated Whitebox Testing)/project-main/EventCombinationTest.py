import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
# Add other imports here if needed

class EventCombinationTest(unittest.TestCase): 
    @patch('MyEventManager.date')
    def test_valid_combination_create_event_1(self, mock_date):
        """
        This test tests whether an event can be created with a valid combination of event's property 
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
        'guestsCanInviteOthers': False                          
        }

        MyEventManager.create_event(
            mock_api, 'physical event', 'Testing', '123 Fake Street, Clayton VIC 3400', [], '2022-10-30', '2022-10-30')

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 1)
        args, kwargs = mock_api.events.return_value.insert.call_args_list[0]
        self.assertEqual(kwargs['body'], expected_output)
    

    @patch('MyEventManager.date')
    def test_invalid_combination_create_event_2(self, mock_date):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: official meeting
        2. Event name: "" (invalid)
        3. Event location: Invalid address 
        4. Attendees: 20
        5. Date: Invalid date
        """ 
        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'}]

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'official meeting', '', 
                'Lot 1777, Orchard Road Ave., Singapore', attendees, '2022-08-30', '2022-08-30')

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)

    def test_invalid_combination_create_event_3(self):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "official meeting"
        2. Event name: "Testing"
        3. Event location: "online"
        4. Attendees: 21
        5. Date: Invalid date
        """ 

        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'},
                     {'email': 'abcd0021@student.monash.edu'}]
        
        mock_api = Mock()

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'official meeting', 'Testing', 
                'online', attendees, '2022-AUG-30', '2022-AUG-30')   

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0) 

    @patch('MyEventManager.date')
    def test_invalid_combination_create_event_4(self, mock_date):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "online meeting"
        2. Event name: " "
        3. Event location: "online"
        4. Attendees: 0
        5. Date: valid date
        """     

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'official meeting', ' ', 
                'online', [], '2022-10-30', '2022-10-30') 

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)

    def test_invalid_combination_create_event_5(self):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "online meeting"
        2. Event name: "Testing"
        3. Event location: valid address (invalid - because online meeting)
        4. Attendees: 0
        5. Date: invalid date
        """     

        mock_api = Mock()

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'online meeting', 'Testing', 
                '123 Fake St. Clayton VIC 3400', [], '22-AUG-30', '22-AUG-30')    
                
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)
          

    @patch('MyEventManager.date')
    def test_invalid_combination_create_event_6(self, mock_date):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "online meeting"
        2. Event name: " "
        3. Event location: valid address (invalid - because online meeting)
        4. Attendees: 20
        5. Date: valid date
        """     

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'online meeting', ' ', 
                '123 Fake St. Clayton VIC 3400', [], '2050-10-30', '2050-10-30')         

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)


    def test_invalid_combination_create_event_7(self):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "online meeting"
        2. Event name: "Testing"
        3. Event location: invalid address
        4. Attendees: 21
        5. Date: invalid date
        """    

        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'},
                     {'email': 'abcd0021@student.monash.edu'}]

        mock_api = Mock()

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'online meeting', 'Testing', 
                'Lot 1777, Orchard Road Ave., Singapore', attendees, '22-08-30', '22-08-30')    

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)


    @patch('MyEventManager.date')
    def test_invalid_combination_create_event_8(self, mock_date):
        # """
        # This test tests different combination of event argument which contains the invalid arguments
        # Input arguments for event:
        # 1. Type of event: "physical event"
        # 2. Event name: "Testing"
        # 3. Event location: valid address
        # 4. Attendees: 21
        # 5. Date: valid date
        # """       

        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'},
                     {'email': 'abcd0021@student.monash.edu'}]

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'physical event', 'Testing', 
                '123 Fake St. Clayton VIC 3400', attendees, '2050-10-30', '2050-10-30')

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)

    def test_invalid_combination_create_event_9(self):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "physical event"
        2. Event name: ""
        3. Event location: invalid address
        4. Attendees: 0
        5. Date: invalid date
        """   

        mock_api = Mock()

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'physical event', '', 
                'Lot 1777, Orchard Road Ave., Singapore', [], '22-08-30', '22-08-30')          

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)


    @patch('MyEventManager.date')
    def test_invalid_combination_create_event_10(self, mock_date):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "physical event"
        2. Event name: "Testing"
        3. Event location: "online"
        4. Attendees: 20
        5. Date: valid date
        """

        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'}]

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'physical event', 'Testing', 
                'online', attendees, '2050-10-30', '2050-10-30')

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)

    @patch('MyEventManager.date')
    def test_valid_combination_create_event_11(self, mock_date):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "official meeting"
        2. Event name: "Testing"
        3. Event location: "online"
        4. Attendees: 20
        5. Date: valid date
        """  

        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'}]

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today
        expected_output = {
            'eventType': 'official meeting', 
            'summary': 'Testing', 
            'location': 'online',
            'attendees': attendees,              
            'start': {'date': '2050-10-30'},
            'end': {'date': '2050-10-30'},
            'guestsCanInviteOthers': False                          
        }

        MyEventManager.create_event(
            mock_api, 'official meeting', 'Testing', 
            'online', attendees, '2050-10-30', '2050-10-30')

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 1)
        args, kwargs = mock_api.events.return_value.insert.call_args_list[0]
        self.assertEqual(kwargs['body'], expected_output)

    def test_invalid_combination_create_event_12(self):
        """
        This test tests different combination of event argument which contains the invalid arguments
        Input arguments for event:
        1. Type of event: "official meeting"
        2. Event name: "Testing"
        3. Event location: valid address
        4. Attendees: 21
        5. Date: invalid date
        """      

        attendees = [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}, {'email': 'abcd0003@student.monash.edu'}, {'email': 'abcd0005@student.monash.edu'}, 
                     {'email': 'abcd0005@student.monash.edu'}, {'email': 'abcd0006@student.monash.edu'}, {'email': 'abcd0007@student.monash.edu'}, {'email': 'abcd0008@student.monash.edu'}, 
                     {'email': 'abcd0009@student.monash.edu'}, {'email': 'abcd0010@student.monash.edu'}, {'email': 'abcd0011@student.monash.edu'}, {'email': 'abcd0012@student.monash.edu'}, 
                     {'email': 'abcd0013@student.monash.edu'}, {'email': 'abcd0014@student.monash.edu'}, {'email': 'abcd0015@student.monash.edu'}, {'email': 'abcd0016@student.monash.edu'}, 
                     {'email': 'abcd0017@student.monash.edu'}, {'email': 'abcd0018@student.monash.edu'}, {'email': 'abcd0019@student.monash.edu'}, {'email': 'abcd0020@student.monash.edu'},
                     {'email': 'abcd0021@student.monash.edu'}]

        mock_api = Mock()

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'official meeting', 'Testing', 
                '98 Shirley Street PIMPAMA QLD 4209', attendees, '22-08-30', '22-08-30')
     
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)

    @patch('MyEventManager.date')
    def test_invalid_combination_create_event_13(self, mock_date):
        # """
        # This test tests different combination of event argument which contains the invalid arguments
        # Input arguments for event:
        # 1. Type of event: "official meeting"
        # 2. Event name: ""
        # 3. Event location: valid address
        # 4. Attendees: 0
        # 5. Date: valid date
        # """    

        mock_api = Mock()
        mock_today = date(2022, 9, 21)
        mock_date.today.return_value = mock_today

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'official meeting', '', 
                '123 Fake St. Clayton VIC 3400', [], '2050-10-30', '2050-10-30')

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)

    def test_invalid_combination_create_event_14(self):
        # """
        # This test tests different combination of event argument which contains the invalid arguments
        # Input arguments for event:
        # 1. Type of event: "official meeting"
        # 2. Event name: "Testing"
        # 3. Event location: invalid address
        # 4. Attendees: 0
        # 5. Date: invalid date
        # """      

        mock_api = Mock()

        with self.assertRaises(Exception):
            MyEventManager.create_event(
                mock_api, 'official meeting', 'Testing', 
                '123456 Monash College', [], '22-08-30', '22-08-30')    

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)
