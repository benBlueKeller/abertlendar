from apiclient import discovery
import httplib2

from credentials import get_credentials
from schedule import Schedule


class Alberlendar():
    """takes google credentials to parse a google spreadsheets schedule into the calendar"""
    def __init__(self,
                 schedule_id="1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o"):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        sheets = discovery.build('sheets', 'v4', http=http,
                                 discoveryServiceUrl='https://sheets.googleapis.com/'
                                 '$discovery/rest?version=v4')
        calendar = discovery.build('calendar', 'v3', http=http)
        shifts = Schedule(sheets=sheets, schedule_id=schedule_id)
        import pdb; pdb.set_trace()

if __name__ == '__main__':
    ALB = Alberlendar()
