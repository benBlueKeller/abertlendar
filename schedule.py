from datetime import datetime
from datetime import timedelta

from util import par_sheet


class Schedule(list):
    """Schedule takes a sheets apiclient and schedule_id,
    then turns tabs with 'CURRENT' and 'NEXT' into a list of shifts"""
    def __init__(self, sheets, schedule_id, pytz=None):
        super(Schedule, self).__init__()
        spreadsheet = sheets.spreadsheets().get(spreadsheetId=schedule_id).execute()['sheets']
        self.scoopers = set()
        self.time_min = pytz.localize(datetime.max - timedelta(weeks=1))
        self.time_max = pytz.localize(datetime.min + timedelta(weeks=1))

        for sheet in spreadsheet:
            print(sheet['properties']['title'])
            if (sheet['properties']['title'].upper().find("CURRENT") > -1
                    or sheet['properties']['title'].upper().find("NEXT") > -1):
                schedule = sheets.spreadsheets().values().get(
                    spreadsheetId=schedule_id, range=sheet['properties']['title']).execute()
                values = schedule.get('values', [])
                self.extend(par_sheet(values, pytz))
        for shift in self:
            self.scoopers = self.scoopers.union([shift["name"].upper()])
            if shift["start"] < self.time_min:
                self.time_min = shift["start"]
            if shift["end"] > self.time_max:
                self.time_max = shift["end"]
