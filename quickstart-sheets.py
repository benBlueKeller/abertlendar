
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
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
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():


    def par_sheet(values):
        values
        teams = [];
        for irow, row in enumerate(values):
            # look for the first row that has saturday in column A
            if row[0].rstrip().lstrip().upper() == 'SATURDAY':
                week_1 = dict(row_0 = irow, days = dict())
                for col in row:
                    trimmed = col.rstrip().lstrip()
                    #checks for weekdays by finding alpha strings
                    if trimmed.isalpha() == True:
                        weekday = trimmed
                    elif trimmed != '' and '/' in trimmed:
                        print('\n\n\n')
                        print(trimmed)
                        print(row)
                        #split parts apart to add leading zeros to month\day
                        spl = trimmed.split("/", 2)
                        if len(spl[0]) != 2:
                            spl[0] =  '0' + spl[0] 
                        if len(spl[1]) != 2:
                            spl[1] = '0' + spl[1]
                        time = datetime.strptime("/".join(spl), "%m/%d/%Y")
                        week_1['days'][weekday] = time
                return week_1   

            else:
                rowlen = len(row)
                print(rowlen)
                print(row[0])
                print(row[rowlen - 1])


    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    rangeName = 'Class Data!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
    
    scheduleId ='1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o'
    schedule = service.spreadsheets().get(spreadsheetId=scheduleId).execute()
    scheduleSheets = schedule['sheets']
    for sheet in scheduleSheets:
        print(sheet['properties'])
        if sheet['properties']['title'].find("CURRENT") > -1:
            currentSchedule = service.spreadsheets().values().get(
                spreadsheetId=scheduleId, range=sheet['properties']['title']).execute()
            values = currentSchedule.get('values', [])
            week_1 = par_sheet(values)
            import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
