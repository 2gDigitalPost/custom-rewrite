from tactic_client_lib import TacticServerStub

from pyasm.command import Trigger
from pyasm.common import TacticException
from pyasm.search import Search


class HandleDepartmentRequestTaskStatusUpdate(Trigger):
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

        # Task process should be either 'Request' or 'Approval'
        task_process = task_sobject.get('process').lower()
        # For this trigger, only 'Complete', 'Rejected', and 'Approved' apply
        task_status = task_sobject.get('status').lower()
        # Get a server instance to send the data
        server = TacticServerStub.get()

        if task_process == 'request' and task_status == 'complete':
            # Check if the department request has its 'Response' column filled out. If not, raise an error
            if not department_request_sobject.get('response'):
                raise TacticException("Before marking the request as 'Complete', you must fill out the 'Response'"
                                      "column.")

            # Mark the twog/department_request status as needing approval
            server.update(department_request_sobject.get_search_key(), data={'status': 'approval'})
        elif task_process == 'approval':
            if task_status == 'rejected':
                # Need to set the twog/department_request status back to 'in_progress' so that it appears on the
                # department's list again. Setting the task status to 'Revise' is not handled here (the pipeline
                # takes care of that).
                server.update(department_request_sobject.get_search_key(), data={'status': 'in_progress'})
            elif task_status == 'approved':
                # If the Approval task is marked as 'approved', then the request is finished. Mark the
                # twog/department_request status as 'complete' so it disappears from all views.
                server.update(department_request_sobject.get_search_key(), data={'status': 'complete'})
