import unittest

from flask import Blueprint

from api.endpoints.deployment import ns as invoices_namespace, DeploymentsCollection
from api.restplus import api
from app import app


class TestCalendarService:
    def customer_events(self, year, month):
        return [{'kind': 'calendar#event',
                 'status': 'confirmed',
                 'created': '2019-09-19T15:52:50.000Z',
                 'updated': '2019-10-28T12:24:34.718Z',
                 'summary': 'Kunde: zeppelin',
                 'start': {'date': '2019-10-01'},
                 'end': {'date': '2019-10-02'},
                 'description': 'Action: Coaching\nPrice: 1800 €\nTravel Expense: 100 €'}]


class TestInvoiceApp(unittest.TestCase):
    def setUp(self):
        DeploymentsCollection.calendar_service = TestCalendarService()
        self.app = app
        blueprint = Blueprint('api', __name__, url_prefix='/api')

        api.init_app(blueprint)
        api.add_namespace(invoices_namespace)

        self.app.register_blueprint(blueprint)

    def test_deployments_parsed(self):
        with self.app.test_client() as context:
            response = context.get('/api/deployments', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'"customer": "zeppelin"', response.data)
            self.assertIn(b'"action": "Coaching"', response.data)
            self.assertIn(b'"price": "1800"', response.data)
            self.assertIn(b'"date": "2019-10-01', response.data)
