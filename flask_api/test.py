from flask import Flask
from flask_restful import Resource, Api

import os, sys, inspect

import ConfigParser

sys.path.append('/home/apache/tactic/src/client')

from tactic_client_lib import TacticServerStub

app = Flask(__name__)
api = Api(app)

config = ConfigParser.ConfigParser()
config.read('config.ini')

# Get credentials from config file
user = config.get('credentials', 'user')
password = config.get('credentials', 'password')
project = config.get('credentials', 'project')

# Just get the dev server URL for now
url = config.get('server', 'dev')

# Get a server object to perform queries
server = TacticServerStub(server=url, project=project, user=user, password=password)


class HelloWorld(Resource):
    def get(self):
        existing_languages = server.eval('@SOBJECT(twog/department_instructions)')

        return {'hello': existing_languages}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
