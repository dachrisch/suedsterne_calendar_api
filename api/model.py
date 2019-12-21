from datetime import datetime

import dateutil.parser
import parse


class Deployment:
    ACTION_TEMPLATE = "Action: {value:w}"
    PRICE_TEMPLATE = "Price: {value:d}"
    TRAVEL_EXPENSE_TEMPLATE = "Travel Expense: {value:d}"
    id = 1
    customer = 'name'
    action = 'action'
    date = datetime(2019, 12, 1)
    price = 1280
    travel_expense = 100

    def __init__(self, calendar_entry):
        self.id = calendar_entry['id']
        self.customer = calendar_entry['summary'].replace('Kunde: ', '')
        self.date = dateutil.parser.parse(calendar_entry['start'].get('dateTime', calendar_entry['start'].get('date')))
        if 'description' not in calendar_entry:
            raise Exception('description missing: %s, %s' % (self.customer, self.date))
        self.action = self._parse(calendar_entry['description'], Deployment.ACTION_TEMPLATE)
        self.price = self._parse(calendar_entry['description'], Deployment.PRICE_TEMPLATE)
        self.travel_expense = self._parse(calendar_entry['description'], Deployment.TRAVEL_EXPENSE_TEMPLATE)

    def _parse(self, description, template):
        result = parse.search(template, description)
        if result:
            return result['value']
