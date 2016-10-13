from tactic_client_lib import TacticServerStub

from pyasm.search import Search

from common_tools.utils import get_order_sobject_from_task_sobject


def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    if not server:
        server = TacticServerStub.get()

    task_sobject = input_data.get('sobject')

    task_search = Search('sthpw/task')
    task_search.add_code_filter(task_sobject.get('code'))
    task_sobject = task_search.get_sobject()

    if task_sobject and task_sobject.get('search_type') == u'twog/component?project=twog':
        order_sobject = get_order_sobject_from_task_sobject(task_sobject)

        task_priority = order_sobject.get('priority')

        if task_priority:
            search_key = server.build_search_key('sthpw/task', task_sobject.get_code(), project_code='twog')

            server.update(search_key, {'priority': task_priority})


if __name__ == '__main__':
    main()
