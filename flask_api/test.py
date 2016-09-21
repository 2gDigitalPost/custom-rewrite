from flask import Flask, render_template
from flask_restful import Resource, Api

import os, sys, inspect

import ConfigParser

sys.path.append('/home/apache/tactic/src/client')

from tactic_client_lib import TacticServerStub

sys.path.append('/opt/spt/custom')

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


@app.route('/hello')
def hello():
    return render_template('hello.html')


class HelloWorld(Resource):
    def get(self):
        existing_languages = server.eval('@SOBJECT(twog/department_instructions)')

        return {'hello': existing_languages}


class DepartmentInstructions(Resource):
    def get(self):
        department_instructions = server.eval('@SOBJECT(twog/department_instructions)')

        return {'department_instructions_list': department_instructions}


class InstructionsTemplate(Resource):
    def get(self, instructions_template_id):
        instructions_template_sobject = server.eval('@SOBJECT(twog/instructions_template["code", "{0}"])'.format(instructions_template_id))
        department_instructions_in_template_sobjects = server.eval('@SOBJECT(twog/department_instructions_in_template["instructions_template_code", "{0}"])'.format(instructions_template_id))
        department_instructions_sobjects_in_template = server.eval('@SOBJECT(twog/department_instructions["code", "in", "{0}"])'.format('|'.join([department_instructions_in_template_sobject.get('department_instructions_code') for department_instructions_in_template_sobject in department_instructions_in_template_sobjects])))
        department_instructions_sobjects_not_in_template = server.eval('@SOBJECT(twog/department_instructions["code", "not in", "{0}"])'.format('|'.join([department_instructions_in_template_sobject.get('department_instructions_code') for department_instructions_in_template_sobject in department_instructions_in_template_sobjects])))

        return {'instructions_template': instructions_template_sobject,
                'department_instructions_in_template': department_instructions_sobjects_in_template,
                'department_instructions_not_in_template': department_instructions_sobjects_not_in_template}


api.add_resource(HelloWorld, '/')
api.add_resource(DepartmentInstructions, '/department_instructions')
api.add_resource(InstructionsTemplate, '/instructions_template/<string:instructions_template_id>')

if __name__ == '__main__':
    app.run(debug=True)

