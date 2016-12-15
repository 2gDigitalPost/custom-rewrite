from tactic_client_lib import TacticServerStub

from pyasm.command import Trigger


class UpdateDepartmentRequestApproval(Trigger):
    def execute(self):
        # Get the sobject that the task is attached to (in this case, should be twog/department_request)
        sobject = self.input.get('sobject')

        # Get the code of the sobject
        search_code = sobject.get('search_code')

        if search_code:
            # Get a server instance
            server = TacticServerStub.get()

            # Build a search key using the code
            search_key = server.build_search_key('twog/department_request', search_code, project_code='twog')

            # Update the twog/department_request to be approved
            server.update(search_key, data={'approved': True})
