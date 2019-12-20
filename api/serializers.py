from flask_restplus import fields

from api.restplus import api

deployment = api.model('Deployment', {
    'id': fields.String(readOnly=True, description='The unique identifier'),
    'customer': fields.String(required=True, description='Name of the customer'),
    'action': fields.String(required=True, description='Description of the action'),
    'date': fields.DateTime(required=True, description='Date of the deployment'),
    'price': fields.String(reqired=True, description='Price for this action'),
    'travel expense': fields.Integer(reqired=False, description='Travel Expenses (if applicable)'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

list_of_deployments = api.inherit('List of deployments', pagination, {
    'deployments': fields.List(fields.Nested(deployment))
})
