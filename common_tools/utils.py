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


def get_task_data_equipment(task_data_code):
    """
    Given a task_data code, find all the equipment sobjects currently associated with the task_data entry.

    :param task_data_code: task_data sobject's unique code
    :return: List of equipment sobjects
    """
    equipment_in_task_data_search = Search('twog/equipment_in_task_data')
    equipment_in_task_data_search.add_filter('task_data_code', task_data_code)
    equipment_in_task_data = equipment_in_task_data_search.get_sobjects()

    if len(equipment_in_task_data) > 0:
        print(equipment_in_task_data)
        equipment_in_task_data_string = ','.join(
            ["'{0}'".format(equipment.get('equipment_code')) for equipment in equipment_in_task_data])

        equipment_search = Search('twog/equipment')
        equipment_search.add_where('\"code\" in ({0})'.format(equipment_in_task_data_string))
        equipment = equipment_search.get_sobjects()

        return equipment
    else:
        return []
