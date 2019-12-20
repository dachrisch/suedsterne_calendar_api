import logging
from datetime import datetime

import dateutil.parser
import parse
from flask_restplus import Resource

from api.calendar.service import GoogleCalendarService
from api.parsers import pagination_arguments
from api.restplus import api
from api.serializers import deployment

log = logging.getLogger(__name__)

ns = api.namespace('deployments', description='Operations for deployments')


class Deployment:
    ACTION_TEMPLATE = "Action: {value:w}"
    PRICE_TEMPLATE = "Price: {value:d}"
    TRAVEL_EXPENSE_TEMPLATE = "Travel Expense: {value}"
    id = 1
    customer = 'name'
    action = 'action'
    date = datetime(2019, 12, 1)
    price = 1280

    def __init__(self, calendar_entry):
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


@ns.route('/')
class DeploymentsCollection(Resource):
    calendar_service = GoogleCalendarService()

    @api.expect(pagination_arguments)
    @api.marshal_with(deployment)
    def get(self):
        return [Deployment(calendar_entry) for calendar_entry in
                DeploymentsCollection.calendar_service.customer_events(2019, 12)]


@ns.route('/<int:id>')
class DeploymentItem(Resource):
    calendar_service = GoogleCalendarService()

    @api.marshal_with(deployment)
    def get(self, id):
        return None
