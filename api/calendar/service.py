from datetime import datetime
from os import path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendarService(object):

    def customer_events(self, from_date: datetime, to_date: datetime, template: str = 'Kunde: '):
        events = self.make_service().events().list(calendarId='primary', timeMin=from_date.isoformat() + 'Z',
                                                   timeMax=to_date.isoformat() + 'Z',
                                                   singleEvents=True,
                                                   orderBy='startTime', q=template).execute().get('items', [])
        return events

    def event_by_id(self, _id):
        return self.make_service().events().get(calendarId='primary', eventId=_id).execute()

    @classmethod
    def make_service(cls):
        credentials = service_account.Credentials.from_service_account_file(
            path.join(path.join(path.expanduser('~'), '.credentials'), 'suedsterne-1328.json'),
            scopes=SCOPES).with_subject('cd@it-agile.de')

        service = build('calendar', 'v3', credentials=credentials)
        return service
