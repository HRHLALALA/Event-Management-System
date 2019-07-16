# Event Management system
## Team: Segmentation Fault

## Framework
Frontend: HTML,CSS,Django
Backend: Python Flask, Flask-SQLAlchemy

## Member Assignment

Front-End Part: Yiwei Zhang
Back-End Part: Renhao Huang


## Preliminary Requirements from UNSW
The events organised in the university can be grouped broadly into two categories namely courses and seminars. 

Each event is scheduled at a particular venue and can run for a single day or over a period of days. Each event has a maximum attendee capacity. Each scheduled event has a de-register window period up and until which a registered attendee is allowed to de-register from the event, e.g., a course ‘photo- shop’ can be cancelled up to 24 hours before the scheduled date’.
A course is delivered by a single presenter who will also post the event on the EMS. A seminar consists of multiple sessions and each session can be presented by a UNSW academic or a non-UNSW guest-speaker e.g., “7th Australasian Symposium on Big Data & Analytics” is a seminar which runs from 2nd of October, 2018 to 3rd of October, 2018 and consists of sessions such as ‘Using Machine Learning to analyse financial data’, ‘Semantic ontologies for financial data analysis’, ‘Predictive Analytics’. A seminar is posted on the
EMS by a convenor, who may or may not be a speaker at one of the sessions. The system should provide different forms to handle the posting of the above two types of events.

The EMS is only accessible by members (staff and students) of UNSW. Users should be able to log into the system with their zID and password. Once a user has logged into the system, they should see the two categories of events and list of all the ‘open events’ under each category. Clicking on a particular event should provide more details about the event. A user can select a particular event and register for this event. Once the user has successfully registered, a confirmation is displayed to the user. A registered user can cancel their registration up and until the de-registration window specified for that particular event.
Only UNSW staff are allowed to post (i.e., convene) events. Both UNSW staff and student can register for any event provided the event capacity has not exceeded. However, a UNSW staff cannot register for an event for which they are the convenor. Both UNSW staff and students can register for an event. Every logged in user must also have a link to a dashboard. If the user is a student, then the dashboard should display all current and past events that they have registered for. If the user is a staff, then their dashboard will display (i) current and past events that they have registered for (ii) current and past events that they have posted (iii) any cancelled events. Additionally, when a convenor clicks on an event they have organised, they should be able to see a list of attendees for that event. An unauthenticated user cannot access the website.

 At any point in time, an event can be ‘open’, ‘closed’ or ‘cancelled’. Any event which is scheduled to run in the future or currently running is said to be ‘open’. Once an event has been completed, the course convenor will change the status of the event to ‘closed’. If an event is cancelled before the scheduled-date, then it is said to be ‘cancelled’.
The customer has also advised your team that they are still unsure of all their requirements, but these are their preliminary requirements. They would refine their requirements after seeing an initial version of the software system. Keeping this in mind, your consultancy firm has decided that this project will be delivered adopting an agile software development methodology to give the team flexibility to be able to adapt to the customer changes.

## Default member
Type: Trainer
name="aaa",zid="aaa",id="aaa",password="aaa"

Type: Trainee
name="bbb",zid="bbb",id="bbb",password="bbb"

## Contributions:(most of)
1. html files(htmls,css) are by Yiwei Zhang
2. python files are written by Renhao Huang
3. Debug: together
4. Idea: together

## Meeting Summary:
4/25:
1. 4/25 is public holiday so this is an online meeting.
2. Database system, python files, html+css files are nearly finish and all of them are tested separately.
3. All the files can put together and the system can run by the end of the week.
4. After that we will focus on debug.

2/5
1. The separate pages for registered events and posted events are canceled.
2. The EMS main page is canceled and everyting will display om the Dashboard.
3. We re-read the Preliminary Requirements and decide to add some new features.
4. Add a new feature that is the seminar events can add sessions and the seminar without sessions will not appear on the "open events".
5. Add a new feature that is the users cannot cancel their registration up after the de-registration window.
6. Add a new feature that is events can only be cancelled up to 24 hours before the scheduled date.

That is the Velocity Chart by the end of week 09
![alt text](https://github.com/cs1531/segmentation-fault/blob/master/diagram/Velocity%20chart.png)
