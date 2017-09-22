from apiclient import discovery
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')

class Alberlendar():
    """takes google credentials to parse a google spreadsheets schedule into the calendar"""
    def __init__(*ars, **kwargs):

        def get_sheets_values(scheduleID='1xJcLh9yWGmqu_Blnp4yykb4cSnnus5fU4YoHFqGEf-o', service=discovery.build('calendar', 'v3', discoveryUrl)):
            """returns values from desired sheets"""
