import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from datetime import datetime
from datetime import date
import EventCombinationTest
import AddressFormatTest
import EventDateTest
import RestoreFunctionTest
import CancelFunctionTest
import DeleteFunctionTest
import ImportExportJsonTest
import ManageAttendeesTest
import AttendeesResponeTest
import NotificationTest
import RequestChangeTest
import ChangeEventOwnerTest
import CreateEventOnBehalfTest
import EventUpdateTest
import NavigationTest
import SetRemindersTest

# Add other imports here if needed

class MyEventManagerTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

def main():
    # Compile all the test suites into a list
    suiteList = []
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(EventCombinationTest.EventCombinationTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(AddressFormatTest.AddressFormatTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(EventDateTest.EventDateTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(RestoreFunctionTest.RestoreFunctionTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(CancelFunctionTest.CancelFunctionTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(DeleteFunctionTest.DeleteFunctionTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(ImportExportJsonTest.ImportExportJsonTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(ManageAttendeesTest.ManageAttendeesTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(AttendeesResponeTest.AttendeesResponeTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(NotificationTest.NotificationTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(RequestChangeTest.RequestChangeTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(ChangeEventOwnerTest.ChangeEventOwnerTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(CreateEventOnBehalfTest.CreateEventOnBehalfTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(EventUpdateTest.EventUpdateTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(SetRemindersTest.SetRemindersTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(NavigationTest.NavigationTest))



    # combine all the test suites
    comboSuite = unittest.TestSuite(suiteList)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(comboSuite)

main()