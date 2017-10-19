from datetime import datetime

from apiclient import discovery
import httplib2

from credentials import get_credentials
from util import par_sheet

CREDENTIALS = get_credentials()
HTTP = CREDENTIALS.authorize(httplib2)
SHEETS = discovery.build('sheets', 'v4', http=HTTP,
                         discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')

class Schedule(list):
    """Schedule turns tabs with 'CURRENT' and 'NEXT' google sheets
        salt & straw schedule into a list of shifts"""
    def __init__(self, schedule_id='1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o',
                 sheets=SHEETS):
        super(Schedule, self).__init__()
        spreadsheet = sheets.spreadsheets().get(spreadsheetId=schedule_id).execute()['sheets']
        self.scoopers = set()
        self.time_min = datetime.max
        self.time_max = datetime.min

        for sheet in spreadsheet:
            if (sheet['properties']['title'].find("CURRENT") > -1
                    or sheet['properties']['title'].find("NEXT") > -1):
                schedule = sheets.spreadsheets().values().get(
                    spreadsheetId=schedule_id, range=sheet['properties']['title']).execute()
                values = schedule.get('values', [])
                self.extend(par_sheet(values))
        for shift in self:
            self.scoopers = self.scoopers.union([shift["name"].upper()])
            if shift["start"] < self.time_min:
                self.time_min = shift["start"]
            if shift["end"] > self.time_max:
                self.time_max = shift["end"]
