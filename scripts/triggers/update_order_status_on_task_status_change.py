from common_tools.utils import get_sobject_by_code, get_order_sobject_from_task_sobject,\
    get_all_tasks_from_order_sobject


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

    order_sobject = get_order_sobject_from_task_sobject(task_sobject)
    order_status = order_sobject.get('status').lower()
    task_status = task_sobject.get('status').lower()

    if task_status == 'in progress':
        if order_status != 'in_progress':
            # Build the order search key
            order_search_key = server.build_search_key('twog/order', order_sobject.get('code'), project_code='twog')

            # Send the update data to the server
            server.update(order_search_key, {'status': 'in_progress'})
    elif task_status == 'complete':
        # Get all the tasks attached to the parent order
        all_order_tasks = get_all_tasks_from_order_sobject(order_sobject)

        # If even one of the tasks is not set to 'complete', return.
        for order_task in all_order_tasks:
            if order_task.get('status').lower() != 'complete':
                return
        else:
            # Build the order search key
            order_search_key = server.build_search_key('twog/order', order_sobject.get('code'), project_code='twog')

            # Send the update data to the server
            server.update(order_search_key, {'status': 'complete'})
