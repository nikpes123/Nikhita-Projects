import unittest
from unittest.mock import Mock, patch
import MyEventManager
from datetime import date

class NavigationTest(unittest.TestCase):
    @patch('MyEventManager.date')
    def test_success_navigate_day_upper_bound(self, mock_date):
        """
        This test tests whether navigation on day can be done and can the event at the upper bound (on point)
        of the date range of event viewing (5 yrs in the future) be retrieved
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)                              # Allow the date class to run as normal when instantiate a date object
        mock_navigator = "Day"
        mock_selected_date = date(2027,9,25) 
        mock_events = [{'start': {'date': '2027-09-25'}}]
        mock_api.events.return_value.list.return_value.execute.return_value = mock_events
        retrieved_events = MyEventManager.navigation(mock_api, mock_navigator ,mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2027-09-25T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in
        self.assertEqual(kwargs['timeMax'], "2027-09-25T23:59:59+08:00")                            # Check whether the correct lower bound date range is passed in
        self.assertEqual(retrieved_events, mock_events)                                             # To check whether the event at that date can be retrieved
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)      # To check whether the method that retrieve the events is called


    @patch('MyEventManager.date')
    def test_success_navigate_day_lower_bound(self, mock_date):
        """
        This test tests whether navigation on day can be done and can the event at the lower bound (on point)
        of the date range of event viewing (5 yrs in the past) be retrieved
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        mock_navigator = "Day"
        mock_selected_date = date(2017,9,25) 
        mock_events = [{'start': {'date': '2017-09-25'}}]
        mock_api.events.return_value.list.return_value.execute.return_value = mock_events
        retrieved_events = MyEventManager.navigation(mock_api, mock_navigator ,mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2017-09-25T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in
        self.assertEqual(kwargs['timeMax'], "2017-09-25T23:59:59+08:00")                            # Check whether the correct lower bound date range is passed in
        self.assertEqual(retrieved_events, mock_events)                                             # To check whether the event at that date can be retrieved
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)      # To check whether the method that retrieve the events is called


    @patch('MyEventManager.date')
    def test_fail_navigate_day_exceed_upper_bound(self, mock_date):
        """
        This test tests whether the event that exceed the the upper bound (off point)
        of the date range of event viewing (5 yrs in the past) be retrieved through navigation
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)       
        mock_navigator = "Day"
        mock_selected_date = date(2027,9,26) 
        retrieved_events = MyEventManager.navigation(mock_api, mock_navigator ,mock_selected_date)

        self.assertEqual(retrieved_events, None)                                                    # To check whether the event at that date cannot be retrieved
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 0)      # To check whether the method that retrieve the events is called


    @patch('MyEventManager.date')
    def test_fail_navigate_day_subceed_lower_bound(self, mock_date):
        """
        This test tests whether the event that exceed the the upper bound (off point)
        of the date range of event viewing (5 yrs in the past) be retrieved through navigation
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)       
        mock_navigator = "Day"
        mock_selected_date = date(2017,9,24) 
        retrieved_events = MyEventManager.navigation(mock_api, mock_navigator ,mock_selected_date)

        self.assertEqual(retrieved_events, None)                                                    # To verify whether the event at that date cannot be retrieved
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 0)      # To check whether the method that retrieve the events is called


    @patch('MyEventManager.date')
    def test_success_navigate_month_upper_bound(self, mock_date):
        """
        This test tests whether the navigation on month can be done correctly and the respective event in that month
        is retrieved if it in the upper bound valid date viewing range
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "MoNtH"
        mock_selected_date = date(2027,9,9)
        MyEventManager.navigation(mock_api, mock_navigator, mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2027-09-01T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in to retrieve the event 
        self.assertEqual(kwargs['timeMax'], "2027-09-25T23:59:59+08:00")                            # Check whether the correct uppper bound date range is passed in to retrieve the event
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)


    @patch('MyEventManager.date')
    def test_success_navigate_month_lower_bound(self, mock_date):
        """
        This test tests whether the navigation on month can be done correctly and the respective event in that month
        is retrieved if it in the lower bound of valid date viewing range
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 10, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "Month"
        mock_selected_date = date(2017,10,9)
        MyEventManager.navigation(mock_api, mock_navigator, mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2017-10-25T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in to retrieve the event 
        self.assertEqual(kwargs['timeMax'], "2017-10-31T23:59:59+08:00")                            # Check whether the correct uppper bound date range is passed in to retrieve the event
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)


    @patch('MyEventManager.date')
    def test_fail_navigate_month_out_of_bound(self, mock_date):
        """
        This test tests whether the navigation on month can be done correctly and the respective event in that month
        is retrieved if out of the bound of valid date viewing range
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 3, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "Month"
        mock_selected_date = date(2017,2,9)
        retrieve_event = MyEventManager.navigation(mock_api, mock_navigator, mock_selected_date)

        self.assertEqual(retrieve_event, None)
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 0) # Tests fail to retrieve because out of 5 years range from now  
    

    @patch('MyEventManager.date')
    def test_success_navigate_year(self, mock_date):
        """
        This test tests whether the navigation on year can be done correctly and the respective event in that year
        is retrieved if it is in the valid date viewing range
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "YeaR"
        mock_selected_date = date(2022,9,9)
        MyEventManager.navigation(mock_api, mock_navigator, mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2022-01-01T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in to retrieve the event 
        self.assertEqual(kwargs['timeMax'], "2022-12-31T23:59:59+08:00")                            # Check whether the correct uppper bound date range is passed in to retrieve the event
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)


    @patch('MyEventManager.date')
    def test_fail_retrieve_event_navigate_year(self, mock_date):
        """
        This test tests whether the navigation on year can be done correctly and the respective event in that year
        is retrieved if it is out of the valid date viewing range
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 9, 25)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "Year"
        mock_selected_date = date(2016,9,9)
        retrieve_event = MyEventManager.navigation(mock_api, mock_navigator, mock_selected_date)

        self.assertEqual(retrieve_event, None)
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 0)


    @patch('MyEventManager.date')
    def test_success_navigate_forward(self, mock_date):
        """
        This function tests whether calender can be viewed upto 2050 using "forward arrow"
        to navigate and getting the event if in the valid event viewing date range after navigation
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "ForWARD"
        mock_selected_date = date(2022,12,9)
        MyEventManager.navigation(mock_api, mock_navigator,mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2023-01-01T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in to retrieve the event 
        self.assertEqual(kwargs['timeMax'], "2023-01-31T23:59:59+08:00") 
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)

    @patch('MyEventManager.date')
    def test_success_navigate_backward(self, mock_date):
        """
        This test tests whether calendar can navigate backward using backward arrow and view the events
        on the month after navigation if they are in the valid event date viewing range
        """
        mock_api = Mock()
        mock_date.today.return_value = date(2022, 12, 31)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw) 
        mock_navigator = "backward"
        mock_selected_date = date(2028,1,1)
        MyEventManager.navigation(mock_api, mock_navigator,mock_selected_date)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], "2027-12-01T00:00:00+08:00")                            # Check whether the correct lower bound date range is passed in to retrieve the event 
        self.assertEqual(kwargs['timeMax'], "2027-12-31T23:59:59+08:00") 
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 1)

    def test_fail_invalid_navigator(self):
        """
        This test tests whether navaigation can be done when the invalid instruction is inputted
        """
        mock_api = Mock()
        mock_navigator = "fghbhbyhhn"
        mock_selected_date = date(2021,1,8)
        MyEventManager.navigation(mock_api, mock_navigator,mock_selected_date)
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.call_count, 0)
    
    def test_pass_search_list_dictionary(self):
        """
        This test tests whether the search function can search through dictionary inside a list (search the internal content)
        """
        mock_api = Mock()
        mock_events = [{"organizer": {'email': "nikhita@student.monash.edu"}},
                        {"organizer": {'email': "TAnPaa123@student.monash.edu"}}]
        mock_navigator = "search"
        mock_search_type = "organizer"
        mock_keyword = "nikhita"
        mock_api.events.return_value.list.return_value.execute.return_value = mock_events
        x = MyEventManager.navigation(api = mock_api, navigator = mock_navigator, searchType = mock_search_type, keyword=mock_keyword)
        self.assertEqual(x, [{"organizer": {'email': "nikhita@student.monash.edu"}}])


    def test_pass_search_other_data_structure(self):
        """
        This test tests whether the search function can search through other data structure such as list and dictionary 
        """
        mock_api = Mock()
        mock_events = [{"summary": "ABC"}, {"summary": "KJB"}]
        mock_navigator = "search"
        mock_search_type = "summary"
        mock_keyword = "KJB"
        mock_api.events.return_value.list.return_value.execute.return_value = mock_events
        x = MyEventManager.navigation(api = mock_api, navigator = mock_navigator, searchType = mock_search_type, keyword=mock_keyword)
        self.assertEqual(x, [{"summary": "KJB"}])


    def test_pass_search_attendees(self):
        """
        This test tests whether the search function can be used to search through the attendees
        """
        mock_api = Mock()
        mock_events =   [{"attendees": [{"id": "31361552","email": "npes0001@student.monash.edu"}]},
                        {"attendees": [{"id": "31361552","email": "mhae0001@student.monash.edu"}]}]

        mock_navigator = "search"
        mock_search_type = "attendees"
        mock_keyword = "313"
        mock_api.events.return_value.list.return_value.execute.return_value = mock_events
        x = MyEventManager.navigation(api = mock_api, navigator = mock_navigator, searchType = mock_search_type, keyword=mock_keyword)
        self.assertEqual(x, mock_events)
