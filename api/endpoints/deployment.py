import calendar
import logging
from datetime import date

from flask import request
from flask_restplus import Resource

from api.auth import GoogleAuthProvider, UnauthorizedException
from api.calendar.service import GoogleCalendarService
from api.model import Deployment
from api.parsers import calendar_arguments
from api.restplus import api
from api.serializers import deployment

log = logging.getLogger(__name__)

ns = api.namespace('deployments', description='Operations for deployments')

@ns.route('/')
class DeploymentsCollection(Resource):
    calendar_service = GoogleCalendarService()
    auth_service = GoogleAuthProvider()

    @api.expect(calendar_arguments)
    @api.marshal_with(deployment)
    def get(self):
        if not DeploymentsCollection.auth_service.authorized:
            raise UnauthorizedException
        arguments = calendar_arguments.parse_args(request)

        try:
            start_date = date.fromisoformat(arguments.get('start_date'))
        except (TypeError, ValueError):
            log.debug('ignoring invalid start date: ' + str(arguments))
            start_date = date(date.today().year, date.today().month, 1)

        try:
            end_date = date.fromisoformat(arguments.get('end_date'))
        except (TypeError, ValueError):
            log.debug('ignoring invalid end date: ' + str(arguments))
            end_date = date(date.today().year, date.today().month,
                            calendar.monthrange(date.today().year, date.today().month)[1])

        return [Deployment(calendar_entry) for calendar_entry in
                DeploymentsCollection.calendar_service.customer_events(start_date, end_date)]


@ns.route('/<string:id>')
class DeploymentItem(Resource):
    calendar_service = GoogleCalendarService()

    @api.marshal_with(deployment)
    def get(self, id):
        return Deployment(DeploymentItem.calendar_service.event_by_id(id))
