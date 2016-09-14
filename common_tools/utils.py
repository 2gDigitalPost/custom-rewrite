from pyasm.search import Search


def get_task_data_sobject_from_task_code(task_code):
    """
    Given a task code, find the task_data sobject associated with it

    :param task_code: Unique ID for a task
    :return: task_data sobject
    """

    task_data_search = Search('twog/task_data')
    task_data_search.add_filter('task_code', task_code)
    task_data = task_data_search.get_sobject()

    if task_data:
        return task_data
    else:
        return None