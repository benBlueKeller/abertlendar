from apiclient import discovery
import httplib2

from credentials import get_credentials
from util import par_sheet_dict

CREDENTIALS = get_credentials()
HTTP = CREDENTIALS.authorize(httplib2)
SHEETS = discovery.build('sheets', 'v4', http=HTTP,
                         discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')

class Schedule(dict):
    """Schedule turns tabs with 'CURRENT' and 'NEXT' google sheets
        salt & straw schedule into a dict"""
    def __init__(self, schedule_id='1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o',
                 sheets=SHEETS):
        super(Shifts, self).__init__()
        spreadsheet = sheets.spreadsheets().get(spreadsheetId=schedule_id).execute()['sheets']
        for sheet in schedule:
            if sheet['properties']['title'].find("CURRENT") > -1 or sheet['properties']['title'].find("NEXT") > -1:
                schedule = sheets.spreadsheets().values().get(
                    spreadsheetId=scheduleId, range=sheet['properties']['title']).execute()
                values = schedule.get('values', [])
                # figure out how to combine various dicts
