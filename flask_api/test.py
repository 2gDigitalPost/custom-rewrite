from flask import Flask, jsonify, render_template, request
from flask_restful import reqparse, Resource, Api

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

parser = reqparse.RequestParser()

@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/files_select')
def files_select():
    return render_template('files_select.html')


class HelloWorld(Resource):
    def get(self):
        existing_languages = server.eval('@SOBJECT(twog/department_instructions)')

        return {'hello': existing_languages}


class DepartmentInstructions(Resource):
    def get(self):
        department_instructions = server.eval('@SOBJECT(twog/department_instructions)')

        return {'department_instructions_list': department_instructions}


class NewInstructionsTemplate(Resource):
    def get(self):

        department_instructions = server.eval('@SOBJECT(twog/department_instructions)')

        return {'department_instructions_list': department_instructions}

    def post(self):
        json_data = request.get_json()

        print(json_data)

        inserted_template = server.insert('twog/instructions_template', {'name': json_data.get('name')})

        for department_instruction in json_data.get('department_instructions'):
            server.insert('twog/department_instructions_in_template',
                          {'instructions_template_code': inserted_template.get('code'),
                           'department_instructions_code': department_instruction.get('code'),
                           'sort_order': department_instruction.get('sort_order')
                           }
                          )

        return {'status': 200}


class InstructionsTemplate(Resource):
    def get(self, instructions_template_id):
        instructions_template_sobject = server.eval('@SOBJECT(twog/instructions_template["code", "{0}"])'.format(instructions_template_id))
        department_instructions_in_template_sobjects = server.eval('@SOBJECT(twog/department_instructions_in_template["instructions_template_code", "{0}"])'.format(instructions_template_id))
        department_instructions_sobjects_in_template = server.eval('@SOBJECT(twog/department_instructions["code", "in", "{0}"])'.format('|'.join([department_instructions_in_template_sobject.get('department_instructions_code') for department_instructions_in_template_sobject in department_instructions_in_template_sobjects])))
        department_instructions_sobjects_not_in_template = server.eval('@SOBJECT(twog/department_instructions["code", "not in", "{0}"])'.format('|'.join([department_instructions_in_template_sobject.get('department_instructions_code') for department_instructions_in_template_sobject in department_instructions_in_template_sobjects])))

        return {'instructions_template': instructions_template_sobject,
                'department_instructions_in_template': department_instructions_sobjects_in_template,
                'department_instructions_not_in_template': department_instructions_sobjects_not_in_template}

    def post(self):
        args = parser.parse_args()

        print(args)


api.add_resource(HelloWorld, '/')
api.add_resource(DepartmentInstructions, '/department_instructions')
api.add_resource(NewInstructionsTemplate, '/instructions_template')
api.add_resource(InstructionsTemplate, '/instructions_template/<string:instructions_template_id>')

if __name__ == '__main__':
    app.run(debug=True)

