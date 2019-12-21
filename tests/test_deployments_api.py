import unittest

from api.endpoints.deployment import DeploymentsCollection, DeploymentItem
from app import create_app


class TestCalendarService:
    def customer_events(self, year, month):
        return [{'kind': 'calendar#event',
                 'id': '678495465gfds347859uzhkgjf',
                 'summary': 'Kunde: zeppelin',
                 'start': {'date': '2019-10-01'},
                 'description': 'Action: Coaching\nPrice: 1800 €\nTravel Expense: 100 €'
                 },
                {'kind': 'calendar#event',
                 'id': 'jsdhfg945nkgfd374fe',
                 'summary': 'Kunde: zeppelin',
                 'start': {'date': '2019-10-02'},
                 'description': 'Action: Coaching\nPrice: 1800 €\nTravel Expense: 100 €'
                 }]

    def event_by_id(self, id):
        if '678495465gfds347859uzhkgjf' == id:
            return {'kind': 'calendar#event',
                    'id': '678495465gfds347859uzhkgjf',
                    'status': 'confirmed',
                    'created': '2019-09-19T15:52:50.000Z',
                    'updated': '2019-10-28T12:24:34.718Z',
                    'summary': 'Kunde: zeppelin',
                    'start': {'date': '2019-10-01'},
                    'end': {'date': '2019-10-02'},
                    'description': 'Action: Coaching\nPrice: 1800 €\nTravel Expense: 100 €'}
        else:
            return None


class TestInvoiceApp(unittest.TestCase):
    def setUp(self):
        DeploymentsCollection.calendar_service = TestCalendarService()
        DeploymentItem.calendar_service = TestCalendarService()
        self.app = create_app().test_client()

    def test_deployments_parsed(self):
        response = self.app.get('/api/deployments', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"id": "678495465gfds347859uzhkgjf"', response.data)
        self.assertIn(b'"id": "jsdhfg945nkgfd374fe"', response.data)

    def test_deployment_by_id(self):
        response = self.app.get('/api/deployments/678495465gfds347859uzhkgjf', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"id": "678495465gfds347859uzhkgjf"', response.data)
        self.assertIn(b'"customer": "zeppelin"', response.data)
        self.assertIn(b'"action": "Coaching"', response.data)
        self.assertIn(b'"price": "1800"', response.data)
        self.assertIn(b'"date": "2019-10-01', response.data)

    def test_deployment_not_found(self):
        response = self.app.get('/api/deployments/not_available', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
