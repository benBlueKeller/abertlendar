import httplib2

from apiclient import discovery

from credentials import get_credentials

SHEETS = discovery.build('sheets', 'v4', http=http,
                         discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')


class Alberlendar():
    """takes google credentials to parse a google spreadsheets schedule into the calendar"""
    def __init__(self,
                 http=credentials.authorize(httplib2.Http()),
                 credentials=get_credentials(),
                 schedule_id="1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o",
                 sheets = SHEETS):
        pass
