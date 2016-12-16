from pyasm.common import Environment, TacticException


def insert_data_check(server=None, input_data=None):
    department_request_sobject = input_data.get('sobject')

    if not department_request_sobject.get('name'):
        raise TacticException("Name field is required.")

    if not department_request_sobject.get('due_date'):
        raise TacticException("Due Date field is required.")

    if not department_request_sobject.get('description'):
        raise TacticException("Description field is required.")

    # If 'status' is not set, set it to 'in_progress' by default
    if not department_request_sobject.get('status'):
        status = 'in_progress'
    else:
        status = None

    # If 'login' is not in the inserted sobject, insert it using the logged in user's name
    if not department_request_sobject.get('login'):
        login = Environment.get_security().get_login().get_login()
    else:
        login = None

    # If either status or login was set, and update is needed
    if status or login:
        update_dictionary = {}

        if status:
            update_dictionary['status'] = status
        if login:
            update_dictionary['login'] = login

        # Send the update data
        server.update(department_request_sobject.get('__search_key__'), update_dictionary)
