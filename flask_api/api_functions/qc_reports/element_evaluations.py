from flask import jsonify, request
from flask_restful import reqparse, Resource

import sys

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

sys.path.append(config.get('tacticpath', 'path'))

from tactic_client_lib import TacticServerStub

# Get credentials from config file
project = config.get('credentials', 'project')

# Just get the dev server URL for now
url = config.get('server', 'dev')


class ElementEvaluations(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        element_evaluations = server.eval("@SOBJECT(twog/element_evaluation)")

        return jsonify({'element_evaluations': element_evaluations})

    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        element_evaluation_data = json_data.get('element_evaluation')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        server.insert('twog/element_evaluation', element_evaluation_data)

        return jsonify({'status': 200})


class ElementEvaluationExistsByName(Resource):
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        element_evaluations = server.eval("@SOBJECT(twog/element_evaluation['name', '{0}'])".format(name))

        if element_evaluations:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})

