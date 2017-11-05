from apiclient import discovery
import httplib2
import pytz

from credentials import get_credentials
from schedule import Schedule
from util import scooper_match

PST = pytz.timezone('US/Pacific')

class Alberlendar(object):
    """takes google credentials to parse a google spreadsheets schedule into the calendar"""
    def find_alberlendars(self):
        """return all calendars with 'alberlendar' in summary"""
        cal_list = self.calendar.calendarList().list().execute()['items'] #pylint: disable=E1101,C0301
        albs = []
        for cal in cal_list:
            if cal['summary'].find('alberlendar') > -1:
                albs.append(cal)
        return albs

    def scooper_alberlendar(self):
        """of find_alberlendars, return first calendar with this scooper in summary"""
        for aldar in self.find_alberlendars():
            if aldar['summary'].find(self.scooper) > -1:
                return aldar
        return None


    def __init__(self,
                 scooper,
                 cal_id=None,
                 schedule_id="1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o"):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        sheets = discovery.build('sheets', 'v4', http=http,
                                 discoveryServiceUrl='https://sheets.googleapis.com/'
                                 '$discovery/rest?version=v4')
        self.scooper = scooper
        self.calendar = discovery.build('calendar', 'v3', http=http)
        shifts = Schedule(sheets=sheets, schedule_id=schedule_id, pytz=PST)
        events_during_schedule = self.calendar.events().list(calendarId=cal_id, #pylint: disable=E1101,C0301
                                                             timeMin=shifts.time_min.isoformat(),
                                                             timeMax=shifts.time_max.isoformat()
                                                            ).execute().get('items', [])
        if cal_id is None:
            if self.scooper_alberlendar() is not None:
                cal_id = self.scooper_alberlendar()['id']
        for shift in shifts:
            if scooper_match(scooper, shift['name']):
                event_id = ('salt' + str(shift['row']) +
                            'shift' + str(shift['start'].toordinal()) +
                            str(shift['start'].hour) + str(shift['start'].minute) +
                            str(shift['end'].hour) + str(shift['end'].minute))
                event = {
                    'summary': "Salty Shift " + shift["time_str"],
                    'id': event_id,
                    'start': {
                        'dateTime': shift["start"].isoformat()
                    },
                    'end': {
                        'dateTime': shift["end"].isoformat()
                    }
                }
                exists = False
                for shared_event in events_during_schedule:
                    if event['id'] == shared_event['id']:
                        exists = True
                        print('ID exists:\n' + shared_event['id'])
                if not exists:
                    cal_event = self.calendar.events().insert(calendarId=cal_id, body=event).execute() #pylint: disable=E1101
                    print('Event created: {}'.format(cal_event.get('htmlLink')))

if __name__ == '__main__':
    ALB = Alberlendar(scooper="Ben",
                      cal_id="saltandstraw.com"
                      "_jgum8lvp1047r31f1leeq9debg@group.calendar.google.com")
