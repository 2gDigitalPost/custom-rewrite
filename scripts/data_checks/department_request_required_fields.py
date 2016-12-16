from pyasm.command import Trigger
from pyasm.common import Environment, TacticException
from pyasm.search import Search


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


def request_task_marked_complete_data_check(server=None, input_data=None):
    request_task_sobject = input_data.get('sobject')

    request_task_status = request_task_sobject.get('status')

    # This function only applies if the task is marked as 'Complete'
    if request_task_status != 'Complete':
        return

    if not request_task_sobject.get('response'):
        raise TacticException("A 'Response' is required.")


class RequestTaskMarkedCompleteTrigger(Trigger):
    def execute(self):
        # Get the task sobject (in this case, should be attached to twog/department_request)
        task_sobject = self.input.get('sobject')

        # Do a sanity check on the search_type to make sure we're working with a twog/department_request
        search_type = task_sobject.get('search_type')

        if search_type != u'twog/department_request?project=twog':
            raise TacticException("Something went wrong. A trigger was called on a task that it should not have been."
                                  "Trigger Name: {0}".format(self.__class__.__name__))

        # Get the twog/department_request sobject
        search_code = task_sobject.get('search_code')
        department_request_search = Search('twog/department_request')
        department_request_search.add_code_filter(search_code)
        department_request_sobject = department_request_search.get_sobject()

        # Check if the department request has its 'Response' column filled out. If not, raise an error
        if not department_request_sobject.get('response'):
            raise TacticException("Before marking the request as 'Complete', you must fill out the 'Response' column.")
