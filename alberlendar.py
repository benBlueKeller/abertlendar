from apiclient import discovery
import httplib2
import pytz

from credentials import get_credentials
from schedule import Schedule

PST = pytz.timezone('US/Pacific')

class Alberlendar():
    """takes google credentials to parse a google spreadsheets schedule into the calendar"""
    def __init__(self,
                 scooper,
                 cal_id,
                 schedule_id="1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o"):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        sheets = discovery.build('sheets', 'v4', http=http,
                                 discoveryServiceUrl='https://sheets.googleapis.com/'
                                 '$discovery/rest?version=v4')
        calendar = discovery.build('calendar', 'v3', http=http)
        shifts = Schedule(sheets=sheets, schedule_id=schedule_id, pytz=PST)
        events_during_schedule = calendar.events().list(calendarId=cal_id, timeMin=shifts.time_min.isoformat(), timeMax=shifts.time_max.isoformat()).execute() #pylint: disable=E1101,C0301

if __name__ == '__main__':
    ALB = Alberlendar(scooper="Ben",
                      cal_id="saltandstraw.com"
                      "_jgum8lvp1047r31f1leeq9debg@group.calendar.google.com")
