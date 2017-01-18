from flask import Flask, jsonify, render_template, request, flash, session, abort
from flask_cors import CORS
from flask_restful import reqparse, Resource, Api

import sys

import ConfigParser

from api_functions.department_requests import add_tasks_to_department_request_dictionary

config = ConfigParser.ConfigParser()
config.read('config.ini')

sys.path.append(config.get('tacticpath', 'path'))

from tactic_client_lib import TacticServerStub

sys.path.append('/opt/spt/custom')

app = Flask(__name__)
CORS(app)
api = Api(app)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.secret_key = SECRET_KEY

# Get credentials from config file
project = config.get('credentials', 'project')

# Just get the dev server URL for now
url = config.get('server', 'dev')

from flask_login import current_user


@app.route("/api/v1/login", methods=["POST"])
def api_login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        # Missing arguments
        abort(400)

    server = TacticServerStub(server=url, project=project, user=username, password=password)
    ticket = server.get_ticket(username, password)

    session['ticket'] = ticket

    return jsonify({ 'ticket': ticket })


@app.route('/')
def index():
    return render_template('index.html')


class DepartmentInstructions(Resource):
    def get(self):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        department_instructions = server.eval('@SOBJECT(twog/department_instructions)')

        return {'department_instructions_list': department_instructions}


class NewInstructionsTemplate(Resource):
    def get(self):
        server = TacticServerStub(server=url, project=project, ticket=current_user.id)

        department_instructions = server.eval('@SOBJECT(twog/department_instructions)')

        return {'department_instructions_list': department_instructions}

    def post(self):
        server = TacticServerStub(server=url, project=project, ticket=current_user.id)

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
        server = TacticServerStub(server=url, project=project, ticket=current_user.id)

        instructions_template_sobject = server.eval('@SOBJECT(twog/instructions_template["code", "{0}"])'.format(instructions_template_id))
        department_instructions_in_template_sobjects = server.eval('@SOBJECT(twog/department_instructions_in_template["instructions_template_code", "{0}"])'.format(instructions_template_id))
        department_instructions_sobjects_in_template = server.eval('@SOBJECT(twog/department_instructions["code", "in", "{0}"])'.format('|'.join([department_instructions_in_template_sobject.get('department_instructions_code') for department_instructions_in_template_sobject in department_instructions_in_template_sobjects])))
        department_instructions_sobjects_not_in_template = server.eval('@SOBJECT(twog/department_instructions["code", "not in", "{0}"])'.format('|'.join([department_instructions_in_template_sobject.get('department_instructions_code') for department_instructions_in_template_sobject in department_instructions_in_template_sobjects])))

        return {'instructions_template': instructions_template_sobject,
                'department_instructions_in_template': department_instructions_sobjects_in_template,
                'department_instructions_not_in_template': department_instructions_sobjects_not_in_template}


class Clients(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        # ticket = session.get('ticket')
        server = TacticServerStub(server=url, project=project, ticket=ticket)

        client_sobjects = server.eval("@SOBJECT(twog/client)")

        return jsonify({'clients': client_sobjects})


class Divisions(Resource):
    def get(self, client_code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        division_sobjects = server.eval("@SOBJECT(twog/division['client_code', '{0}'])".format(client_code))

        return jsonify({'divisions': division_sobjects})


class AllTitles(Resource):
    def get(self, ticket):
        server = TacticServerStub(server=url, project=project, ticket=ticket)

        title_sobjects = server.eval("@SOBJECT(twog/title)")

        return jsonify({'titles': title_sobjects})


class OrderPriorities(Resource):
    def get(self):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        order_sobjects = server.eval("@SOBJECT(twog/order['@ORDER_BY', 'priority asc'])")

        priority_levels = {}
        previous_priority = 0

        for iterator, order_sobject in enumerate(order_sobjects):
            current_priority = order_sobject.get('priority')

            if current_priority != previous_priority:
                priority_levels[iterator] = current_priority
                previous_priority = current_priority
            else:
                priority_levels[iterator] = None

        for priority_level, priority_decimal in priority_levels.iteritems():
            if priority_decimal is None:
                previous_priority = priority_levels.get(priority_level - 1)
                next_priority = priority_levels.get(priority_level + 1)

                if previous_priority is None:
                    previous_priority = 0.0

                if next_priority is None:
                    next_priority = 600000.0

                priority_levels[priority_level] = (previous_priority + next_priority) / 2.0

        return {'orders': order_sobjects, 'count': len(order_sobjects), 'priority_levels': priority_levels}

    def post(self):
        server = TacticServerStub(server=url, project=project, ticket=current_user.id)

        json_data = request.get_json()

        update_data = {}

        for order_code, priority in json_data.iteritems():
            order_search_key = server.build_search_key('twog/order', order_code, project_code='twog')
            update_data[order_search_key] = {'priority': float(priority)}

        server.update_multiple(update_data)

        return {'status': 200}


class FullOrder(Resource):
    """
    Given an order's unique code, return all the details possible on that order. This includes the twog/order sobject,
    all twog/component sobjects, and all twog/package sobjects.
    """

    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the order sobject (there should be only one, but it still returns in a list)
        order_sobject = server.eval("@SOBJECT(twog/order['code', '{0}'])".format(code))[0]

        # Get all the components associated with the order
        component_sobjects = server.eval("@SOBJECT(twog/component['order_code', '{0}'])".format(code))

        component_sobjects_full = []

        title_codes_list = [component_sobject.get('title_code') for component_sobject in component_sobjects]
        title_codes_string = '|'.join([title_code for title_code in title_codes_list])
        titles = server.eval("@SOBJECT(twog/title['code', 'in', '{0}'])".format(title_codes_string))

        titles_dict = {}

        for title in titles:
            titles_dict[title.get('code')] = title

        component_codes_list = [component_sobject.get('code') for component_sobject in component_sobjects]
        component_codes_string = '|'.join([component_code for component_code in component_codes_list])

        tasks = server.eval("@SOBJECT(sthpw/task['search_code', 'in', '{0}'])".format(component_codes_string))

        tasks_dict = {}

        for task in tasks:
            task_search_code = task.get('search_code')

            if task_search_code in tasks_dict:
                tasks_dict[task_search_code].append(task)
            else:
                tasks_dict[task_search_code] = [task]

        file_flows = server.eval("@SOBJECT(twog/file_flow['component_code', 'in', '{0}'])".format(component_codes_string))
        file_flow_codes = [file_flow.get('code') for file_flow in file_flows]
        file_flow_codes_string = '|'.join(file_flow_codes)

        file_flow_to_package_sobjects = server.eval("@SOBJECT(twog/file_flow_to_package['file_flow_code', 'in', '{0}'])".format(file_flow_codes_string))

        file_flows_to_package_dict = {}

        for file_flow_to_package_sobject in file_flow_to_package_sobjects:
            file_flow_code = file_flow_to_package_sobject.get('file_flow_code')

            if file_flow_code in file_flows_to_package_dict:
                file_flows_to_package_dict[file_flow_code].append(file_flow_to_package_sobject)
            else:
                file_flows_to_package_dict[file_flow_code] = [file_flow_to_package_sobject]

        # Get all the details of all the components
        for component_sobject in component_sobjects:
            component_sobject_full = {'code': component_sobject.get('code'), 'component': component_sobject}

            # A component may or may not have a title associated with it
            if component_sobject.get('title_code'):
                component_sobject_full['title'] = titles_dict.get(component_sobject.get('title_code'))
            else:
                component_sobject_full['title'] = None

            # Get the tasks assigned to the component, if any
            component_sobject_full['tasks'] = tasks_dict.get(component_sobject.get('code'))

            component_sobject_full['file_flows'] = []

            for file_flow in file_flows:
                if file_flow.get('component_code') == component_sobject.get('code'):
                    component_sobject_full['file_flows'].append(file_flow)

            component_sobjects_full.append(component_sobject_full)

        # Get all the packages associated with the order
        package_sobjects = server.eval("@SOBJECT(twog/package['order_code', '{0}'])".format(code))

        return jsonify({'order': order_sobject, 'components': component_sobjects, 'packages': package_sobjects,
                        'components_full': component_sobjects_full,
                        'file_flows_to_packages': file_flows_to_package_dict})


class Orders(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        order_sobjects = server.eval("@SOBJECT(twog/order)")

        return jsonify({'orders': order_sobjects})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        json_data = request.get_json()

        # Some data can have None set as the value. This does not work when inserting to the database, so remove
        # these keys/values
        cleaned_json_data = {key: value for key, value in json_data.iteritems() if value != None}

        print(cleaned_json_data)

        inserted_order = server.insert('twog/order', cleaned_json_data)

        return {'status': 200, 'order_code': inserted_order.get('code')}


class Title(Resource):
    def get(self, name):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        found_titles = server.eval("@SOBJECT(twog/title['name', 'EQ', '{0}'])".format(name))

        return {'status': 200, 'titles': found_titles}


class Titles(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        title_sobjects = server.eval("@SOBJECT(twog/title)")

        return jsonify({'titles': title_sobjects})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        json_data = request.get_json()

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Some data can have None set as the value. This does not work when inserting to the database, so remove
        # these keys/values
        cleaned_json_data = {key: value for key, value in json_data.iteritems() if value != None}

        imdb_id = json_data.get('imdb_id')

        if imdb_id:
            existing_title = server.eval("@SOBJECT(twog/title['imdb_id', '{0}'])".format(imdb_id))

            if existing_title:
                # HTTP status 409: Conflict
                return {'status': 409}

        inserted_title = server.insert('twog/title', cleaned_json_data)

        return {'status': 200, 'inserted_title': inserted_title}


class TitleAdder(Resource):
    def post(self):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        json_data = request.get_json()

        # Some data can have None set as the value. This does not work when inserting to the database, so remove
        # these keys/values
        cleaned_json_data = {key: value for key, value in json_data.iteritems() if value != None}

        imdb_id = json_data.get('imdb_id')
        existing_title = server.eval("@SOBJECT(twog/title['imdb_id', '{0}'])".format(imdb_id))

        if existing_title:
            # HTTP status 409: Conflict
            return {'status': 409}

        inserted_title = server.insert('twog/title', cleaned_json_data)

        flash('Title added successfully: {0}'.format(inserted_title.get('code')))

        return {'status': 200, 'inserted_title': inserted_title}


class ComponentsInOrder(Resource):
    def get(self, code):
        pass

    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        components_to_insert_list = []

        for component in json_data.get('components'):
            component_data_to_insert = {
                'name': component.get('name'),
                'order_code': code,
                'title_code': component.get('title_code')
            }

            if component.get('language_code'):
                component_data_to_insert['language_code'] = component.get('language_code')

            if component.get('pipeline_code'):
                component_data_to_insert['pipeline_code'] = component.get('pipeline_code')

            components_to_insert_list.append(component_data_to_insert)

        server.insert_multiple('twog/component', components_to_insert_list)

        return jsonify({'status': 200})


class Languages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        language_sobjects = server.eval("@SOBJECT(twog/language)")

        return jsonify({'languages': language_sobjects})


class DepartmentInstructionsAdder(Resource):
    def post(self):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        json_data = request.get_json()

        server.insert('twog/department_instructions', json_data)

        return {'status': 200}


class Pipeline(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        pipeline_sobject = server.eval("@SOBJECT(sthpw/pipeline['code', '{0}'])".format(code))[0]

        return jsonify({'pipeline': pipeline_sobject})


class ComponentPipelines(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        pipeline_sobjects = server.eval("@SOBJECT(sthpw/pipeline['search_type', 'twog/component'])")

        return jsonify({'pipelines': pipeline_sobjects})


class FileFlowByOrderCode(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        file_flow_sobjects = server.eval("@SOBJECT(twog/file_flow['order_code', '{0}'])".format(code))

        file_flow_json_data = {'file_flows': file_flow_sobjects}

        # Only search for connections of the file flows exist
        if len(file_flow_sobjects) > 0:
            file_flow_codes = [file_flow_sobject.get('code') for file_flow_sobject in file_flow_sobjects]
            file_flow_codes_string = '|'.join(file_flow_codes)
            print(file_flow_codes_string)

            file_flow_to_component_sobjects = server.eval(
                "@SOBJECT(twog/file_flow_to_component['file_flow_code', 'in', '{0}'])".format(file_flow_codes_string))
            file_flow_to_package_sobjects = server.eval(
                "@SOBJECT(twog/file_flow_to_package['file_flow_code', 'in', '{0}'])".format(file_flow_codes_string))

            file_flow_json_data['file_flow_to_components'] = file_flow_to_component_sobjects
            file_flow_json_data['file_flow_to_packages'] = file_flow_to_package_sobjects
        else:
            file_flow_json_data['file_flow_to_components'] = []
            file_flow_json_data['file_flow_to_packages'] = []

        return jsonify(file_flow_json_data)


class FileFlow(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_flow = json_data.get('file_flow')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        server.insert('twog/file_flow', file_flow)

        return jsonify({'status': 200})


class FileFlowToComponent(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_flow_to_component = json_data.get('file_flow_to_component')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        server.insert('twog/file_flow_to_component', file_flow_to_component)

        return jsonify({'status': 200})


class FileFlowToComponentWithCode(Resource):
    def delete(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_key = server.build_search_key('twog/file_flow_to_component', code, project_code='twog')

        server.delete_sobject(search_key)

        return jsonify({'status': 200})


class FileFlowToPackage(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_flow_to_package = json_data.get('file_flow_to_package')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        server.insert('twog/file_flow_to_package', file_flow_to_package)

        return jsonify({'status': 200})


class FileFlowToPackageWithCode(Resource):
    def delete(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_key = server.build_search_key('twog/file_flow_to_package', code, project_code='twog')

        server.delete_sobject(search_key)

        return jsonify({'status': 200})


class DepartmentRequests(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        department_requests = server.eval("@SOBJECT(twog/department_request['status', '!=', 'complete']['@ORDER_BY', 'due_date asc'])")

        if len(department_requests) > 0:
            add_tasks_to_department_request_dictionary(server, department_requests)

        return jsonify({'department_requests': department_requests})


class DepartmentRequestsByDepartment(Resource):
    def get(self, department):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        department_requests = server.eval(
            "@SOBJECT(twog/department_request['assigned_department', '{0}']['status', 'in_progress']['@ORDER_BY', 'due_date asc'])".format(department)
        )

        if len(department_requests) > 0:
            add_tasks_to_department_request_dictionary(server, department_requests)

        return jsonify({'department_requests': department_requests})


class DepartmentRequestsByUser(Resource):
    def get(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        department_requests = server.eval(
            "@SOBJECT(twog/department_request['login', '{0}']['status', '!=', 'complete']['@ORDER_BY', 'due_date asc'])".format(user)
        )

        if len(department_requests) > 0:
            add_tasks_to_department_request_dictionary(server, department_requests)

        return jsonify({'department_requests': department_requests})


class DepartmentRequestsByCode(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        department_request = server.get_by_code('twog/department_request', code)

        if department_request:
            add_tasks_to_department_request_dictionary(server, [department_request])

        return jsonify({'department_request': department_request})

    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        department_request = json_data.get('department_request')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the search key, response (if any), and status (if any)
        search_key = department_request.get('search_key')
        response = department_request.get('response')
        status = department_request.get('status').strip().lower()

        # Get the twog/department_request sobject (need the code and original response)
        department_request_sobject = server.get_by_search_key(search_key)

        # Only send an update if there is a response. Otherwise, only a task was updated
        if response:
            existing_response = department_request_sobject.get('response')

            # If a response already exists, append the new one to it.
            if existing_response:
                # response = department_request_sobject.get('response') + '\n\n' + response
                response = response + '\n\n' + existing_response

            server.update(search_key, {'response': response})

        # The api accepts a 'status' key, but this should update the task's status, not the request status.
        # Determine which task to update, if any, and then update the task.
        if status:
            if status in ['ready', 'in progress', 'additional information needed', 'complete']:
                # Status should update the Request task
                process_name = 'Request'

                if status == 'ready':
                    updated_task_status = 'Ready'
                elif status == 'in progress':
                    updated_task_status = 'In Progress'
                elif status == 'additional information needed':
                    updated_task_status = 'Additional Info Needed'
                else:
                    updated_task_status = 'Complete'
            else:
                # Status should update the Approval task
                process_name = 'Approval'

                if status == 'rejected':
                    updated_task_status = 'Rejected'
                else:
                    updated_task_status = 'Approved'

            task = server.eval(
                "@SOBJECT(sthpw/task['search_code', '{0}']['process', '{1}'])".format(
                    department_request_sobject.get('code'), process_name))[0]

            server.update(task.get('__search_key__'), {'status': updated_task_status})

        return jsonify({'status': 200})


api.add_resource(DepartmentInstructions, '/department_instructions')
api.add_resource(NewInstructionsTemplate, '/instructions_template')
api.add_resource(InstructionsTemplate, '/instructions_template/<string:instructions_template_id>')
api.add_resource(Clients, '/api/v1/clients')
api.add_resource(Divisions, '/api/v1/divisions/<string:client_code>')
api.add_resource(AllTitles, '/titles/<string:ticket>')
api.add_resource(OrderPriorities, '/orders/priorities')
api.add_resource(Orders, '/api/v1/orders')
api.add_resource(FullOrder, '/api/v1/orders/<string:code>/full')
api.add_resource(TitleAdder, '/api/v1/titles/add')
api.add_resource(Title, '/api/v1/title/name/<string:name>')
api.add_resource(Titles, '/api/v1/titles')
api.add_resource(ComponentsInOrder, '/api/v1/orders/<string:code>/components')
api.add_resource(Languages, '/api/v1/languages')
api.add_resource(DepartmentInstructionsAdder, '/api/v1/instructions/department/add')
api.add_resource(Pipeline, '/api/v1/pipelines/code/<string:code>')
api.add_resource(ComponentPipelines, '/api/v1/pipelines/component')
api.add_resource(FileFlow, '/api/v1/file-flows')
api.add_resource(FileFlowByOrderCode, '/api/v1/orders/<string:code>/file-flows')
api.add_resource(FileFlowToComponent, '/api/v1/file-flow-to-component')
api.add_resource(FileFlowToComponentWithCode, '/api/v1/file-flow-to-component/<string:code>')
api.add_resource(FileFlowToPackage, '/api/v1/file-flow-to-package')
api.add_resource(FileFlowToPackageWithCode, '/api/v1/file-flow-to-package/<string:code>')
api.add_resource(DepartmentRequests, '/api/v1/department-requests')
api.add_resource(DepartmentRequestsByUser, '/api/v1/department-requests/user/<string:user>')
api.add_resource(DepartmentRequestsByCode, '/api/v1/department-requests/code/<string:code>')
api.add_resource(DepartmentRequestsByDepartment, '/api/v1/department-requests/<string:department>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
