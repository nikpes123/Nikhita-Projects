# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
from calendar import calendar
from datetime import datetime
from datetime import date 
import pickle
import os.path
import usaddress
import json
from io import open
from time import timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

cancelled_events = []
EVENT_TYPES = ['official meeting', 'online meeting', 'physical event'] # Constant variable for event types (the only 3 types)
ADDRESS_COMPONENT = ['AddressNumber', 'StreetName', 'StreetNamePostType', 'PlaceName', 'StateName', 'ZipCode']

############################################################
#################### HELPER FUNCTION #######################
############################################################   
def event_type_checker(event_type:str):
    """
    Check whether the event is one of the event type we supported in this application
    """
    if event_type in EVENT_TYPES:
        return event_type
    else:
        raise Exception("Event type can only be 'official meeting', 'online meeting' or 'physical event'")

def event_name_checker(event_name:str):
    """
    Check whether event name contain actual character or not
    Any thing other than emtpy string and only spaces is accepted
    """
    if len(event_name) >= 1 and not event_name.isspace():
        return event_name
    else:
        raise Exception("Event name need to contain at least 1 character")

def attendees_checker(attendees:list):
    """
    Validate the number of attendees and their emails
    """
    if len(attendees) <= 20 and attendees_identity_checker(attendees):
        return attendees
    else:
        raise Exception("Number of attendees need to be in between 1 to 20")

def attendees_identity_checker(attendees:list):
    """
    Verify whether all the attendees are using monash student's email 
    """
    for attendee in attendees:
        if len(attendee['email']) == 27 and attendee['email'][9:] == "student.monash.edu": # assure it is a monash student email
            continue
        else:
            raise Exception("Attendees need to be Monash student")

    return True

def date_format_range_checker(event_date:str):
    """
    Check the format and the range of the event date inputted
    """
    format_correct = True
    try:
        convert_date =datetime.strptime(event_date, '%Y-%m-%d').date() # Accept yyyy-mm-dd format
    except ValueError:
        try:
            convert_date = datetime.strptime(event_date, '%d-%b-%y').date() # Accept dd-MON-yy format
        except ValueError:
            format_correct = False

    if format_correct:
        if convert_date >= date.today() and convert_date.year <= 2050:
            return datetime.strftime(convert_date, '%Y-%m-%d')                # Always store time in yyyy-mm-dd format
        else:
            raise Exception('Event cannot be created on past dates and later than 2050')
    else:
        raise Exception("Date format is incorrect")

def validate_event_location(event_type, event_location):
    """
    Validate whether the event location meets the respective event type, if it is support physical address, validate the address
    """
    if event_type == 'online meeting' and event_location == "online" or event_type == "official meeting" and event_location == "online":
        return event_location
    elif event_type == 'official meeting' or (event_type == 'physical event' and not event_location == "online"):
        return validate_address(event_location)
    else:
        raise Exception("This type of event does not match the correct event location")

def validate_address(event_location):
    """
    Validate whether the address format is correct
    """
    parse_address = usaddress.parse(event_location)
    temp = []
    for (v,k) in parse_address:
        temp.append((k, v))
    
    dict_address = dict(temp)
    if list(dict_address.keys()) == ADDRESS_COMPONENT:
        return event_location
    else:
        raise Exception("Invalid address format")

def convert_date_format(date_input, when):
    """
    The purpose of this helper function is to add time and zone to a date object
    """
    # we want (2011-06-03T10:00:00-07:00)
    #         (YYYY-MM-DDTHH:MM:SS+08:00)
    input_string = date_input.isoformat()
    if when =="start":
        input_string += "T00:00:00+08:00"
    else:
        input_string += "T23:59:59+08:00"
    # return datetime.strptime(input_string,"%Y-%m-%dT%H:%M:%S%z")
    return input_string

def checker(navigator, date_input):
    """
    The purpose of this helper function is to check whether we use do the backward
     and forward navigator and it calculates valid date
    """
    valid_date = None
    if navigator == "backward" and date_input.month == 1:
        valid_date = date(date_input.year-1,12,1)
    elif navigator == "forward" and date_input.month == 12:
        valid_date = date(date_input.year+1,1,1)
    else:
        valid_date = date(date_input.year, date_input.month-1,1)
    return valid_date

def calculate_month_end_date(month):
    """
    The purpose of this helper function is to find out the last valid date in a month
    """
    end_date = 0
    if month in [1,3,5,7,8,10,12]:
        end_date = 31
    elif month == 2:
        end_date = 28
    else:
        end_date = 30
    return end_date

def is_start_after_end_checker(start_date:str, end_date:str):
    if start_date <= end_date:
        return True
    else:
        return False

############################################################
############# CALENDAR FUNCTION IMPLEMENTATION #############
############################################################
def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def delete_event(api, event_id): 
    """ 
    Delete the event that matches the event_id passed in
    Only event on past dates can be deleted
    """   
    event = api.events().get(calendarId='primary', eventId=event_id).execute()

    # Retrieve today's date
    current_datetime = date.today()  
    event_end_datetime = event['end'].get('date')

    convert_end_date = datetime.strptime(event_end_datetime, '%Y-%m-%d').date() # since we are retrieving date and they are stored in yyyy-mm-dd format

    # The event has passed
    if convert_end_date < current_datetime: 
        api.events().delete(calendarId='primary', eventId=event_id).execute()
    else:
        raise Exception("Only event on past dates can be deleted")


def cancel_event(api, event_id):
    """ 
    Cancel the event that matches the event_id passed in
    Only present and future event can be cancelled
    Past event -> any event that ended before current date & time (It's illogical to cancel a past event)
    """   
    event = api.events().get(calendarId='primary', eventId=event_id).execute()

    current_datetime = date.today()  
    event_end_datetime = event['end'].get('date')

    convert_end_date = datetime.strptime(event_end_datetime, '%Y-%m-%d').date()

    if convert_end_date >= current_datetime:
        api.events().delete(calendarId='primary', eventId=event_id, sendUpdates="all").execute()
        cancelled_events.append(event_id)   # The record that keep the eventId of cancelled event for restore purpose in the future
    else:
        raise Exception("Only present and future event can be cancelled")


def restore_event(api, event_id):
    """ 
    Restore the cancelled event 
    Only present and future event can be restored (if the event has ended before restoration, it cannot be restored)
    """   
    event = api.events().get(calendarId='primary', eventId=event_id, timeZone="GMT+8:00").execute()

    if event_id in cancelled_events:                                                           # Checking whether the record has the cancelled event
        current_datetime = date.today()
        event_end_datetime = event['end'].get('date')

        convert_end_date = datetime.strptime(event_end_datetime, '%Y-%m-%d').date()

        if convert_end_date >= current_datetime:
            event['status'] = 'confirmed'
            api.events().update(calendarId='primary', eventId=event_id, sendUpdates='all', body=event).execute()
            cancelled_events.remove(event_id)                                                         # Remove the id of the event from the cancelled record
        else:
            raise Exception("Only cancelled present or future event can be restored")

    else:
        raise Exception("This event has not been cancelled")
        

def create_event(api, event_type:str, event_name:str, event_location:str, attendees:list, start_date:str, end_date:str, organizer_email:str = None):
    """
    Create event and validate all the input given and their combination before actually insert to the calendar
    If: organizer_email is not passed in, it means the user is creating it for himself, so the creator and organizer role will set by default in the API
    else: we will set both of that ourselves before creating the event
    """

    event = {
        'eventType': event_type_checker(event_type.lower()),    # Change the input event type to lower case
        'summary': event_name_checker(event_name),
        'location': validate_event_location(event_type, event_location),
        'attendees': attendees_checker(attendees),              # Check number of attendees and the identity of attendees (Monash student or not)
        'start': {'date': date_format_range_checker(start_date)},
        'end': {'date': date_format_range_checker(end_date)},
        'guestsCanInviteOthers': False                          # Set to false to ensure guests cannot add the other attendees
    }

    if organizer_email:
        event_organizer = {'organizer': {'email': organizer_email}, 'creator': {'email': organizer_email}}
        event = event | event_organizer

    if start_date > end_date:
        raise Exception("Start date need to be smaller or equal to end date")

    api.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()


def export_JSON(api, file_name):
    """
    Exporting all events in the calendar into JSON format into json file
    """
    all_events = api.events().list(calendarId='primary').execute()      # Getting all the events on the calendar
    with open(file_name, "w") as outfile:
        json.dump(all_events, outfile)                                  # Write the retrieved events to a file in JSON format


def import_JSON(api, input_file):
    """
    Importing events in JSON format and store all the events imported into the calendar
    This functionality supports importing multiple events
    """
    format = True
    f = open(input_file)
    try:
        events_data = json.load(f)
    except:
        format = False

    if format:
        for event in events_data['items']:
            api.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    else:
        raise Exception("Invalid JSON format")


def manage_attendees(api, event_id, up_attendee, action, isOrganizer):
    """
    This method allows event organizer to update the attendees of the event
    """
    event = api.events().get(calendarId='primary', eventId=event_id).execute()
    if isOrganizer:
        if action.lower() == "add":                                     # if user want to add attendee, append to the attendees of the event
            if len(event['attendees']) < 20:
                event['attendees'].append(up_attendee)
            else:
                raise Exception("Number of attendees reach maximum")

        elif action.lower() == "remove":
            for attendee in event['attendees']:
                if attendee['email'] == up_attendee['email']:           # If the email matches, then remove the attendee
                    event['attendees'].remove(attendee)
                    break
                else:
                    continue
                
        elif action.lower() == "update":
            for i in range(len(event['attendees'])):
                if event['attendees'][i]['email'] == up_attendee['email']:           # If the email matches, then update the attendee
                    event['attendees'][i] = up_attendee
                else:
                    continue
        else:
            raise Exception("Not such function to perform")

        api.events().update(calendarId='primary', eventId=event_id, body=event, sendUpdates='all').execute()

    else:
        raise Exception("Only event organizer can manage the attendees")


def attendees_response(api, event_id, respone, attendee_email):
    """
    This function allows the attendees to respond the event invitation
    """
    event = api.events().get(calendarId='primary', eventId=event_id).execute()

    for i in range(len(event['attendees'])):
        if event['attendees'][i]['email'] == attendee_email:           # If the email matches, then update the attendee
            if respone == "accepted":
                event['attendees'][i]["responseStatus"] = "accepted"
            elif respone == "declined":
                event['attendees'][i]["responseStatus"] = "declined"
            else:
                raise Exception("Only \"accepted\" and \"declined\" status are accepted")
            api.events().update(calendarId='primary', eventId=event_id, body=event, sendUpdates='all').execute()
            break
    return

def request_change_time_venue(api, event_id, request, attendee_email):
    """
    This function provides the feature for the attendees to request for change of time or venue of the event by leaving the response's comment
    """
    event = api.events().get(calendarId='primary', eventId=event_id).execute()

    for i in range(len(event['attendees'])):
        if event['attendees'][i]['email'] == attendee_email: 
            event['attendees'][i]['comment'] = request
            api.events().update(calendarId='primary', eventId=event_id, body=event).execute()
            break 
    return
    
def change_event_owner(api, event_id, destination_calendar_id):
    """
    This function change the event's owner
    """
    correct_destination = True
    try:
        api.events().move(calendarId='primary', eventId=event_id, destination=destination_calendar_id).execute()
    except:
        correct_destination = False

    if not correct_destination:
        raise Exception("Invalid new owner")


def update_event(api,event_id, key, value):
    """
    This function update the event's property (Not all can be updated) 
    """
    event = api.events().get(calendarId='primary', eventId=event_id).execute()
    if key == 'eventType':
        event['eventType'] = event_type_checker(value.lower())

    elif key == 'summary':
        event['summary'] = event_name_checker(value)

    elif key == 'location':
        event['location'] = validate_event_location(event['eventType'], value)

    elif key == 'attendees':
        event['attendees'] = attendees_checker(value)

    elif key == 'start':
        valid_dates = is_start_after_end_checker(value, event['end']['date'])
        if valid_dates:
            event['start'] = {'date': date_format_range_checker(value)}
        else:
            raise Exception("Start date need to be smaller or equal to end date")

    elif key == 'end':
        valid_dates = is_start_after_end_checker(event['start']['date'], value)
        if valid_dates:
            event['end'] = {'date': date_format_range_checker(value)}
        else:
            raise Exception("Start date need to be smaller or equal to end date")

    else:
        raise Exception('Invalid key or value')

    api.events().update(calendarId='primary', eventId=event_id, body=event, sendUpdates='all').execute()


def calendar_view(api, lower, upper):
    """
    This function aims to allow attendees to view events in a certain range(lower,upper) inclusive.
    The attendees can only view events and their respective information for a maximum of 5 years
    in past (from today's date) and the next five years (in future). No events after 2050 are
    to be shown.
    """
    # check whether lower or upper is within 2050
    if upper.year > 2050 or lower.year > 2050:
        return

    # datetime.strptime(event_date, '%Y-%m-%d').date()
    date_today = date.today()
    lower_bound_date = date(date_today.year-5, date_today.month, date_today.day)
    upper_bound_date =  date(date_today.year+5, date_today.month, date_today.day)
    if lower >= lower_bound_date and upper <= upper_bound_date:
        # valid
        lower = convert_date_format(lower, "start")
        upper = convert_date_format(upper, "end")

    elif (lower >= lower_bound_date and lower <= upper_bound_date) and not(upper <= upper_bound_date):
        # if lower is valid but upper is not
        # then we retrieve from (lower,upper_bound_date)
        lower = convert_date_format(lower, "start")
        upper = convert_date_format(upper_bound_date, "end")
    elif not(lower >= lower_bound_date) and (upper>= lower_bound_date and upper <= upper_bound_date):
        # if lower is invalid but upper is
        # then wr retrieve from (lower_bound_date, upper)
        lower = convert_date_format(lower_bound_date, "start")
        upper = convert_date_format(upper, "end")
    else:
        # if both invalid, we retreive none events
        return None
    events = api.events().list(calendarId='primary', timeMin=lower, timeMax = upper).execute()
    return events


def navigation(api, navigator, date_input = None, searchType=None, keyword = None):
    """
    This function hanldes the mechanism of navigation at the backend of the UI component
    Basically control what event should be outputed when the user navigate through different dates, months or years
    Besides, this function also handle the forward backward functionality in the calendar application
    
    Input:
        1. api: the google calendar API
        2. navigator: The button event that we are listening to
        3. date_input: The date given after clicking the button
        4. keyword: keyword that we are searching for
    """

    navigator = navigator.lower()
    if navigator == "day":
        from_date = date_input 
        to_date = date_input
        return calendar_view(api, from_date, to_date)
    
    elif navigator == "month":
        from_date = date(date_input.year, date_input.month, 1)
        to_date = date(date_input.year, date_input.month, calculate_month_end_date(date_input.month))
        return calendar_view(api, from_date, to_date)
    
    elif navigator == "year":
        from_date = date(date_input.year, 1, 1)
        to_date = date(date_input.year, 12, calculate_month_end_date(12))
        return calendar_view(api, from_date, to_date)
    
    elif navigator == "backward" or navigator == "forward":
        # Need a checker for month and year here 
        # (12+1)!= 13 and ==1 (change year also +1)
        date_input = checker(navigator, date_input)
        return navigation(api, "month", date_input)
    
    elif navigator == "search":
        return search(api, searchType, keyword)
    else:
        # invalid navigator -> do nothing
        return


def search(api, searchtype, keyword):
    events = api.events().list(calendarId='primary').execute()
    relevant_events = []

    if searchtype in ["organizer", "creator"]: #
        for i in range(len(events)):
            for key in events[i][searchtype].keys():
                if keyword in events[i][searchtype][key]:
                    relevant_events.append(events[i])
                    break

    elif searchtype == "attendees": # list of dicts
        for i in range(len(events)):
            found = False
            for j in range(len(events[i][searchtype])):
                for key in events[i][searchtype][j].keys():
                    if keyword in events[i][searchtype][j][key]:
                        relevant_events.append(events[i])
                        found = True
                        break
                if found:
                    break
    else:
        for i in range(len(events)): # Any type other than data structure type
            if keyword in str(events[i][searchtype]):
                relevant_events.append(events[i])

    return relevant_events

def set_reminder(api, event_id, minutes):
    """
    The organiser as well as attendees can set up a reminder respective
    to the event and that will be shown on their own application
    """
    if minutes < 0 or minutes > 40320:
        raise Exception("Invalid minutes") 
        
    event = api.events().get(calendarId='primary', eventId=event_id).execute()
    event["reminders"] = {
        "useDefault": False,
        "overrides" : [
            {
                "method": "popup",
                "minutes": minutes
            }
        ]
    }
    api.events().update(calendarId='primary', eventId=event_id, body = event, sendUpdates = 'all').execute()

