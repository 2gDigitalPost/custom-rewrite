from pyasm.search import Search

from common_tools.utils import get_task_sobjects_from_component_sobject


def main(server=None, trigger_input=None):
    """
    :param server: the TacticServerStub object
    :param trigger_input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not trigger_input:
        trigger_input = {}

    # Get the task
    task_sobject = trigger_input.get('sobject')

    # Only proceed if the task exists and is attached to a twog/component sobject
    if not (task_sobject and task_sobject.get('search_type') == u'twog/component?project=twog'):
        return

    component_search_code = task_sobject.get('search_code')

    component_search = Search('twog/component')
    component_search.add_code_filter(component_search_code)
    component = component_search.get_sobject()

    task_status = task_sobject.get('status')

    # If the task is marked as complete, check if the component needs to be set to complete as well (only happens if
    # all other tasks on that component are marked as complete)
    if task_status.lower() == 'complete':
        tasks = get_task_sobjects_from_component_sobject(component)

        for task in tasks:
            if task.get('status') != 'Complete':
                return
        else:
            server.update(component.get_search_key(), {'status': 'complete'})
    elif task_status.lower() == 'in progress':
        if component.get('status').lower() != 'in_progress':
            server.update(component.get_search_key(), {'status': 'in_progress'})


if __name__ == '__main__':
    main()
