from flask_restplus import reqparse

calendar_arguments = reqparse.RequestParser()
calendar_arguments.add_argument('start_date', type=str, required=False, help='First day of Deployments to retrieve')
calendar_arguments.add_argument('end_date', type=str, required=False, help='Last day of Deployments to retrieve')
