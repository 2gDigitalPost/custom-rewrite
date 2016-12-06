from common_tools.utils import get_sobject_by_code, get_pipeline_xml, get_next_tasks_processes_from_xml,\
    get_task_sobject_from_xml_and_process


def main(server=None, input_data=None):
    if not input_data:
        return

    # The input for the script should be a sthpw/task sobject
    task_input = input_data.get('sobject')

    # Get the actual task sobject rather than the script input (needed for get_order_sobject_from_task_sobject function)
    task_sobject = get_sobject_by_code('sthpw/task', task_input.get('code'))

    # This script only applies to tasks that are to twog/component or twog/package sobjects
    if task_sobject.get('search_type') not in [u'twog/component?project=twog', u'twog/package?project=twog']:
        return

    task_status = task_sobject.get('status').lower()

    if task_status != 'complete':
        return

    pipeline_code = task_sobject.get_parent().get('pipeline_code')

    pipeline_xml = get_pipeline_xml(pipeline_code)

    next_task_processes = get_next_tasks_processes_from_xml(pipeline_xml, task_sobject.get('process'))

    if next_task_processes:
        for process in next_task_processes:
            next_task_sobject = get_task_sobject_from_xml_and_process(pipeline_xml, process,
                                                                      task_sobject.get('search_code'))

            if next_task_sobject:
                search_key = next_task_sobject.get_search_key()

                server.update(search_key, {'status': 'Ready'})
