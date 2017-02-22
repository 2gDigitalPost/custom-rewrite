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


class InstructionsTemplates(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        instructions_template_sobjects = server.eval("@SOBJECT(twog/instructions_template)")

        return jsonify({'instructions_templates': instructions_template_sobjects})

    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')
        instructions_text = json_data.get('instructions_text')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        created_instructions_template = server.insert('twog/instructions_template',
                                                      {'name': name, 'instructions_text': instructions_text})

        return jsonify({'code': created_instructions_template.get('code')})


class InstructionsDocument(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        instructions_sobject = server.get_by_code('twog/instructions', code)

        # Also include any components that reference this document
        attached_components = server.eval("@SOBJECT(twog/component['instructions_code', '{0}'])".format(
            instructions_sobject.get('code')))
        instructions_sobject['components'] = attached_components

        return jsonify({'instructions': instructions_sobject})

    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        name = json_data.get('name')
        instructions_text = json_data.get('instructions_text')

        instructions_sobject = server.get_by_code('twog/instructions', code)

        server.update(instructions_sobject.get('__search_key__'), {'name': name,
                                                                   'instructions_text': instructions_text})

        return jsonify({'instructions': instructions_sobject})


class NewInstructionsForMultipleComponents(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        name = json_data.get('name')
        instructions_text = json_data.get('instructions_text')
        component_codes = json_data.get('component_codes')

        created_instructions_document = server.insert('twog/instructions',
                                                      {'name': name, 'instructions_text': instructions_text})

        update_data = {}

        for component_code in component_codes:
            search_key = server.build_search_key('twog/component', component_code, project_code='twog')
            update_data[search_key] = {'instructions_code': created_instructions_document.get('code')}

        server.update_multiple(update_data)

        return jsonify({'new_instructions_code': created_instructions_document.get('code')})


class InstructionsTemplate(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        instructions_template_sobject = server.get_by_code('twog/instructions_template', code)

        return jsonify({'instructions_template': instructions_template_sobject})

    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        name = json_data.get('name')
        instructions_text = json_data.get('instructions_text')

        instructions_template_sobject = server.get_by_code('twog/instructions_template', code)

        server.update(instructions_template_sobject.get('__search_key__'), {'name': name,
                                                                            'instructions_text': instructions_text})

        return jsonify({'instructions_template': instructions_template_sobject})


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
        order_sobject = server.get_by_code('twog/order', code)

        # Get the division sobject
        division_sobject = server.get_by_code('twog/division', order_sobject.get('division_code'))

        # Also get the image associated with the division, if there is one
        division_image_sobjects = server.eval("@SOBJECT(sthpw/file['search_code', '{0}'])".format(division_sobject.get('code')))

        if division_image_sobjects:
            division_image = division_image_sobjects[-1].get('file_name')
        else:
            division_image = None

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

        component_tasks = server.eval("@SOBJECT(sthpw/task['search_code', 'in', '{0}'])".format(component_codes_string))

        tasks_dict = {}

        for task in component_tasks:
            task_search_code = task.get('search_code')

            if task_search_code in tasks_dict:
                tasks_dict[task_search_code].append(task)
            else:
                tasks_dict[task_search_code] = [task]

        # Get all the files associated with this order, if any
        # Start by getting the file to order connection objects
        file_to_order_sobjects = server.eval("@SOBJECT(twog/file_in_order['order_code', '{0}'])".format(
            order_sobject.get('code')))

        # Get a list of the file codes in string format
        file_codes = [file_to_order_sobject.get('file_code') for file_to_order_sobject in file_to_order_sobjects]
        file_codes_string = '|'.join(file_codes)

        # Get the actual file sobjects
        file_sobjects = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(file_codes_string))

        # Get the file flows from the components
        file_flows = server.eval("@SOBJECT(twog/file_flow['component_code', 'in', '{0}'])".format(component_codes_string))
        file_flow_codes = [file_flow.get('code') for file_flow in file_flows]
        file_flow_codes_string = '|'.join(file_flow_codes)

        # Get the actual file objects attached to the file flows, if they exist
        file_codes_in_file_flows = [file_flow.get('file_code') for file_flow in file_flows]
        file_codes_in_file_flows_string = '|'.join(file_codes_in_file_flows)

        file_sobjects_in_file_flows = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(file_codes_in_file_flows_string))

        file_sobject_in_file_flows_by_code = {}

        for file_sobjects_in_file_flow in file_sobjects_in_file_flows:
            if file_sobjects_in_file_flow.get('code') not in file_sobject_in_file_flows_by_code:
                file_sobject_in_file_flows_by_code[file_sobjects_in_file_flow.get('code')] = file_sobjects_in_file_flow

        for file_flow in file_flows:
            file_sobject = file_sobject_in_file_flows_by_code.get(file_flow.get('file_code'))
            file_flow['file_object'] = file_sobject

        file_flow_to_package_sobjects = server.eval("@SOBJECT(twog/file_flow_to_package['file_flow_code', 'in', '{0}'])".format(file_flow_codes_string))

        file_flows_to_package_dict = {}

        for file_flow_to_package_sobject in file_flow_to_package_sobjects:
            file_flow_code = file_flow_to_package_sobject.get('file_flow_code')

            if file_flow_code in file_flows_to_package_dict:
                file_flows_to_package_dict[file_flow_code].append(file_flow_to_package_sobject)
            else:
                file_flows_to_package_dict[file_flow_code] = [file_flow_to_package_sobject]

        # Get all the packages associated with the order
        package_sobjects = server.eval("@SOBJECT(twog/package['order_code', '{0}'])".format(code))

        package_codes_string = '|'.join([package.get('code') for package in package_sobjects])
        package_tasks = server.eval("@SOBJECT(sthpw/task['search_code', 'in', '{0}'])".format(package_codes_string))

        package_tasks_dict = {}

        for task in package_tasks:
            task_search_code = task.get('search_code')

            if task_search_code in package_tasks_dict:
                package_tasks_dict[task_search_code].append(task)
            else:
                package_tasks_dict[task_search_code] = [task]

        # Get all the extra data needed for the package objects, including the platform and connection status
        for package_sobject in package_sobjects:
            # Get the platform object and add it to the package dictionary
            platform_sobject = server.get_by_code('twog/platform', package_sobject.get('platform_code'))
            package_sobject['platform'] = platform_sobject

            # Get the platform connection sobject and add it to the package dictionary
            platform_connection_sobject = server.eval("@SOBJECT(twog/platform_connection['platform_code', '{0}']['division_code', '{1}'])".format(package_sobject.get('platform_code'), order_sobject.get('division_code')))[0]
            package_sobject['platform_connection'] = platform_connection_sobject

            # Also get the image associated with the platform, if there is one
            platform_image_sobjects = server.eval(
                "@SOBJECT(sthpw/file['search_code', '{0}'])".format(platform_sobject.get('code')))

            if platform_image_sobjects:
                platform_image = platform_image_sobjects[-1].get('file_name')
            else:
                platform_image = None

            package_sobject['platform_image'] = platform_image

            # Get the tasks assigned to the component, if any (sorted by code)
            tasks_list = package_tasks_dict.get(package_sobject.get('code'))

            package_sobject['tasks'] = tasks_list

        # Get the package names sorted by package code
        package_code_to_package_dict = {}

        for package_sobject in package_sobjects:
            package_code_to_package_dict[package_sobject.get('code')] = package_sobject

        for file_flow in file_flows:
            file_flow['delivering_to'] = []

            if file_flow.get('code') in file_flows_to_package_dict:
                packages_delivering_to = file_flows_to_package_dict.get(file_flow.get('code'))

                for package_delivering_to in packages_delivering_to:
                    file_flow['delivering_to'].append(package_code_to_package_dict.get(package_delivering_to.get('package_code')))

        # Get all the details of all the components
        for component_sobject in component_sobjects:
            component_sobject_full = {'code': component_sobject.get('code'), 'component': component_sobject}

            # A component may or may not have a title associated with it
            if component_sobject.get('title_code'):
                component_sobject_full['title'] = titles_dict.get(component_sobject.get('title_code'))
            else:
                component_sobject_full['title'] = None

            # Get the tasks assigned to the component, if any (sorted by code)
            tasks_list = tasks_dict.get(component_sobject.get('code'))

            # Only sort the list if it exists
            if tasks_list:
                component_sobject_full['tasks'] = sorted(tasks_list, key=lambda task: task.get('code'))
            else:
                component_sobject_full['tasks'] = []

            component_sobject_full['file_flows'] = []

            for file_flow in file_flows:
                if file_flow.get('component_code') == component_sobject.get('code'):
                    component_sobject_full['file_flows'].append(file_flow)

            component_sobjects_full.append(component_sobject_full)

        # Finally, return the full order object in all its glory
        return jsonify({'order': order_sobject, 'division': division_sobject, 'division_image': division_image,
                        'components': component_sobjects, 'packages': package_sobjects,
                        'components_full': component_sobjects_full,
                        'file_flows_to_packages': file_flows_to_package_dict,
                        'files': file_sobjects})


class Orders(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        order_sobjects = server.eval("@SOBJECT(twog/order)")

        # Get the division sobject for each order.
        # Start by getting a list of all the division codes
        division_codes = [order_sobject.get('division_code') for order_sobject in order_sobjects]

        # Then, get a string of all the codes, separated by the pipe character
        division_codes_string = '|'.join(division_codes)

        # Now query for all the divisions
        division_sobjects = server.eval("@SOBJECT(twog/division['code', 'in', '{0}'])".format(division_codes_string))

        # Create a dictionary of the divisions, with the codes being the keys and the division sobject being the
        # value (allows for easier searching for the next part)
        divisions_dict = {}

        for division_sobject in division_sobjects:
            divisions_dict[division_sobject.get('code')] = division_sobject

        # Now attach the divisions to their orders
        for order_sobject in order_sobjects:
            order_sobject['division'] = divisions_dict.get(order_sobject.get('division_code'))

        # Now get the list of titles for each order
        # Start by getting all the components for each order (from the list of order codes)
        order_codes = [order_sobject.get('code') for order_sobject in order_sobjects]
        order_codes_string = '|'.join(order_codes)

        # Query for the components
        components = server.eval("@SOBJECT(twog/component['order_code', 'in', '{0}'])".format(order_codes_string))

        # Set up a dictionary of order codes to title codes
        order_codes_to_title_codes_dict = {}

        for component in components:
            order_code = component.get('order_code')
            title_code = component.get('title_code')

            if order_code in order_codes_to_title_codes_dict:
                order_codes_to_title_codes_dict[order_code].add(title_code)
            else:
                order_codes_to_title_codes_dict[order_code] = {title_code}

        # Get all the title codes in a set
        title_codes = set()

        for component in components:
            # Do not add an empty title code
            title_code = component.get('title_code')

            if title_code:
                title_codes.add(title_code)

        # Get the actual title sobjects for all the codes
        title_codes_string = '|'.join(title_codes)
        title_sobjects = server.eval("@SOBJECT(twog/title['code', 'in', '{0}'])".format(title_codes_string))

        # Sort the title objects by their codes for faster searching
        title_code_to_title_sobjects_dict = {}

        for title_sobject in title_sobjects:
            title_code = title_sobject.get('code')

            title_code_to_title_sobjects_dict[title_code] = title_sobject

        # Finally, assign each order sobject its appropriate titles
        for order_sobject in order_sobjects:
            order_code = order_sobject.get('code')
            order_title_codes = order_codes_to_title_codes_dict.get(order_code)
            order_sobject['title_sobjects'] = []

            if order_title_codes:
                for order_title_code in order_title_codes:
                    order_sobject['title_sobjects'].append(title_code_to_title_sobjects_dict.get(order_title_code))

        # Return the orders
        return jsonify({'orders': order_sobjects})

    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        order_data = json_data.get('order')

        # Some data can have None set as the value. This does not work when inserting to the database, so remove
        # these keys/values
        cleaned_order_data = {key: value for key, value in order_data.iteritems() if value != None}

        inserted_order = server.insert('twog/order', cleaned_order_data)

        # Only one of the following should be submitted, not both
        new_po_data = json_data.get('new_purchase_order')
        existing_po_data = json_data.get('existing_purchase_order')

        if new_po_data:
            inserted_po = server.insert('twog/purchase_order', new_po_data)

            server.insert('twog/order_to_purchase_order', {'order_code': inserted_order.get('code'),
                                                           'purchase_order_code': inserted_po.get('code')})
        elif existing_po_data:
            server.insert('twog/order_to_purchase_order', {'order_code': inserted_order.get('code'),
                                                           'purchase_order_code': existing_po_data.get('code')})

        return {'status': 200, 'order_code': inserted_order.get('code')}


class Order(Resource):
    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        order_code = json_data.get('order_code')
        update_data = json_data.get('update_data')

        # Fetch the order object from the server
        order = server.get_by_code('twog/order', order_code)

        # Update the order with the received data
        server.update(order.get('__search_key__'), update_data)


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


class TitleExistsByIMDbID(Resource):
    def get(self, imdb_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        existing_title = server.eval("@SOBJECT(twog/title['imdb_id', '{0}'])".format(imdb_id))

        if existing_title:
            return jsonify({'status': 200, 'exists': True})
        else:
            return jsonify({'status': 200, 'exists': False})


class TitlesExistByIMDbID(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)



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


class TitleFromOMDb(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        title_data = json_data.get('title_data')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Some data can have None set as the value. This does not work when inserting to the database, so remove
        # these keys/values
        cleaned_json_data = {key: value for key, value in title_data.iteritems() if value != None}

        imdb_id = title_data.get('imdb_id')
        existing_title = server.eval("@SOBJECT(twog/title['imdb_id', '{0}'])".format(imdb_id))

        if existing_title:
            # HTTP status 409: Conflict
            return {'status': 409}

        inserted_title = server.insert('twog/title', cleaned_json_data)

        return jsonify({'inserted_title': inserted_title})


class ManualTitleEntry(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        title_data = json_data.get('title')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Some data can have None set as the value. This does not work when inserting to the database, so remove
        # these keys/values
        cleaned_json_data = {key: value for key, value in title_data.iteritems() if value != None}

        inserted_title = server.insert('twog/title', cleaned_json_data)

        return jsonify({'inserted_title': inserted_title})


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


class ComponentByCode(Resource):

    def post(self, code):
        json_data = request.get_json()
        component_data = json_data.get('component')
        ticket = json_data.get('token')
        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_key = server.build_search_key('twog/component', code, project_code='twog')

        server.update(search_key, component_data)

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


class FileFlowsByComponentCode(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        file_flows = server.eval("@SOBJECT(twog/file_flow['component_code', '{0}'])".format(code))


        # Get the file flows from the components
        file_flow_codes = [file_flow.get('code') for file_flow in file_flows]
        file_flow_codes_string = '|'.join(file_flow_codes)

        # Get the actual file objects attached to the file flows, if they exist
        file_codes_in_file_flows = [file_flow.get('file_code') for file_flow in file_flows]
        file_codes_in_file_flows_string = '|'.join(file_codes_in_file_flows)

        file_sobjects_in_file_flows = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(file_codes_in_file_flows_string))

        file_sobject_in_file_flows_by_code = {}

        for file_sobjects_in_file_flow in file_sobjects_in_file_flows:
            if file_sobjects_in_file_flow.get('code') not in file_sobject_in_file_flows_by_code:
                file_sobject_in_file_flows_by_code[file_sobjects_in_file_flow.get('code')] = file_sobjects_in_file_flow

        for file_flow in file_flows:
            file_sobject = file_sobject_in_file_flows_by_code.get(file_flow.get('file_code'))
            file_flow['file_object'] = file_sobject

        file_flow_to_package_sobjects = server.eval("@SOBJECT(twog/file_flow_to_package['file_flow_code', 'in', '{0}'])".format(file_flow_codes_string))

        file_flows_to_package_dict = {}

        for file_flow_to_package_sobject in file_flow_to_package_sobjects:
            file_flow_code = file_flow_to_package_sobject.get('file_flow_code')

            if file_flow_code in file_flows_to_package_dict:
                file_flows_to_package_dict[file_flow_code].append(file_flow_to_package_sobject)
            else:
                file_flows_to_package_dict[file_flow_code] = [file_flow_to_package_sobject]

        # Get all the packages associated with the order
        component = server.get_by_code('twog/component', code)
        package_sobjects = server.eval("@SOBJECT(twog/package['order_code', '{0}'])".format(component.get('order_code')))

        # Get the package names sorted by package code
        package_code_to_package_dict = {}

        for package_sobject in package_sobjects:
            package_code_to_package_dict[package_sobject.get('code')] = package_sobject

        for file_flow in file_flows:
            file_flow['delivering_to'] = []

            if file_flow.get('code') in file_flows_to_package_dict:
                packages_delivering_to = file_flows_to_package_dict.get(file_flow.get('code'))

                for package_delivering_to in packages_delivering_to:
                    file_flow['delivering_to'].append(package_code_to_package_dict.get(package_delivering_to.get('package_code')))

        return jsonify({'file_flows': file_flows})


class FileFlow(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_flow = json_data.get('file_flow')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        server.insert('twog/file_flow', file_flow)

        return jsonify({'status': 200})


class FileFlowByCode(Resource):
    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        update_data = json_data.get('update_data')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Need to get the search key to perform the updates
        file_flow_search_key = server.build_search_key('twog/file_flow', code, project_code='twog')

        # Filter the update data
        name = update_data.get('name')
        file_code = update_data.get('file_code')
        new_package_connections = update_data.get('new_package_connections', [])
        deleted_package_connections = update_data.get('deleted_package_connections', [])

        # Name and file code can be updated directly.
        file_flow_update_data = {}

        if name:
            file_flow_update_data['name'] = name
        if file_code:
            file_flow_update_data['file_code'] = file_code

        # Perform the update only if there is data
        if file_flow_update_data:
            server.update(file_flow_search_key, file_flow_update_data)

        # Now perform the updates to the package connections, if they exist
        # Start with inserting any new connections
        new_package_update_data = []

        for new_package_connection in new_package_connections:
            new_package_update_data.append({'file_flow_code': code, 'package_code': new_package_connection})

        if new_package_update_data:
            server.insert_multiple('twog/file_flow_to_package', new_package_update_data)

        # Now delete the package connections that were removed
        deleted_package_update_data = []

        for deleted_package_connection in deleted_package_connections:
            deleted_package_update_data.append({'file_flow_code': code, 'package_code': deleted_package_connection})
            file_flow_package_connection = server.get_unique_sobject('twog/file_flow_to_package',
                                                                     {'file_flow_code': code,
                                                                      'package_code': deleted_package_connection})

            server.delete_sobject(file_flow_package_connection.get('__search_key__'))

        return jsonify({'status': 200})


class FileFlowTemplate(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_flow_template = json_data.get('file_flow_template')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        server.insert('twog/file_flow_template', file_flow_template)

        return jsonify({'status': 200})


class FileFlowTemplateToPackageTemplates(Resource):
    def get(self, file_flow_template_code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        file_flow_to_package_sobjects = server.eval("@SOBJECT(twog/file_flow_template_to_package_template['file_flow_template_code', '{0}'])".format(file_flow_template_code))

        return jsonify({'file_flow_to_package_sobjects': file_flow_to_package_sobjects})

    def post(self, file_flow_template_code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        new_package_connections = json_data.get('new_package_connections')
        deleted_package_connections = json_data.get('deleted_package_connections')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        for new_package_connection in new_package_connections:
            server.insert('twog/file_flow_template_to_package_template',
                          {'file_flow_template_code': file_flow_template_code,
                           'package_template_code': new_package_connection})

        for deleted_package_connection in deleted_package_connections:
            file_flow_template_to_package_template_sobject = server.eval("@SOBJECT(twog/file_flow_template_to_package_template['file_flow_template_code', '{0}']['package_template_code', '{1}'])".format(file_flow_template_code, deleted_package_connection))[0]
            search_key = server.build_search_key('twog/file_flow_template_to_package_template',
                                                 file_flow_template_to_package_template_sobject.get('code'),
                                                 project_code='twog')
            server.delete_sobject(search_key)

        return jsonify({'status': 200})


class FileFlowTemplateByCode(Resource):
    def delete(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_key = server.build_search_key('twog/file_flow_template', code, project_code='twog')

        server.delete_sobject(search_key)

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


class ProjectTemplates(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        project_templates = server.eval('@SOBJECT(twog/project_template)')

        return jsonify({'project_templates': project_templates})

    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        new_project_template = server.insert('twog/project_template', {'name': name})

        return jsonify({'status': 200, 'project_template_code': new_project_template.get('code')})


class ProjectTemplatesFull(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        project_template = server.get_by_code('twog/project_template', code)

        # Get all the associated component_template sobjects
        component_templates = server.eval(
            "@SOBJECT(twog/component_template['project_template_code', '{0}'])".format(code))

        # Get the component template codes in string form
        component_template_codes = [component_template.get('code') for component_template in component_templates]
        component_template_codes_string = '|'.join(component_template_codes)

        # Get the component template pipelines
        # Get a list of the codes to search for, in string format
        component_template_pipeline_codes = [component_template.get('component_pipeline_code')
                                             for component_template in component_templates]
        component_template_pipeline_codes_string = '|'.join(component_template_pipeline_codes)

        # Search for the pipelines
        component_template_pipelines = server.eval("@SOBJECT(sthpw/pipeline['code', 'in', '{0}'])".format(
            component_template_pipeline_codes_string))

        # Sort the pipelines by code
        component_template_pipeline_code_to_object = {}

        for component_template_pipeline in component_template_pipelines:
            component_template_pipeline_code_to_object[component_template_pipeline.get('code')] = component_template_pipeline

        # Add the pipelines to the component templates dictionary
        for component_template in component_templates:
            component_template['pipeline'] = component_template_pipeline_code_to_object.get(
                component_template.get('component_pipeline_code'))

        # Get all the file flow templates belonging to the component templates
        file_flow_templates = server.eval(
            "@SOBJECT(twog/file_flow_template['component_template_code', 'in', '{0}'])".format(
                component_template_codes_string))

        # Now search for the links between the file flow templates and the package templates
        # Start by getting the file flow template codes in string format
        file_flow_template_codes = [file_flow_template.get('code') for file_flow_template in file_flow_templates]
        file_flow_template_codes_string = '|'.join(file_flow_template_codes)

        # Get the connection objects
        file_flow_template_to_package_templates = server.eval(
            "@SOBJECT(twog/file_flow_template_to_package_template['file_flow_template_code', 'in', '{0}'])".format(
                file_flow_template_codes_string))

        # Sort the connection objects by template code to package template code
        file_flow_template_code_to_package_template_code_dict = {}

        for file_flow_template_to_package_template in file_flow_template_to_package_templates:
            file_flow_template_code = file_flow_template_to_package_template.get('file_flow_template_code')
            package_template_code = file_flow_template_to_package_template.get('package_template_code')

            if file_flow_template_code in file_flow_template_code_to_package_template_code_dict:
                file_flow_template_code_to_package_template_code_dict[file_flow_template_code].append(
                    package_template_code)
            else:
                file_flow_template_code_to_package_template_code_dict[file_flow_template_code] = [package_template_code]

        # Add the package template codes to the file flow templates
        for file_flow_template in file_flow_templates:
            file_flow_template['connected_packages'] = file_flow_template_code_to_package_template_code_dict.get(
                file_flow_template.get('code'), [])

        # Put the file flow templates in a dictionary, sorted by the component codes they are attached to
        component_code_to_file_flow_templates_dict = {}

        for file_flow_template in file_flow_templates:
            component_template_code = file_flow_template.get('component_template_code')

            if component_template_code in component_code_to_file_flow_templates_dict:
                component_code_to_file_flow_templates_dict[component_template_code].append(file_flow_template)
            else:
                component_code_to_file_flow_templates_dict[component_template_code] = [file_flow_template]

        # Put the file flow templates in the component templates dictionary
        for component_template in component_templates:
            component_template['file_flow_templates'] = component_code_to_file_flow_templates_dict.get(
                component_template.get('code'))

        # Get the instructions templates for all the component templates
        # Start by getting the list of instructions template codes in string format
        instructions_template_codes = [component_template.get('instructions_template_code')
                                       for component_template in component_templates]
        instructions_template_codes_string = '|'.join(instructions_template_codes)

        # Get the instructions template objects
        instructions_template_sobjects = server.eval(
            "@SOBJECT(twog/instructions_template['code', 'in', '{0}'])".format(instructions_template_codes_string))

        # Sort the instructions templates by their codes
        instructions_template_code_to_object_dict = {}

        for instructions_template_sobject in instructions_template_sobjects:
            instructions_template_code_to_object_dict[instructions_template_sobject.get('code')] = instructions_template_sobject

        # Add the instructions templates to the component templates dictionary
        for component_template in component_templates:
            component_template['instructions_template'] = instructions_template_code_to_object_dict.get(
                component_template.get('instructions_template_code'))

        # Get all the associated package_template sobjects
        package_templates = server.eval("@SOBJECT(twog/package_template['project_template_code', '{0}'])".format(code))

        # Get the package template pipeline codes in string format
        package_template_pipeline_codes = [package_template.get('package_pipeline_code')
                                           for package_template in package_templates]
        package_template_pipeline_codes_string = '|'.join(package_template_pipeline_codes)

        # Get all the pipeline objects for the package templates
        package_template_pipelines = server.eval("@SOBJECT(sthpw/pipeline['code', 'in', '{0}'])".format(
            package_template_pipeline_codes_string))

        # Sort the pipelines by their codes
        pipeline_code_to_objects = {}

        for pipeline in package_template_pipelines:
            pipeline_code_to_objects[pipeline.get('code')] = pipeline

        # Get the platform codes in string format
        platform_codes = [package_template.get('platform_code') for package_template in package_templates]
        platform_codes_string = '|'.join(platform_codes)

        # Get all the platform objects for the package templates
        package_template_platforms = server.eval("@SOBJECT(twog/platform['code', 'in', '{0}'])".format(
            platform_codes_string))

        # Sort the platforms by codes
        platform_code_to_objects = {}

        for platform in package_template_platforms:
            platform_code_to_objects[platform.get('code')] = platform

        # Add the pipeline and package objects to the package templates dictionary
        for package_template in package_templates:
            package_template['pipeline'] = pipeline_code_to_objects.get(package_template.get('package_pipeline_code'))
            package_template['platform'] = platform_code_to_objects.get(package_template.get('platform_code'))

        return jsonify({'project_template': project_template, 'component_templates': component_templates,
                        'package_templates': package_templates})


def create_components_from_component_templates(server, project_template_code, titles, languages, order_code,
                                               split_instructions=False):
    component_template_sobjects = server.eval(
        "@SOBJECT(twog/component_template['project_template_code', '{0}'])".format(project_template_code))

    components_to_create = []
    for component_template_sobject in component_template_sobjects:
        for title in titles:
            if languages:
                for language in languages:
                    component_to_create = {
                        'name': title.get('name') + ' - ' + language.get(
                            'name') + ': ' + component_template_sobject.get('name'),
                        'order_code': order_code,
                        'pipeline_code': component_template_sobject.get('component_pipeline_code'),
                        'title_code': title.get('code'),
                        'component_template_code': component_template_sobject.get('code')
                    }

                    components_to_create.append(component_to_create)
            else:
                component_to_create = {
                    'name': title.get('name') + ': ' + component_template_sobject.get('name'),
                    'order_code': order_code,
                    'pipeline_code': component_template_sobject.get('component_pipeline_code'),
                    'title_code': title.get('code'),
                    'component_template_code': component_template_sobject.get('code')
                }

                components_to_create.append(component_to_create)

    component_results = server.insert_multiple('twog/component', components_to_create)

    for component_result in component_results:
        server.add_initial_tasks(component_result.get('__search_key__'))

    return component_results


class CreateFromProjectTemplate(Resource):
    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        titles = json_data.get('titles')
        languages = json_data.get('languages')
        project_template_code = json_data.get('project_template_code')
        split_instructions = json_data.get('split_instructions')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Fetch the order object that we are creating for
        order_sobject = server.get_by_code('twog/order', code)

        # Get the project template object that was specified
        project_template = server.get_by_code('twog/project_template', project_template_code)

        # Get the component templates contained in the project template
        component_templates = server.eval("@SOBJECT(twog/component_template['project_template_code', '{0}'])".format(
            project_template.get('code')))

        # Get the component codes in string format
        component_template_codes = [component_template.get('code') for component_template in component_templates]
        component_template_codes_string = '|'.join(component_template_codes)

        # Get the instructions template codes in string format
        instructions_template_codes = [component_template.get('instructions_template_code')
                                       for component_template in component_templates]
        instructions_template_codes_string = '|'.join(instructions_template_codes)

        # Get the package templates contained in the project template
        package_templates = server.eval("@SOBJECT(twog/package_template['project_template_code', '{0}'])".format(
            project_template.get('code')))

        # Get all the instructions templates for all the component templates
        instructions_templates = server.eval(
            "@SOBJECT(twog/instructions_template['code', 'in', '{0}'])".format(instructions_template_codes_string))

        # Get the file flow templates for all the component templates
        file_flow_templates = server.eval(
            "@SOBJECT(twog/file_flow_template['component_template_code', 'in', '{0}'])".format(
                component_template_codes_string))

        # Get the file flow template to package template connection objects
        # Start by getting a list of the file flow template codes in string format
        file_flow_template_codes = [file_flow_template.get('code') for file_flow_template in file_flow_templates]
        file_flow_template_codes_string = '|'.join(file_flow_template_codes)

        # Search for all the file flow template to package template connections
        file_flow_template_to_package_template_connections = server.eval(
            "@SOBJECT(twog/file_flow_template_to_package_template['file_flow_template_code', 'in', '{0}'])".format(
                file_flow_template_codes_string))

        # All the data has been gathered, time to start inserting some new entries!
        # Start with the components
        created_components = create_components_from_component_templates(server, project_template_code, titles,
                                                                        languages, order_sobject.get('code'),
                                                                        split_instructions)

        # Get a dictionary that related the component templates to the actual component codes that they created
        component_template_code_to_created_component_codes = {}

        for component in created_components:
            component_template_code = component.get('component_template_code')

            if component_template_code in component_template_code_to_created_component_codes:
                component_template_code_to_created_component_codes[component_template_code].append(component.get('code'))
            else:
                component_template_code_to_created_component_codes[component_template_code] = [component.get('code')]

        # Get a dictionary that related the component templates to the actual components that they created
        component_template_code_to_created_components = {}

        for component in created_components:
            component_template_code = component.get('component_template_code')

            if component_template_code in component_template_code_to_created_components:
                component_template_code_to_created_components[component_template_code].append(component)
            else:
                component_template_code_to_created_components[component_template_code] = [component]

        # Now create the instructions
        instructions_to_create = []

        # Get a dictionary that lists the instructions template code to the instructions template object
        instructions_template_code_to_instructions_template_object = {}

        for instructions_template in instructions_templates:
            instructions_template_code_to_instructions_template_object[instructions_template.get('code')] = instructions_template

        # Also get a dictionary that lists the component template codes to their instructions template code
        component_template_code_to_instructions_template_code = {}

        for component_template in component_templates:
            component_template_code_to_instructions_template_code[component_template.get('code')] = component_template.get('instructions_template_code')

        if split_instructions:
            for created_component in created_components:
                instructions_template_code = component_template_code_to_instructions_template_code.get(
                    created_component.get('component_template_code'))
                instructions_template = instructions_template_code_to_instructions_template_object.get(
                    instructions_template_code)

                instructions_document_to_add = {
                    'name': instructions_template.get('name'),
                    'instructions_text': instructions_template.get('instructions_text'),
                    'instructions_template_code': instructions_template.get('code')
                }

                instructions_to_create.append(instructions_document_to_add)
        else:
            for instructions_template in instructions_templates:
                # Set up the instructions dictionary to be submitted
                instructions_document_to_add = {
                    'name': instructions_template.get('name'),
                    'instructions_text': instructions_template.get('instructions_text'),
                    'instructions_template_code': instructions_template.get('code')
                }

                instructions_to_create.append(instructions_document_to_add)

        # Create the new instructions
        created_instructions = server.insert_multiple('twog/instructions', instructions_to_create)

        components_to_update = {}
        if split_instructions:
            # Sort the created instructions by their template codes
            instructions_template_code_to_created_instructions_code = {}

            for instructions in created_instructions:
                instructions_template_code = instructions.get('instructions_template_code')

                if instructions_template_code in instructions_template_code_to_created_instructions_code:
                    instructions_template_code_to_created_instructions_code[instructions_template_code].append(instructions.get('code'))
                else:
                    instructions_template_code_to_created_instructions_code[instructions_template_code] = [instructions.get('code')]

            for component_template_code, components in component_template_code_to_created_components.items():
                component_instructions_template_code = component_template_code_to_instructions_template_code.get(
                    component_template_code)

                available_instructions_documents = instructions_template_code_to_created_instructions_code.get(
                    component_instructions_template_code)

                for component, instruction_document_code in zip(components, available_instructions_documents):
                    components_to_update[component.get('__search_key__')] = {'instructions_code': instruction_document_code}
        else:
            # Sort the created instructions by their template codes
            instructions_template_code_to_created_instructions_code = {}

            for instructions in created_instructions:
                instructions_template_code_to_created_instructions_code[
                    instructions.get('instructions_template_code')] = instructions.get('code')

            for component in created_components:
                component_template_code = component.get('component_template_code')
                component_instructions_template_code = component_template_code_to_instructions_template_code.get(component_template_code)

                for instructions in created_instructions:
                    instructions_template_code = instructions.get('instructions_template_code')

                    if component_instructions_template_code == instructions_template_code:
                        components_to_update[component.get('__search_key__')] = {
                            'instructions_code': instructions.get('code')}

        server.update_multiple(components_to_update)

        # Now create the file flows
        file_flows_to_create = []

        for file_flow_template in file_flow_templates:
            # Get the parent component codes to relate the file flow to
            component_codes = component_template_code_to_created_component_codes.get(
                file_flow_template.get('component_template_code'))

            for component_code in component_codes:
                # Set up a dictionary to submit
                new_file_flow_data = {
                    'name': file_flow_template.get('name'),
                    'component_code': component_code,
                    'file_flow_template_code': file_flow_template.get('code')
                }

                # Add the entry to the creation list
                file_flows_to_create.append(new_file_flow_data)

        # Submit all the file flows at once
        created_file_flows = server.insert_multiple('twog/file_flow', file_flows_to_create)

        # Now for the packages
        packages_to_create = []
        for package_template in package_templates:
            package_to_create = {
                'name': package_template.get('name'),
                'order_code': order_sobject.get('code'),
                'platform_code': package_template.get('platform_code'),
                'pipeline_code': package_template.get('package_pipeline_code'),
                'package_template_code': package_template.get('code')
            }

            packages_to_create.append(package_to_create)

        created_packages = server.insert_multiple('twog/package', packages_to_create)

        # Attach the initial tasks to the packages
        for package in created_packages:
            server.add_initial_tasks(package.get('__search_key__'))

        # Lastly, create the file flow to package connections
        # We need to relate the file flows to their template codes and the packages to their template codes
        # Create a dictionary for each
        file_flow_template_code_to_created_file_flow_code = {}
        package_template_code_to_created_package_code = {}

        for created_file_flow in created_file_flows:
            file_flow_template_code = created_file_flow.get('file_flow_template_code')

            if file_flow_template_code in file_flow_template_code_to_created_file_flow_code:
                file_flow_template_code_to_created_file_flow_code[file_flow_template_code].append(created_file_flow.get('code'))
            else:
                file_flow_template_code_to_created_file_flow_code[file_flow_template_code] = [created_file_flow.get('code')]

        for created_package in created_packages:
            package_template_code_to_created_package_code[created_package.get('package_template_code')] = created_package.get('code')

        file_flow_to_package_connections_to_create = []

        for file_flow_template_to_package_template_connection in file_flow_template_to_package_template_connections:
            created_file_flow_codes = file_flow_template_code_to_created_file_flow_code.get(file_flow_template_to_package_template_connection.get('file_flow_template_code'))

            for created_file_flow_code in created_file_flow_codes:
                file_flow_to_package_connection_to_create = {
                    'file_flow_code': created_file_flow_code,
                    'package_code': package_template_code_to_created_package_code.get(
                        file_flow_template_to_package_template_connection.get('package_template_code')
                    )
                }

                file_flow_to_package_connections_to_create.append(file_flow_to_package_connection_to_create)

        server.insert_multiple('twog/file_flow_to_package', file_flow_to_package_connections_to_create)

        return jsonify({'order_code': order_sobject.get('code')})


class ComponentTemplates(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        component_templates = server.eval('@SOBJECT(twog/component_template)')

        return jsonify({'component_templates': component_templates})

    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')
        project_template_code = json_data.get('project_template_code')
        component_pipeline_code = json_data.get('component_pipeline_code')
        instructions_template_code = json_data.get('instructions_template_code')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        new_component_template = server.insert('twog/component_template',
                                               {'name': name, 'project_template_code': project_template_code,
                                                'component_pipeline_code': component_pipeline_code,
                                                'instructions_template_code': instructions_template_code})

        return jsonify({'status': 200, 'project_template_code': new_component_template.get('code')})


class ComponentTemplateByCode(Resource):
    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')
        component_pipeline_code = json_data.get('component_pipeline_code')
        instructions_template_code = json_data.get('instructions_template_code')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        existing_component_template = server.get_by_code('twog/component_template', code)

        server.update(existing_component_template.get('__search_key__'), {
            'name': name,
            'component_pipeline_code': component_pipeline_code,
            'instructions_template_code': instructions_template_code
        })

        return jsonify({'status': 200})

    def delete(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_key = server.build_search_key('twog/component_template', code, project_code='twog')

        server.delete_sobject(search_key)

        return jsonify({'status': 200})


class PackageTemplates(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        package_templates = server.eval('@SOBJECT(twog/package_template)')

        return jsonify({'package_templates': package_templates})

    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')
        project_template_code = json_data.get('project_template_code')
        package_pipeline_code = json_data.get('package_pipeline_code')
        platform_code = json_data.get('platform_code')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        new_package_template = server.insert('twog/package_template',
                                             {'name': name, 'project_template_code': project_template_code,
                                              'package_pipeline_code': package_pipeline_code,
                                              'platform_code': platform_code
                                              })

        return jsonify({'status': 200, 'project_template_code': new_package_template.get('code')})


class PackageTemplateByCode(Resource):
    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')
        package_pipeline_code = json_data.get('package_pipeline_code')
        platform_code = json_data.get('platform_code')
        project_template_code = json_data.get('project_template_code')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the existing object
        package_template_sobject = server.get_by_code('twog/package_template', code)

        # Update the existing object
        server.update(package_template_sobject.get('__search_key__'),
                      {'name': name, 'package_pipeline_code': package_pipeline_code, 'platform_code': platform_code,
                       'project_template_code': project_template_code})

        return jsonify({'status': 200})

    def delete(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_key = server.build_search_key('twog/package_template', code, project_code='twog')

        server.delete_sobject(search_key)

        return jsonify({'status': 200})


class Platforms(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        platforms = server.eval('@SOBJECT(twog/platform)')

        return jsonify({'platforms': platforms})


class PipelinesByType(Resource):
    def get(self, type):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        pipelines = server.eval("@SOBJECT(sthpw/pipeline['search_type', 'twog/{0}'])".format(type))

        return jsonify({'pipelines': pipelines})


class Task(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        task = server.get_by_code('sthpw/task', code)

        return jsonify({'task': task})

    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        update_data = json_data.get('update_data')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the existing object
        task_sobject = server.get_by_code('sthpw/task', code)

        # Update the existing object
        server.update(task_sobject.get('__search_key__'), update_data)

        return jsonify({'status': 200})


class Tasks(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_types = ['twog/component?project=twog', 'twog/package?project=twog']
        search_types_string = '|'.join(search_types)

        excluded_statuses = ['Pending', 'Complete']
        excluded_statuses_string = '|'.join(excluded_statuses)

        tasks = server.eval("@SOBJECT(sthpw/task['search_type', 'in', '{0}']['status', 'not in', '{1}'])".format(search_types_string, excluded_statuses_string))

        return jsonify({'tasks': tasks})


class TasksByDepartment(Resource):
    def get(self, department):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_types = ['twog/component?project=twog', 'twog/package?project=twog']
        search_types_string = '|'.join(search_types)

        excluded_statuses = ['Pending', 'Complete']
        excluded_statuses_string = '|'.join(excluded_statuses)

        tasks = server.eval(
            "@SOBJECT(sthpw/task['search_type', 'in', '{0}']['status', 'not in', '{1}'])".format(search_types_string, excluded_statuses_string))

        department_tasks = []

        for task in tasks:
            process = task.get('process')
            process_department = process.split(':')[0].strip().lower()

            if process_department == department:
                department_tasks.append(task)

        return jsonify({'tasks': department_tasks})


class TasksBySubmittedUser(Resource):
    def get(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_types = ['twog/component?project=twog', 'twog/package?project=twog']
        search_types_string = '|'.join(search_types)

        excluded_statuses = ['Pending', 'Complete']
        excluded_statuses_string = '|'.join(excluded_statuses)

        tasks = server.eval("@SOBJECT(sthpw/task['search_type', 'in', '{0}']['status', 'not in', '{1}']['login', '{2}'])".format(search_types_string, excluded_statuses_string, user))

        return jsonify({'tasks': tasks})


class TasksByAssignedUser(Resource):
    def get(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        search_types = ['twog/component?project=twog', 'twog/package?project=twog']
        search_types_string = '|'.join(search_types)

        excluded_statuses = ['Pending', 'Complete']
        excluded_statuses_string = '|'.join(excluded_statuses)

        tasks = server.eval("@SOBJECT(sthpw/task['search_type', 'in', '{0}']['status', 'not in', '{1}']['assigned', '{2}'])".format(search_types_string, excluded_statuses_string, user))

        return jsonify({'tasks': tasks})


def parse_instructions_text_for_task(instructions, task_name):
    instructions_text = instructions.get('instructions_text', 'Sorry, no instructions are available for this task')

    task_instructions_text = ''
    instruction_text_in_task = False

    for line in instructions_text.split('\n'):
        if line:
            if line.startswith('!@|'):
                name = line.split('|')[1].strip()

                if task_name == name:
                    task_instructions_text += name + '\n'
                    instruction_text_in_task = True
                else:
                    instruction_text_in_task = False
            elif instruction_text_in_task:
                task_instructions_text += line + '\n'

    if not task_instructions_text:
        task_instructions_text = 'Sorry, no instructions are available for this task.'

    return task_instructions_text


class TaskFull(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        task = server.get_by_code('sthpw/task', code)

        # Get the task_data object (should exist for tasks created for twog/component and twog/package sobjects)
        task_data = server.get_unique_sobject('twog/task_data', {'task_code': task.get('code')})
        task_data_code = task_data.get('code')

        # Get the parent sobject
        parent = server.get_parent(task.get('__search_key__'))

        # Get the twog/instructions sobject (from the parent)
        instructions = server.get_by_code('twog/instructions', parent.get('instructions_code'))

        # Parse out the instructions text that is relevant to this task
        instructions_text = parse_instructions_text_for_task(instructions, task.get('process'))

        # Get the tasks that come before this task
        input_tasks = server.get_input_tasks(task.get('__search_key__'))

        # Get the tasks that come after this task
        output_tasks = server.get_output_tasks(task.get('__search_key__'))

        # Get the equipment. Start by querying the twog/equipment_in_task_data table
        equipment_in_task_data_sobjects = server.eval(
            "@SOBJECT(twog/equipment_in_task_data['task_data_code', '{0}'])".format(task_data_code))

        # Now query for each equipment entry. Start by getting a list of all the equipment codes
        equipment_codes = [equipment_in_task_data_sobject.get('equipment_code') for equipment_in_task_data_sobject in equipment_in_task_data_sobjects]

        # Put the codes into string format, separated by the pipe character
        equipment_codes_string = '|'.join(equipment_codes)

        # Search for the twog/equipment sobjects
        equipment = server.eval("@SOBJECT(twog/equipment['code', 'in', '{0}'])".format(equipment_codes_string))

        # Get the input files for the task
        # Start by searching the twog/task_data_in_file table for relevant entries
        task_data_input_file_sobjects = server.eval("@SOBJECT(twog/task_data_in_file['task_data_code', '{0}'])".format(
            task_data_code))

        # Get the file codes in string format for faster searching
        input_file_codes = [task_data_input_file_sobject.get('file_code')
                            for task_data_input_file_sobject in task_data_input_file_sobjects]
        input_file_codes_string = '|'.join(input_file_codes)

        # Get all the input files that match the codes string
        input_files = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(input_file_codes_string))

        # Get the output files for the task
        # Start by searching the twog/task_data_out_file table for relevant entries
        task_data_output_file_sobjects = server.eval(
            "@SOBJECT(twog/task_data_out_file['task_data_code', '{0}'])".format(task_data_code))

        # Get the file codes in string format for faster searching
        output_file_codes = [task_data_output_file_sobject.get('file_code')
                             for task_data_output_file_sobject in task_data_output_file_sobjects]
        output_file_codes_string = '|'.join(output_file_codes)

        # Get all the output files that match the codes string
        output_files = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(output_file_codes_string))

        return jsonify({'task': task, 'task_data': task_data, 'parent': parent, 'instructions_text': instructions_text,
                        'input_tasks': input_tasks, 'output_tasks': output_tasks, 'equipment': equipment,
                        'input_files': input_files, 'output_files': output_files})


class TaskStatusOptions(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        task = server.get_by_code('sthpw/task', code)
        processes = server.get_pipeline_processes_info(task.get('__search_key__'))

        return jsonify({'processes': processes['processes']})


class Equipment(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        equipment = server.eval("@SOBJECT(twog/equipment)")

        return jsonify({'equipment': equipment})


class EquipmentInTask(Resource):
    def post(self, task_code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        equipment_codes = json_data.get('equipment_codes', [])

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the twog/task_data object associated with the task code
        # There should be one and only one twog/task_data object associated with one task code
        task_data = server.get_unique_sobject('twog/task_data', {'task_code': task_code})

        # Start by getting the existing equipment in task entries.
        existing_entries = server.eval("@SOBJECT(twog/equipment_in_task_data['task_data_code', '{0}'])".format(
            task_data.get('code')))

        # Compare the submitted codes with the existing entries to get a list of what needs to be added
        entries_to_add = []

        for equipment_code in equipment_codes:
            if equipment_code not in [existing_entry.get('code') for existing_entry in existing_entries]:
                entries_to_add.append({'equipment_code': equipment_code, 'task_data_code': task_data.get('code')})

        # Add the new entries to the twog/equipment_in_task_data table
        server.insert_multiple('twog/equipment_in_task_data', entries_to_add)

        # Compare the existing entries with the equipment codes to get a list of what needs to be removed
        entries_to_delete = []

        for existing_entry in existing_entries:
            existing_entry_code = existing_entry.get('code')

            if existing_entry_code not in equipment_codes:
                entries_to_delete.append(existing_entry)

        # Delete entries that exist but were not included in the submission (the user unselected them)
        for entry_to_delete in entries_to_delete:
            search_key = entry_to_delete.get('__search_key__')

            server.delete_sobject(search_key)

        return jsonify({'status': 200})


class TaskInputFileOptions(Resource):
    def get(self, task_code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the actual sthpw/task sobject
        task = server.get_by_code('sthpw/task', task_code)

        # Get the twog/component sobject
        component = server.get_by_code('twog/component', task.get('search_code'))

        # Get the twog/order sobject
        order = server.get_by_code('twog/order', component.get('order_code'))

        # Get all the relevant twog/file_in_order entries
        files_in_order = server.eval("@SOBJECT(twog/file_in_order['order_code', '{0}'])".format(order.get('code')))

        # Get a list of the file codes for faster searching
        file_codes = [file_in_order.get('file_code') for file_in_order in files_in_order]
        file_codes_string = '|'.join(file_codes)

        # Get the actual twog/file sobjects
        files = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(file_codes_string))

        return jsonify({'files': files})


class TaskInputFiles(Resource):
    def post(self, task_code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_codes = json_data.get('file_codes', [])

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the twog/task_data object associated with the task code
        # There should be one and only one twog/task_data object associated with one task code
        task_data = server.get_unique_sobject('twog/task_data', {'task_code': task_code})

        # Start by getting the existing input file in task entries.
        existing_entries = server.eval("@SOBJECT(twog/task_data_in_file['task_data_code', '{0}'])".format(
            task_data.get('code')))

        # Compare the submitted codes with the existing entries to get a list of what needs to be added
        entries_to_add = []

        for file_code in file_codes:
            if file_code not in [existing_entry.get('code') for existing_entry in existing_entries]:
                entries_to_add.append({'file_code': file_code, 'task_data_code': task_data.get('code')})

        # Add the new entries to the twog/task_data_in_file table
        server.insert_multiple('twog/task_data_in_file', entries_to_add)

        # Compare the existing entries with the file codes to get a list of what needs to be removed
        entries_to_delete = []

        for existing_entry in existing_entries:
            existing_entry_code = existing_entry.get('code')

            if existing_entry_code not in file_codes:
                entries_to_delete.append(existing_entry)

        # Delete entries that exist but were not included in the submission (the user unselected them)
        for entry_to_delete in entries_to_delete:
            search_key = entry_to_delete.get('__search_key__')

            server.delete_sobject(search_key)

        return jsonify({'status': 200})


class TaskOutputFile(Resource):
    def post(self, task_code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        name = json_data.get('name')
        file_path = json_data.get('file_path')
        classification = json_data.get('classification').lower()
        original_file_codes = json_data.get('original_file_codes', [])

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Submit the new twog/file to the server
        new_output_file_data = {
            'name': name,
            'file_path': file_path,
            'classification': classification
        }
        new_output_file = server.insert('twog/file', new_output_file_data)

        # Now make the connections between the new file and the files it came from (if any)
        original_file_to_output_file_data = []

        for original_file_code in original_file_codes:
            original_file_to_output_file_data.append({'origin_file': original_file_code,
                                                      'file_code': new_output_file.get('code')})

        if original_file_to_output_file_data:
            server.insert_multiple('twog/file_to_origin_file', original_file_to_output_file_data)

        # Associate the new output file to the task (twog/task_data_out_file)
        # First, get the twog/task_data object
        task_data = server.get_unique_sobject('twog/task_data', {'task_code': task_code})

        # Insert a link between the new output file and the task_data object
        server.insert('twog/task_data_out_file', {'task_data_code': task_data.get('code'),
                                                  'file_code': new_output_file.get('code')})

        # Also need to associate the file to the order and the division
        # Travel up the chain to get the order. Start by identifying which type the task belongs to
        task_object = server.get_by_code('sthpw/task', task_code)
        search_type = task_object.get('search_type')
        search_code = task_object.get('search_code')

        # Search type includes '?project=twog', don't need that
        search_type = search_type.split('?')[0]

        # Get the parent
        parent_object = server.get_by_code(search_type, search_code)

        # Regardless of if the parent is a component or package, it should have an order code
        # Make the connection between the file and the order
        server.insert('twog/file_in_order', {'file_code': new_output_file.get('code'),
                                             'order_code': parent_object.get('order_code')})

        return jsonify({'status': 200})


class FileObject(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_data = json_data.get('file')
        order_code = json_data.get('order_code')
        origin_file_codes = json_data.get('origin_file_codes', [])

        name = file_data.get('name')
        file_path = file_data.get('file_path')
        classification = file_data.get('classification').lower()
        division_code = file_data.get('division_code')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # If an order code was given and a division code was not, the division can still be found by looking up the
        # order
        if order_code and not division_code:
            order_sobject = server.get_by_code('twog/order', order_code)

            division_code = order_sobject.get('division_code')

        file_data_to_insert = {
            'name': name,
            'file_path': file_path,
            'classification': classification
        }

        if division_code:
            file_data_to_insert['division_code'] = division_code

        # Start by creating the new twog/file sobject
        file_sobject = server.insert('twog/file', file_data_to_insert)

        # Next, link the file to its origin files, if any
        if origin_file_codes:
            data_to_insert = []

            for origin_file_code in origin_file_codes:
                data_to_insert.append({'file_code': file_sobject.get('code'), 'origin_file': origin_file_code})

            server.insert_multiple('twog/file_to_origin_file', data_to_insert)

        # Then, link the file to an order, if an order code was provided
        if order_code:
            server.insert('twog/file_in_order', {'file_code': file_sobject.get('code'), 'order_code': order_code})


        # Return the code of the created file
        return jsonify({'file_code': file_sobject.get('code')})


class FileObjectByCode(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the actual twog/file sobject
        file_object = server.get_by_code('twog/file', code)

        # Also include the origin files
        origin_file_entries = server.eval("@SOBJECT(twog/file_to_origin_file['file_code', '{0}'])".format(
            file_object.get('code')))

        origin_file_codes = [origin_file_entry.get('origin_file') for origin_file_entry in origin_file_entries]
        origin_file_codes_string = '|'.join(origin_file_codes)

        origin_files = server.eval("@SOBJECT(twog/file['code', 'in', '{0}'])".format(origin_file_codes_string))

        file_object['origin_files'] = origin_files

        return jsonify({'file_object': file_object})

    def post(self, code):
        json_data = request.get_json()

        ticket = json_data.get('token')
        file_json = json_data.get('file')
        origin_file_codes = json_data.get('origin_file_codes', [])

        name = file_json.get('name')
        file_path = file_json.get('file_path')
        classification = file_json.get('classification')

        if classification is not None:
            classification = classification.lower()

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the existing object
        existing_output_file = server.get_by_code('twog/file', code)

        # Get the data to submit. Only data that has changed should be submitted
        data_to_submit = {}

        if name and name != existing_output_file.get('name'):
            data_to_submit['name'] = name

        if file_path and file_path != existing_output_file.get('file_path'):
            data_to_submit['file_path'] = file_path

        if classification and classification != existing_output_file.get('classification'):
            data_to_submit['classification'] = classification

        if data_to_submit:
            server.update(existing_output_file.get('__search_key__'), data_to_submit)


        return jsonify({'status': 200})


class FilesByDivision(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        files = server.eval("@SOBJECT(twog/file['division_code', '{0}'])".format(code))

        return jsonify({'files': files})


class FilesInOrder(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        order_code = json_data.get('order_code')
        file_codes = json_data.get('file_codes')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get a list of entries to insert
        entries = []

        for file_code in file_codes:
            entries.append({'order_code': order_code, 'file_code': file_code})

        server.insert_multiple('twog/file_in_order', entries)

        return jsonify({'status': 200})


class RemoveFileInOrder(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        order_code = json_data.get('order_code')
        file_code = json_data.get('file_code')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Find the entry in the twog/file_in_order table
        file_in_order_object = server.get_unique_sobject('twog/file_in_order', {'order_code': order_code,
                                                                                'file_code': file_code})

        # Remove it
        server.delete_sobject(file_in_order_object.get('__search_key__'))

        return jsonify({'status': 200})


class PurchaseOrdersByDivision(Resource):
    def get(self, division_code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        purchase_orders = server.eval("@SOBJECT(twog/purchase_order['division_code', '{0}'])".format(division_code))

        return jsonify({'purchase_orders': purchase_orders})


class PurchaseOrderExists(Resource):
    def get(self, number, division_code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        purchase_orders = server.eval("@SOBJECT(twog/purchase_order['name', '{0}']['division_code', '{1}'])".format(
            number, division_code))

        if purchase_orders:
            purchase_order = purchase_orders[0]
            result_found = True
        else:
            purchase_order = None
            result_found = False

        return jsonify({'purchase_order': purchase_order, 'result_found': result_found})


class EstimatedHours(Resource):
    def post(self):
        json_data = request.get_json()

        ticket = json_data.get('token')
        task_data_code = json_data.get('task_data_code')
        estimated_hours = json_data.get('estimated_hours')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the twog/task_data object and search key
        task_data = server.get_by_code('twog/task_data', task_data_code)
        search_key = task_data.get('__search_key__')

        # Update the task data's estimated hours (cast to float just in case)
        server.update(search_key, {'estimated_hours': float(estimated_hours)})

        return jsonify({'status': 200})


class PackagesInOrder(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        packages = server.eval("@SOBJECT(twog/package['order_code', '{0}'])".format(code))

        return jsonify({'packages': packages})


class PackageWaitingOnFiles(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Start by querying the twog/file_flow_in_package table
        # Only get the entries that have not been completed yet
        file_flow_in_package_objects = server.eval(
            "@SOBJECT(twog/file_flow_to_package['package_code', '{0}'])".format(code))

        # Get the actual twog/file_flow objects
        file_flow_codes = [file_flow_in_package_object.get('file_flow_code')
                           for file_flow_in_package_object in file_flow_in_package_objects if not file_flow_in_package_object.get('complete')]
        file_flow_codes_string = '|'.join(file_flow_codes)

        file_flows = server.eval("@SOBJECT(twog/file_flow['code', 'in', '{0}'])".format(file_flow_codes_string))

        return jsonify({'file_flows': file_flows})


def get_order_from_file_flow_code(server, file_flow_code):
    # Search up the chain to get the Order, then the packages
    # Start by getting the file flow object
    file_flow_object = server.get_by_code('twog/file_flow', file_flow_code)

    # Then, get the component
    component = server.get_by_code('twog/component', file_flow_object.get('component_code'))

    # Now, get the order
    order = server.get_by_code('twog/order', component.get('order_code'))

    return order


class FileFlowPackageOptions(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Search up the chain to get the Order, then the packages
        # Start by getting the file flow object
        file_flow_object = server.get_by_code('twog/file_flow', code)

        # Then, get the component
        component = server.get_by_code('twog/component', file_flow_object.get('component_code'))

        # Now, get the order
        order = server.get_by_code('twog/order', component.get('order_code'))

        # Finally, search for all the packages associated with the order
        packages = server.eval("@SOBJECT(twog/package['order_code', '{0}'])".format(order.get('code')))

        return jsonify({'packages': packages})


class FileFlowDeliverableFileOptions(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the order object
        order = get_order_from_file_flow_code(server, code)

        # Get the twog/file_in_order objects, based on the order code
        file_in_order_objects = server.eval(
            "@SOBJECT(twog/file_in_order['order_code', '{0}'])".format(order.get('code')))

        # Get all the twog/file objects
        file_codes = [file_in_order_object.get('file_code') for file_in_order_object in file_in_order_objects]
        file_codes_string = '|'.join(file_codes)

        # Get all the deliverable files associated with the order
        deliverable_files = server.eval(
            "@SOBJECT(twog/file['code', 'in', '{0}']['classification', 'deliverable'])".format(file_codes_string))

        return jsonify({'files': deliverable_files})


class DeliverableFilesInOrder(Resource):
    def get(self, code):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        ticket = args.get('token')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        # Get the twog/file_in_order objects, based on the order code
        file_in_order_objects = server.eval(
            "@SOBJECT(twog/file_in_order['order_code', '{0}'])".format(code))

        # Get all the twog/file objects
        file_codes = [file_in_order_object.get('file_code') for file_in_order_object in file_in_order_objects]
        file_codes_string = '|'.join(file_codes)

        # Get all the deliverable files associated with the order
        deliverable_files = server.eval(
            "@SOBJECT(twog/file['code', 'in', '{0}']['classification', 'deliverable'])".format(file_codes_string))

        return jsonify({'files': deliverable_files})


api.add_resource(DepartmentInstructions, '/department_instructions')
api.add_resource(NewInstructionsTemplate, '/instructions_template')
api.add_resource(InstructionsTemplate, '/api/v1/instructions-templates/<string:code>')
api.add_resource(InstructionsTemplates, '/api/v1/instructions-templates')
api.add_resource(InstructionsDocument, '/api/v1/instructions/<string:code>')
api.add_resource(NewInstructionsForMultipleComponents, '/api/v1/instructions/components')
api.add_resource(Clients, '/api/v1/clients')
api.add_resource(Divisions, '/api/v1/divisions/<string:client_code>')
api.add_resource(AllTitles, '/titles/<string:ticket>')
api.add_resource(OrderPriorities, '/orders/priorities')
api.add_resource(Orders, '/api/v1/orders')
api.add_resource(FullOrder, '/api/v1/orders/<string:code>/full')
api.add_resource(TitleAdder, '/api/v1/titles/add')
api.add_resource(Title, '/api/v1/title/name/<string:name>')
api.add_resource(Titles, '/api/v1/titles')
api.add_resource(TitleExistsByIMDbID, '/api/v1/titles/imdb/<string:imdb_id>/exists')
api.add_resource(TitlesExistByIMDbID, '/api/v1/titles/imdb/exists')
api.add_resource(TitleFromOMDb, '/api/v1/titles/omdb')
api.add_resource(ManualTitleEntry, '/api/v1/titles/manual')
api.add_resource(Platforms, '/api/v1/platforms')
api.add_resource(ComponentsInOrder, '/api/v1/orders/<string:code>/components')
api.add_resource(ComponentByCode, '/api/v1/components/<string:code>')
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
api.add_resource(FileFlowTemplate, '/api/v1/file-flow-templates')
api.add_resource(FileFlowTemplateByCode, '/api/v1/file-flow-templates/<string:code>')
api.add_resource(FileFlowTemplateToPackageTemplates, '/api/v1/file-flow-templates/<string:file_flow_template_code>/package-templates')
api.add_resource(DepartmentRequests, '/api/v1/department-requests')
api.add_resource(DepartmentRequestsByUser, '/api/v1/department-requests/user/<string:user>')
api.add_resource(DepartmentRequestsByCode, '/api/v1/department-requests/code/<string:code>')
api.add_resource(DepartmentRequestsByDepartment, '/api/v1/department-requests/<string:department>')
api.add_resource(ProjectTemplates, '/api/v1/project-templates')
api.add_resource(ProjectTemplatesFull, '/api/v1/project-templates/<string:code>/full')
api.add_resource(CreateFromProjectTemplate, '/api/v1/orders/<string:code>/create-from-template')
api.add_resource(ComponentTemplates, '/api/v1/component-templates')
api.add_resource(ComponentTemplateByCode, '/api/v1/component-templates/<string:code>')
api.add_resource(PackageTemplates, '/api/v1/package-templates')
api.add_resource(PackageTemplateByCode, '/api/v1/package-templates/<string:code>')
api.add_resource(PipelinesByType, '/api/v1/pipelines/<string:type>')
api.add_resource(Tasks, '/api/v1/tasks')
api.add_resource(TasksByDepartment, '/api/v1/tasks/<string:department>')
api.add_resource(TasksBySubmittedUser, '/api/v1/tasks/user/<string:user>/submitted')
api.add_resource(TasksByAssignedUser, '/api/v1/tasks/user/<string:user>/assigned')
api.add_resource(Task, '/api/v1/task/<string:code>')
api.add_resource(TaskFull, '/api/v1/task/<string:code>/full')
api.add_resource(TaskStatusOptions, '/api/v1/task/<string:code>/status-options')

api.add_resource(DeliverableFilesInOrder, '/api/v1/order/<string:code>/deliverable-files')
api.add_resource(Equipment, '/api/v1/equipment')
api.add_resource(EquipmentInTask, '/api/v1/task/<string:task_code>/equipment')
api.add_resource(EstimatedHours, '/api/v1/estimated-hours')
api.add_resource(FileFlowByCode, '/api/v1/file-flow/<string:code>')
api.add_resource(FileFlowsByComponentCode, '/api/v1/component/<string:code>/file-flows')
api.add_resource(FileFlowPackageOptions, '/api/v1/file-flow/<string:code>/package-options')
api.add_resource(FileFlowDeliverableFileOptions, '/api/v1/file-flow/<string:code>/deliverable-file-options')
api.add_resource(FileObject, '/api/v1/file')
api.add_resource(FileObjectByCode, '/api/v1/file/<string:code>')
api.add_resource(FilesByDivision, '/api/v1/division/<string:code>/files')
api.add_resource(FilesInOrder, '/api/v1/files-in-order')
api.add_resource(Order, '/api/v1/order/<string:code>')
api.add_resource(PackagesInOrder, '/api/v1/order/<string:code>/packages')
api.add_resource(PackageWaitingOnFiles, '/api/v1/package/<string:code>/waiting-files')
api.add_resource(PurchaseOrdersByDivision, '/api/v1/division/<string:division_code>/purchase-orders')
api.add_resource(PurchaseOrderExists,
                 '/api/v1/purchase-order/number/<string:number>/division/<string:division_code>/exists')
api.add_resource(RemoveFileInOrder, '/api/v1/file-in-order/delete')
api.add_resource(TaskInputFileOptions, '/api/v1/task/<string:task_code>/input-file-options')
api.add_resource(TaskInputFiles, '/api/v1/task/<string:task_code>/input-files')
api.add_resource(TaskOutputFile, '/api/v1/task/<string:task_code>/output-file')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
