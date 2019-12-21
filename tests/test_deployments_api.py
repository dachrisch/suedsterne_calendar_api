import unittest
from datetime import datetime, date

from api.endpoints.deployment import DeploymentsCollection, DeploymentItem
from app import create_app


class FakeAuthProvider(object):

    @property
    def authorized(self):
        return True


class TestCalendarService:
    def customer_events(self, from_date: datetime, to_date: datetime, template: str = 'Kunde: '):
        one = {'kind': 'calendar#event',
               'id': '678495465gfds347859uzhkgjf',
               'summary': 'Kunde: zeppelin',
               'start': {'date': '2019-10-01'},
               'description': 'Action: Coaching\nPrice: 1800 €\nTravel Expense: 100 €'
               }
        two = {'kind': 'calendar#event',
               'id': 'jsdhfg945nkgfd374fe',
               'summary': 'Kunde: zeppelin',
               'start': {'date': '2019-10-02'},
               'description': 'Action: Coaching\nPrice: 1800 €\nTravel Expense: 100 €'
               }
        if from_date <= date(2019, 10, 1) < to_date:
            return [one, two]
        elif from_date <= date(2019, 10, 2) <= to_date:
            return [two]
        elif from_date <= date(2019, 10, 1) <= to_date:
            return [one]
        else:
            return []

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


class TestDeploymentsApi(unittest.TestCase):
    def setUp(self):
        DeploymentsCollection.calendar_service = TestCalendarService()
        DeploymentsCollection.auth_service = FakeAuthProvider()
        DeploymentItem.calendar_service = TestCalendarService()
        self.app = create_app().test_client()

    def test_none_found_with_start_date(self):
        response = self.app.get('/api/deployments?start_date=2019-10-03&end_date=2019-12-31', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'[]\n', response.data)

    def test_one_found_with_start_date(self):
        response = self.app.get('/api/deployments?start_date=2019-10-02&end_date=2019-12-31', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"id": "jsdhfg945nkgfd374fe"', response.data)

    def test_two_found_with_start_date(self):
        response = self.app.get('/api/deployments?start_date=2019-10-01&end_date=2019-12-31', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"id": "678495465gfds347859uzhkgjf"', response.data)
        self.assertIn(b'"id": "jsdhfg945nkgfd374fe"', response.data)

    def test_none_found_with_end_date(self):
        response = self.app.get('/api/deployments?start_date=2019-09-01&end_date=2019-09-02', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'[]\n', response.data)

    def test_one_found_with_end_date(self):
        response = self.app.get('/api/deployments?start_date=2019-09-01&end_date=2019-10-01', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"id": "678495465gfds347859uzhkgjf"', response.data)

    def test_two_found_with_end_date(self):
        response = self.app.get('/api/deployments?start_date=2019-09-01&end_date=2019-10-02', follow_redirects=True)
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
        self.assertIn(b'"travel_expense": "100"', response.data)

    def test_deployment_not_found(self):
        response = self.app.get('/api/deployments/not_available', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
