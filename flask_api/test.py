from flask import Flask, jsonify, render_template, request, redirect, flash, url_for, session
from flask_restful import reqparse, Resource, Api

import os, sys, inspect

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

sys.path.append(config.get('tacticpath', 'path'))

from tactic_client_lib import TacticServerStub

sys.path.append('/opt/spt/custom')

app = Flask(__name__)
api = Api(app)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.secret_key = SECRET_KEY


# Get credentials from config file
# user = config.get('credentials', 'user')
# password = config.get('credentials', 'password')
project = config.get('credentials', 'project')

# Just get the dev server URL for now
url = config.get('server', 'dev')

parser = reqparse.RequestParser()


from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class EmailPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


ALL_USERS = {}

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = EmailPasswordForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        server = TacticServerStub(server=url, project=project, user=username, password=password)
        ticket = server.get_ticket(username, password)

        session['ticket'] = ticket

        ALL_USERS[ticket] = username

        user = User(username, ticket)
        login_user(user, remember=False)

        return redirect('/')
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


@login_manager.user_loader
def user_loader(user_id):
    try:
        username = ALL_USERS[user_id]
    except KeyError:
        return None

    user = User(username, user_id)

    return user


@app.route('/instructions_template_builder')
def hello():
    return render_template('instructions_template_builder.html')


@app.route('/files_select')
def files_select():
    return render_template('files_select.html')


@app.route('/orders/create')
def order_creator():
    ticket = session.get('ticket')

    if ticket:
        return render_template('order_creator.html')
    else:
        return redirect('/login')


@app.route('/orders/reprioritizer')
def order_reprioritizer():
    ticket = session.get('ticket')

    if ticket:
        return render_template('order_reprioritizer.html')
    else:
        return redirect('/login')


@app.route('/')
def index():
    ticket = session.get('ticket')

    if ticket:
        return render_template('index.html', ticket=session['ticket'])
    else:
        return redirect('/login')


@app.route('/titles/add')
def title_adder():
    ticket = session.get('ticket')

    if ticket:
        return render_template('title_adder.html', ticket=ticket)
    else:
        return redirect('/login')


@app.route('/instructions/department/add')
def department_instructions_adder():
    ticket = session.get('ticket')

    if ticket:
        return render_template('add_department_instructions.html', ticket=ticket)
    else:
        return redirect('/login')


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

    def post(self):
        args = parser.parse_args()

        print(args)


class Clients(Resource):
    def get(self):
        ticket = session.get('ticket')
        server = TacticServerStub(server=url, project=project, ticket=ticket)

        client_sobjects = server.eval("@SOBJECT(twog/client)")

        return jsonify({'clients': client_sobjects})


class Divisions(Resource):
    def get(self, client_code):
        ticket = session.get('ticket')
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


class Orders(Resource):
    def post(self):
        ticket = session.get('ticket')
        server = TacticServerStub(server=url, project=project, ticket=ticket)

        json_data = request.get_json()

        print(json_data)

        return {'status': 200}

        server.insert('twog/order', json_data)


class TitleAdder(Resource):
    def post(self):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        json_data = request.get_json()

        imdb_id = json_data.get('imdb_id')

        existing_title = server.eval("@SOBJECT(twog/title['imdb_id', '{0}'])".format(imdb_id))

        if existing_title:
            pass
        else:
            server.insert('twog/title', json_data)

        return {'status': 200}


class DepartmentInstructionsAdder(Resource):
    def post(self):
        ticket = session.get('ticket')

        server = TacticServerStub(server=url, project=project, ticket=ticket)

        json_data = request.get_json()

        server.insert('twog/department_instructions', json_data)

        return {'status': 200}


api.add_resource(DepartmentInstructions, '/department_instructions')
api.add_resource(NewInstructionsTemplate, '/instructions_template')
api.add_resource(InstructionsTemplate, '/instructions_template/<string:instructions_template_id>')
api.add_resource(Clients, '/api/v1/clients')
api.add_resource(Divisions, '/api/v1/divisions/<string:client_code>')
api.add_resource(AllTitles, '/titles/<string:ticket>')
api.add_resource(OrderPriorities, '/orders/priorities')
api.add_resource(Orders, '/api/v1/orders/add')
api.add_resource(TitleAdder, '/api/v1/titles/add')
api.add_resource(DepartmentInstructionsAdder, '/api/v1/instructions/department/add')

if __name__ == '__main__':
    global ALL_USERS

    app.run(debug=True, host='0.0.0.0')

