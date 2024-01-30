# Testing Strategies

## 1. Functionality
Our MyEventManager.py file would not actually work on the calendar itself as not all functionality required can be developed by only using the method provided by the google API. Hence, we have introduced some new methods to do the required functionality in the MyEventManager application.
## 2. The naming of test cases
- All test cases are named in a meaningful and self-explanatory way except for the combinatorial testing part. We can indicate what the tests are about and whether they are valid or invalid combinations but not explicitly write out everything at the test case title because it will be too long to write out all combinations. Hence, to improve understanding, we have written our test input for the combination in the docstring section of each test case for the combinatorial testing parts
## 3. Function explanation
### Cancel Function:
 - Since delete and cancel are actually the same things in the google API, so we decided to use the API’s delete method in both MyEventManager application’s functionalities but introduce a record log that store the cancelled event’s id to ensure only the cancelled event can be restored instead of both delete and cancel events.
- The cancel function supports the cancellation of present and future events only because the cancellation of past events does not make sense.
### Restore Function
- The restore function only supports the restoration of present and future events, in other words, the events that have been cancelled and it is a present or future event at the moment of restoration. As it does not make sense for a past event to be restored.
### Helper Functions
- For the purpose of modularisation, we have decided to break down most parts of the createEvent method into smaller parts. For instance, we developed a lot of small functions that handle the validation of dates format, address format, etc. and used them in the createEvent method itself to improve the maintainability of the software.
### Request function
- The way the request function in our implementation is developed is using the existing attendee response comment’s key in the event resources. Hence, it will not be like the actual function in the google calendar app where we can propose a time using the schedule but just give a message/request that asks for a change of venue or time. This makes sense as the word request has the definition of “an act of asking politely”.
# Event
- ## Event’s Attributes (Event Creation)
	**Black-box testing strategy: Combinatorial Testing (CT) and 			Equivalence Partitioning (EP)**
	
	Equivalence Partitioning is used here to derive the value that 			represents each EC and put them into combinatorial testing. Because it is unrealistic to input every possible value for a category into the combinatorial testing and test them which will result in enormous and meaningless test cases. Subsequently, we will take a value from each EC and put them into the category of combinatorial testing.
Combinatorial testing is used here because an event can only be formed if all the attributes related to it are all valid. There are a lot of combinations from all the categories of an event, so using pairwise testing can effectively reduce the number of test cases needed and avoid combinatorial explosion.
Besides, it can ensure that the event creation process works well when every category of an event is combined together.
The reason that the event id is not tested here is that the event id is generated automatically by the google calendar API itself and the user cannot interfere with it, hence we do not need to test the existence of the event id because it will be part of the event properties if the google API behave correctly.
We did not specify the valid and invalid types of date and event location because we have tested them in separate test cases as testing everything in 1 combinatorial testing might make everything look unclear and messy. Hence, if the respective test cases work well, it means that the valid and invalid address and the date range also work well in combinatorial testing.

-	## Event Date Format
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	 The test strategy used here is EP because it can efficiently minimise the number of test cases required to identify whether the event date can be inputted in either **yyyy-mm-dd** or **dd-MON-yy** formats.
The ECs are derived using guideline 5 specified in the notes but with 2 valid ECs and 1 invalid EC. This can ensure that we have tested all possible inputs in different ECs to ensure good coverage of specifications.

- ## Event’s dates range (Create and Update an event)
	**Black-box testing strategy: Boundary Value Analysis(BVA)**
	
	This functionality is about the date range of an event whenever an event organiser creates or updates an event, it has to be at present and future dates - no later than 2050. In order to test this functionality, we have used the boundary value analysis. When testing, we have made sure we create/update an event that is either today or before the year 2050. We have also created test cases when we raise an exception if the event date is not within this range, either in the past or after 2050. In our implementation, we have created a helper function called date_format_range_checker() that will do the range testing for us in both creation and update functions. In Assignment 1, our rationale was also checking for valid dates separately instead of the whole event. If any invalid date, we raise an exception. In our implementation, we have done the same.

- ## Event’s physical address
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	We have used EP as the testing strategy to test the validation of physical event address formats.
EP is used because there are quite a number of different formats which are Australia, American and full address or address with street abbreviation which forms a large test case if we want to test all of them.
We have broken down the possible input into different ECs such as Australia's full address, America’s full address, etc. which allows us to combine some of them to test together to minimise the number of test cases as America and Australia are having the same address format.
We have also tested 2 invalid ECs, which are empty addresses and the wrong address format to ensure everything is covered by the google calendar. The reason the correct format with the wrong value is not tested is that as mentioned by the lecturer, we do not need to validate the existence of the provided address, hence any value is acceptable as long as the address is made up of the correct component.

-	## Event viewing range
	**Black-box testing strategy: Boundary Value Analysis (BVA)**
	
	We have used the boundary value analysis technique to test the event viewing range of attendees and organizers because there is a 5-year range on both sides (past and future) for them to view the events. Hence, to ensure the functionality is tested comprehensively, we used this technique to test the boundary value of the range, both on and off-points on both sides of the boundary. This is to ensure that the application works well even in extreme boundary conditions and only 4 test cases are needed where each of them represents their own Equivalence classes.

# Functionality
-	## Deletion of Event
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	The strategy used here is EP. This is because there are a few ECs that can be derived from the category deletion of events to reduce the number of test cases because there are too many events if we want to test it all and it is impossible to do so. By using the EP, we can derive the ECs as past, present and future events each representing its own categories and test them to indicate all the events are able to cover.

- ## Cancellation and Restoration of Event
	**Black-box testing strategy used: Equivalence Partitioning (EP)**
	
	The test strategy used here is the EP. This is because there are too many events for us to test one by one. Hence, we can split the input into different ECs representing past, present and future events and select one input from each ECs to test on.
This can minimise the number of test cases needed to prove the cancellation of events works on different ECs.
For the restoration of the event, there is only a valid EC, which is the cancelled event. So, we only need to run the test on 1 input from that category.
There are 2 invalid input ECs which are trying to restore uncancelled events and cancelled events that already passed. Although usually only cancelled events will have the restore functionality, the way we wrote our code is that the restore functionality will take in the event id which has the possibility to be an event that has not been cancelled. So, we decided to test that case as well

- ## Update an Existing Event
	**Black-box testing strategy used: Equivalence Partitioning (EP)**
	
	This functionality allows an Organiser to update an existing event. We have used Equivalence class partitioning to test our functionality. We have derived two equivalence classes, one for the successful update of an event and the other for the unsuccessful update. A successful update will only happen if the attribute we are updating is being replaced by a valid input value. An unsuccessful update would be when either it's an invalid attribute or an invalid value to update the attribute of the event.

- ## Request a change of time/venue of the event
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	The testing technique that we used for this functionality is the Equivalence Partitioning method. This is because the attendee can make a lot of different requests for both venue and time, so we have derived 2 ECs for this functionality which are the request for time and the request for a venue change. Only 1 test case is needed in our implementation because we perform the request function by using the attendee response comment implemented in the google calendar API, so we can give requests in string form to ask for changes. Hence, we do not need 2 test cases to prove this function works as they are the same in a way.
Besides, there is no invalid EC because we can give any message we want as it is in the string form, so technically the organiser needs to differentiate the message, hence any input can be accepted.

- ## Transfer Event’s Ownership
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	The testing technique used here is equivalence partitioning because it can minimize the number of test cases needed to check whether the owner role of an event can be transferred. There are 2 ECs, one valid and one invalid which cover all possible scenarios while using this function. Hence, we just need to derive 2 test cases for the change event’s owner function.

-	## Create an event on behalf of others
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	The equivalence partitioning method is used to test whether a user can create an event on behalf of others. The reason is that if one user can create an event for others, it means the function works well for everyone. Hence, we derive one valid EC from the function, which is the user can successfully create an event on behalf of others and 1 test case is needed to cover everything.
There is no invalid EC because the existence of the function means the user can always create an event on behalf of others, so it is either success or failure.

- ## Add/Remove/Update Attendees (Organiser only)
	**Black-box testing strategy: Category Partitioning (CP)**
	
	We choose to use the category partitioning method to test this functionality because this function’s behavior depends on 2 properties at the same time, which are the role of the user that modifying the event and what function the user wants to perform. Hence, we come out with 8 possible combinations for the input values but 5 is enough to cover everything as we do not test exceptional cases (not Organiser) multiple times. The 5 combinations are:
	1.  Organiser Add attendee
	2.  Organiser Remove attendee
	3.  Organiser update attendee
	4.  Organiser performs an invalid function on attendee
	5.  Not Organiser trying to add attendee

- ## Attendee’s Response
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	Equivalence Partitioning is used to derive the test cases for this functionality. We have extracted 3 Equivalence classes from this functionality, which are accept, decline and invalid response. This can ensure that by testing only 3 values, each from one of the ECs, we are able to fully confirm that these responses will work for all the event invitations while maintaining the minimum number of test cases.

# Navigation
- ## Navigation(day, month, year, forward arrow, backward arrow)
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	The black-box testing technique used here is the Equivalence Partitioning method. The reason EP is used here is that we are able to derive equivalence classes from all the possible inputs and use one value from each class to test the whole functionality. The reason behind this choice is that navigation functionality can have a lot of possible input and testing all of them would not be realistic, hence we come out with some ECs that represent different navigation functions such as forward, backward, day, month, year, and search. Testing each value from them can ensure that the navigation can work on the other value as well which helps us to further minimise our test cases.

- ## Navigation (Search)
	**Black-box testing strategy : Equivalence Partitioning (EP) and Combinatorial testing**
	
	The black box testing technique used for the search functionality Equivalence Partitioning, we have split our testing into two equivalence classes, valid(key, value) resulting in a successful search of the event and either one or both of key or value to be invalid resulting in no show of relevant events.
The key in this can be all the possible attributes of the event, which results in many combinations of successful and unsuccessful searches. Category partitioning would just generate way too many test cases to test for each particular category, therefore to minimise our test cases, we have used combinatorial testing on the equivalence classes to test this functionality. In the combinatorial testing, we have used pairwise testing, which would test for each possible combination at least one time.
**Navigation and event viewing range are combined in the test cases, please look carefully**

# Notification & Reminders
- ## Notification
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	We used the equivalence partitioning method to derive test cases for the notification functionality of the MyEventManager application. This is because it can effectively reduce the number of test cases needed and as long as we test that it works for each EC, the notification will work on the other events. There are 5 valid ECs for input which each of which represent cancellation, changes, update event, update attendees (part of update event but with different function) and response to the event. There is no invalid EC, because this functionality is not a standalone function, but it is part of the google API method which handles the send notification function where we directly hardcoded the value. Therefore, we come out with 5 test cases to test this functionality.

- ## Reminders
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	This functionally allows the organiser as well as attendees to set up a reminder respective to the event and that will be shown on their own application(pop-up). We have used Equivalence class partitioning to derive our test cases for this functionality. We have extracted two equivalence classes from this functionality, which are reminders being set up successfully and reminders being set up unsuccessfully. This can ensure that by testing only these 2 values, each from one of the EC’s, we will be able to cover both the cases and organisers/attendees will be able to set up reminders while using the minimum number of test cases.

# JSON format
- ## Import/Export JSON format file
	**Black-box testing strategy: Equivalence Partitioning (EP)**
	
	This functionality allows the user to import an event and export an event from the application. We have used Equivalence Partitioning to test this functionality. We have grouped it into two classes for each import and export functionality. The two valid inputs were mainly exporting a JSON file and importing a JSON format file. And invalid EC would be if the import is happening with the incorrect JSON format. We have used this to cover all the cases possible in this functionality.

 # White Box Testing
Based on the test cases generated using Black Box testing, we were not able to cover branches of the update event method and get_calendar_api method. Since the coverage was low, and it was mainly low due to the update function, we used white box testing (branch coverage), to cover all of the branches in the function. The update function that we created had 8 branches, so we needed 9 test cases. We generated 7 new test cases to cover all the branches. We on we are getting a a branch Coverage of 90% and statement coverage of statement 94%. 