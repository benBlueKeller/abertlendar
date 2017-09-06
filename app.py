
from __future__ import print_function
import httplib2

from apiclient import discovery
# begin own imports seperate
import sys


import pytz

from credentials import get_credentials
from util import scooper_match
from util import par_sheet_dict


#oauth argparser
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None
flags = None


def alberlendar():


def main():


    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')


    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    scheduleId ='1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o'
    schedule = service.spreadsheets().get(spreadsheetId=scheduleId).execute()
    scheduleSheets = schedule['sheets']

    cal_service = discovery.build('calendar', 'v3', http=http)
    # TODO: using argv, find or make proper calendar to operate on
    if '--primary' in sys.argv:
        cal_id = 'primary'
    else:
        cal_list = cal_service.calendarList().list().execute()['items']
        cal_id = False

    # access sheet and
    for sheet in scheduleSheets:
        if sheet['properties']['title'].find("CURRENT") > -1 or sheet['properties']['title'].find("NEXT") > -1:
            currentSchedule = service.spreadsheets().values().get(
                spreadsheetId=scheduleId, range=sheet['properties']['title']).execute()
            values = currentSchedule.get('values', [])
            schedule = par_sheet_dict(values)
            shifts = schedule['shifts']
            pst = pytz.timezone('US/Pacific')

            this_scooper = False
            for scooper in schedule['scoopers']:
                for arg in sys.argv:
                    if scooper_match(arg, scooper):
                        this_scooper = arg
            while not this_scooper:
                this_scooper = input("What is your name on the schedule? ")

            if not cal_id:
                alberlendars = []
                for cal in cal_list:
                    if cal['summary'].find('alberlendar') > -1:
                        for arg in sys.argv:
                            if arg.find('-') == -1 and cal['summary'].split(' ')[0].find(arg) > -1:
                                cal_id = cal['id']
                if not cal_id:
                    make_new = input('should I add a new calendar to google?(y/n): ')[0].upper()
                    if make_new == 'Y':
                        def capitalize(name):
                            return name[0].upper() + name[1:].lower()
                        calendar = {
                            "summary": capitalize(this_scooper) + "'s alberlendar",
                            "timeZone": "America/Los_Angeles"
                        }
                        cal_service.calendars().insert(body=calendar).execute()
                        pass
                    else:
                        use_primary = input('should I use your primary calendar?(y/n): ')[0].upper()
                        if use_primary == 'Y':
                            cal_id = 'primary'




            print("scooper: " + this_scooper)
            for shift in shifts:
                if this_scooper.upper() in shift["name"].upper():
                    #create an id that will identical, but constant, for each shift to avoid repeat events
                    event_id = ('salt' + str(shift['row']) +
                        'shift' + str(shift['start'].toordinal()) +
                        str(shift['start'].hour) + str(shift['start'].minute) +
                        str(shift['end'].hour) + str(shift['end'].minute))
                    exists = False

                    # add PST to timezones
                    shift['start'] = pst.localize(shift['start'])
                    shift['end'] = pst.localize(shift['end'])

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


                    shared_time_events = cal_service.events().list(calendarId=cal_id, timeMin=shift['start'].isoformat(), timeMax=shift['end'].isoformat()).execute()
                    items = shared_time_events.get('items', [])
                    for shared_event in items:
                        if event['id'] == shared_event['id']:
                            exists = True
                            print('ID exists:\n' + shared_event['id'])





                    if not exists:
                        cal_event = cal_service.events().insert(calendarId=cal_id, body=event).execute()
                        print('Event created: {}'.format(cal_event.get('htmlLink')))

if __name__ == '__main__':
    main()
