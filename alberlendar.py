import httplib2

from apiclient import discovery

from credentials import get_credentials

CREDENTIALS = get_credentials()
HTTP = CREDENTIALS.authorize(httplib2)
SHEETS = discovery.build('sheets', 'v4', http=HTTP,
                         discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')
CALENDAR = discovery.build('calendar', 'v3', http=HTTP)


class Alberlendar():
    """takes google credentials to parse a google spreadsheets schedule into the calendar"""
    def __init__(self,
                 schedule_id="1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o",
                 sheets=SHEETS):
        # only thing needed from SHEETS is parsed values, so
        # a seperate class should be need for fetching those valuse
        pass
