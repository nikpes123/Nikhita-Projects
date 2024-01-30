from multiprocessing.sharedctypes import Value
import unittest
from unittest.mock import MagicMock, Mock, patch, mock_open
import MyEventManager

class ManageAttendeesTest(unittest.TestCase):
    
    def test_add_attendee(self):
        """
        This test tests whether event owner can add attendees to the event
        """
        mock_api = Mock()
        mock_event = {"attendees": [{'email': 'abcd0001@student.monash.edu'}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.manage_attendees(mock_api, 'test_id', {'email': 'abcd0002@student.monash.edu'}, "add", True)
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)                # Check whether we call the update method once
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(len(kwargs['body']['attendees']), 2)                                                   # Check whether the updated attendees (added 1) is passing to the method
    

    def test_remove_attendee(self):
        """
        This test tests whether event owner can remove attendee from the event
        """
        mock_api = Mock()
        mock_event = {"attendees": [{'email': 'abcd0001@student.monash.edu'}, {'email': 'abcd0002@student.monash.edu'}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.manage_attendees(mock_api, 'test_id', {'email': 'abcd0002@student.monash.edu'}, "remove", True)
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)                # Check whether we call the update method once
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(len(kwargs['body']['attendees']), 1)                                                   # Check whether the updated attendees (removed 1) is passing to the method
    

    def test_update_attendee(self):
        """
        This test tests whether the event owner can update the info of the attendee
        """
        mock_api = Mock()
        mock_event = {"attendees": [{'email': 'abcd0001@student.monash.edu', 'displayName': 'Michelle'}, {'email': 'abcd0002@student.monash.edu', 'displayName': 'Mike'}]}
        mock_api.events.return_value.get.return_value.execute.return_value = mock_event

        MyEventManager.manage_attendees(mock_api, 'test_id', {'email': 'abcd0002@student.monash.edu', 'displayName': 'Sherry'}, "update", True)
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)                # Check whether we call the update method once
        args, kwargs = mock_api.events.return_value.update.call_args_list[0]
        self.assertEqual(kwargs['body']['attendees'], [{'email': 'abcd0001@student.monash.edu', 'displayName': 'Michelle'}, {'email': 'abcd0002@student.monash.edu', 'displayName': 'Sherry'}])  # Check whether the updated attendees (removed 1) is passing to the method

    def test_invalid_function_attendee(self):
        """
        This test tests whether invalid function can be performed on attendees
        """
        mock_api = Mock()
        with self.assertRaises(Exception):
            MyEventManager.manage_attendees(mock_api, 'test_id', [{'email': 'abcd0001@student.monash.edu', 'displayName': 'Sherry'}], "somefunction", True)

        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 0)            # Changes is not done

    def test_not_owner_manage_attendee(self):
        """
        This test tests whether non event owner can manage the attendees or not
        """
        mock_api = Mock()
        with self.assertRaises(Exception):
            MyEventManager.manage_attendees(mock_api, 'test_id', {'email': 'abcd0001@student.monash.edu', 'displayName': 'Sherry'}, "add", False)

        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 0)            # Changes is not done