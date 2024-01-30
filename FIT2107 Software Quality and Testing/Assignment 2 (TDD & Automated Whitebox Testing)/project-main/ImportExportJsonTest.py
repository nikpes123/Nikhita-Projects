from multiprocessing.sharedctypes import Value
import unittest
from unittest.mock import MagicMock, Mock, patch, mock_open
import MyEventManager
import json

class ImportExportJsonTest(unittest.TestCase):
    @patch('MyEventManager.json')
    def test_import_valid_json_file(self, mock_json):
        """
        Test whether we can import the event in valid JSON format, parse them and insert them into the calendar
        """
        mock_api = Mock()
        mock_events = {"items": [{"summary": "Google I/O 2015", "location": "800 Howard St., San Francisco, CA 94103", "start": {"dateTime": "2015-05-28T09:00:00-07:00"}, "end": {"dateTime": "2015-05-31T09:00:00-07:00"}}, 
                       {"summary": "Google I/O 2020", "location": "800 Howard St., San Francisco, CA 94103", "start": {"dateTime": "2015-05-28T09:00:00-07:00"}, "end": {"dateTime": "2015-05-31T09:00:00-07:00"}}]}

        mock_json.load.return_value = mock_events
        with patch("MyEventManager.open", mock_open()) as _open:
            MyEventManager.import_JSON(mock_api, "testing.txt")
            self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 2)        # Insert function called twice (2 events imported)


    @patch('MyEventManager.json')
    def test_import_invalid_json_file(self, mock_json):
        """
        Test whether Exception will be raised if we import the event in invalid JSON format
        """
        mock_api = Mock()
        mock_json.load.side_effect = Exception                      # Exception is raised (to represent error while parsing the JSON format)

        with patch("MyEventManager.open", mock_open()) as _open:
            with self.assertRaises(Exception):
                MyEventManager.import_JSON(mock_api, "testing.txt")

        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.call_count, 0)


    def test_export_events_json_file(self):
        """
        This test tests whether exporting events to JSON format file can be done
        """
        mock_api = Mock()
        mock_events = [{"summary": "Google I/O 2015", "location": "800 Howard St., San Francisco, CA 94103", "start": {"dateTime": "2015-05-28T09:00:00-07:00"}, "end": {"dateTime": "2015-05-31T09:00:00-07:00"}}, 
                       {"summary": "Google I/O 2020", "location": "800 Howard St., San Francisco, CA 94103", "start": {"dateTime": "2015-05-28T09:00:00-07:00"}, "end": {"dateTime": "2015-05-31T09:00:00-07:00"}}]

        mock_api.events.return_value.list.return_value.execute.return_value = mock_events

        with patch("MyEventManager.json"), patch("MyEventManager.open", mock_open()) as _open:  # Mock the open() method and json
            MyEventManager.export_JSON(mock_api, 'testing.json')
            MyEventManager.json.dump.assert_called_with(mock_events, _open())


