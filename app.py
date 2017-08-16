
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
# begin own imports seperate
import sys

from datetime import datetime
from datetime import timedelta
import pytz


import pdb; pdb.set_trace();


#oauth argparser
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None
flags = None


 #first commit using atom

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

from util import scooper_match



def main():


    def par_sheet(values):
        shifts = []
        this_week = False
        for irow, row in enumerate(values):
            # look for the first row that has saturday in column A
            if len(row) > 0:
                if row[0].rstrip().lstrip().upper() == 'SATURDAY':
                    weekdays = []
                    for col in row:
                        trimmed = col.rstrip().lstrip()
                        #checks for weekdays by finding alpha strings
                        if trimmed.isalpha() == True:
                            weekday = trimmed
                        elif trimmed != '' and '/' in trimmed:
                            #split parts apart to add leading zeros to month\day
                            spl = trimmed.split("/", 2)
                            if len(spl[0]) != 2:
                                spl[0] =  '0' + spl[0]
                            if len(spl[1]) != 2:
                                spl[1] = '0' + spl[1]
                            date = datetime.strptime("/".join(spl), "%m/%d/%Y")
                            weekdays.append((date, weekday))
                    this_week = weekdays

                elif this_week:
                    counter = 0
                    shift = []
                    row_shifts = []

                    for col in row:
                        shift.append(col)
                        counter += 1
                        if counter >= 3:
                            row_shifts.append(shift)
                            counter = 0
                            shift = []

                    for ishift, shift in enumerate(row_shifts):
                        if ishift < len(this_week) and "-" in shift[2]:
                            date, weekday = this_week[ishift]
                            time_str = shift[2].strip()
                            if " " in time_str and not "@" in time_str: 
                                time_str, duty = time_str.split(" ", 1)
                            # BUG: ValueError; for format "@ # #:##-{}" start_time will be wrong
                            try:
                                start_str, end_str = time_str.split('-', 1)
                                start_hours, start_minutes = start_str.split(':', 1)
                                start_hours = int(start_hours)
                                start_minutes = int(start_minutes)
                                if start_hours < 9: # assuming nine is the ealiest and 8 the latest start
                                    start_hours += 12
                                start_time = date + timedelta(hours=start_hours, minutes=start_minutes)
                            except ValueError:
                                pdb.set_trace()
                            try:
                                end_hours, end_minutes = end_str.split(':', 1)
                                end_hours = int(end_hours) + 12 # assuming all shifts end in pm
                                end_minutes = int(end_minutes)
                                end_time = date + timedelta(hours=end_hours, minutes=end_minutes)
                            except ValueError: # for line and close shifts parse from length
                                try:
                                    hours_from_start = float(shift[1])
                                    if hours_from_start >= 6:
                                        hours_from_start += 0.5 # length does not include breaks
                                    end_time = start_time + timedelta(hours=hours_from_start)
                                except ValueError:
                                    end_time = start_time + timedelta(hours=1)
                            shifts.append(dict(name = shift[0],
                                length=shift[1],
                                start= start_time,
                                end = end_time,
                                time_str = time_str,
                                row = irow))
        return shifts

    def par_sheet_dict(values):
        shifts = par_sheet(values)
        scoopers = set()
        time_min = shifts[0]["start"]
        time_max = shifts[0]["end"]
        for shift in shifts:
            scoopers = scoopers.union([shift["name"].upper()])
            if shift["start"] < time_min:
                time_min = shift["start"]
            if shift["end"] > time_max:
                time_max = shift["end"]
        return dict(shifts=shifts, scoopers=scoopers, time_max=time_max, time_min=time_min)

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


    for sheet in scheduleSheets:
        print(sheet['properties'])
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
                count = 0
                for cal in cal_list:
                    if cal['summary'].find('alberlendar') > -1:
                        if count > 0:
                            for arg in sys.argv:
                                if arg.find('-') == -1 and cal['summary'].split(' ')[0].find(arg) > -1:
                                    cal_id = cal['id']
                        cal_id = cal['id']
                        count += 1
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
                    elif make_new == 'N':
                        use_primary = input('should I use your primary calendar?(y/n): ')[0].upper()
                        if use_primary == 'Y':
                            cal_id = 'primary'




            for shift in shifts:
                if "BEN" in shift["name"].upper():
                    #create an id that will identical, but constant, for each shift to avoid repeat events
                    id = ('salt' + str(shift['row']) +
                        'shift' + str(shift['start'].toordinal()) +
                        str(shift['start'].hour) + str(shift['start'].minute) +
                        str(shift['end'].hour) + str(shift['end'].minute))
                    exists = False

                    # add PST to timezones
                    shift['start'] = pst.localize(shift['start'])
                    shift['end'] = pst.localize(shift['end'])

                    event = {
                        'summary': "Salty Shift " + shift["time_str"],
                        'id': id,
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
