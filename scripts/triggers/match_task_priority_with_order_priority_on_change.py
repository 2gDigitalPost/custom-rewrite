from tactic_client_lib import TacticServerStub

from pyasm.search import Search

from common_tools.utils import get_task_sobjects_from_component_sobject


def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    if not server:
        server = TacticServerStub.get()

    input_sobject = input_data.get('sobject')

    order_code = input_sobject.get('code')
    priority = input_sobject.get('priority')

    component_search = Search('twog/component')
    component_search.add_filter('order_code', order_code)
    component_sobjects = component_search.get_sobjects()

    for component_sobject in component_sobjects:
        tasks = get_task_sobjects_from_component_sobject(component_sobject)

        data_to_insert = {}

        for task in tasks:
            task_search_key = server.build_search_key('sthpw/task', task.get_code(), project_code='twog')

            data_to_insert[task_search_key] = {'priority': priority}

        server.update_multiple(data_to_insert)

if __name__ == '__main__':
    main()
