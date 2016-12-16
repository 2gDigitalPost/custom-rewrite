from pyasm.common import Environment, TacticException


def insert_data_check(server=None, input_data=None):
    department_request_sobject = input_data.get('sobject')

    if not department_request_sobject.get('name'):
        raise TacticException("Name field is required.")

    if not department_request_sobject.get('due_date'):
        raise TacticException("Due Date field is required.")

    if not department_request_sobject.get('description'):
        raise TacticException("Description field is required.")

    # If 'login' is not in the inserted sobject, insert it using the logged in user's name
    if not department_request_sobject.get('login'):
        login = Environment.get_security().get_login().get_login()

        server.update(department_request_sobject.get('__search_key__'), {'login': login})
