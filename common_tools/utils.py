from pyasm.search import Search
from pyasm.widget import SelectWdg


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
        equipment_in_task_data_string = ','.join(
            ["'{0}'".format(equipment.get('equipment_code')) for equipment in equipment_in_task_data])

        equipment_search = Search('twog/equipment')
        equipment_search.add_where('\"code\" in ({0})'.format(equipment_in_task_data_string))
        equipment = equipment_search.get_sobjects()

        return equipment
    else:
        return []


def get_task_data_in_files(task_data_code):
    """
    Given the code for a task_data entry, get all the input files associated with it in a list.

    :param task_data_code: task_data sobject's unique code
    :return: List of file sobjects
    """
    in_files_search = Search('twog/task_data_in_file')
    in_files_search.add_filter('task_data_code', task_data_code)
    in_files = in_files_search.get_sobjects()

    if len(in_files) > 0:
        in_files_string = ','.join(["'{0}'".format(in_file.get('file_code')) for in_file in in_files])

        files_search = Search('twog/file')
        files_search.add_where('\"code\" in ({0})'.format(in_files_string))
        files = files_search.get_sobjects()

        return files
    else:
        return []


def get_task_data_out_files(task_data_code):
    """
    Given the code for a task_data entry, get all the output files associated with it in a list.

    :param task_data_code: task_data sobject's unique code
    :return: List of file sobjects
    """
    out_files_search = Search('twog/task_data_out_file')
    out_files_search.add_filter('task_data_code', task_data_code)
    out_files = out_files_search.get_sobjects()

    if len(out_files) > 0:
        out_files_string = ','.join(["'{0}'".format(out_file.get('file_code')) for out_file in out_files])

        files_search = Search('twog/file')
        files_search.add_where('\"code\" in ({0})'.format(out_files_string))
        files = files_search.get_sobjects()

        return files
    else:
        return []


def get_files_for_order(order_code):
    """
    Given the code for an order, get all the files that are associated with it in a list.

    :param order_code: order sobject's unique code
    :return: List of file sobjects
    """

    files_in_order_search = Search('twog/file_in_order')
    files_in_order_search.add_filter('order_code', order_code)
    files_in_order = files_in_order_search.get_sobjects()

    if len(files_in_order) > 0:
        files_string = ','.join(
            ["'{0}'".format(file_in_order.get('file_code')) for file_in_order in files_in_order]
        )

        files_search = Search('twog/file')
        files_search.add_where('\"code\" in ({0})'.format(files_string))
        files = files_search.get_sobjects()

        return files
    else:
        return []


def get_instructions_template_select_wdg():
    """
    Get a Select Widget with all the instructions template options

    :return: SelectWdg
    """

    instructions_search = Search('twog/instructions_template')

    instructions_template_select_wdg = SelectWdg('instructions_template_select')
    instructions_template_select_wdg.set_id('instructions_template_select')
    instructions_template_select_wdg.add_empty_option()
    instructions_template_select_wdg.set_search_for_options(instructions_search, 'code', 'name')

    return instructions_template_select_wdg


def get_department_instructions_sobjects_for_instructions_template_code(instructions_template_code):
    """
    Given the code to an instructions template, return a list of the corresponding department instructions sobjects.

    :param instructions_template_code: twog/instructions_template unique code
    :return: List of twog/department_instructions sobjects (possibly empty)
    """

    department_instructions_in_template_search = Search('twog/department_instructions_in_template')
    department_instructions_in_template_search.add_filter('instructions_template_code', instructions_template_code)
    department_instructions_in_template_sobjects = department_instructions_in_template_search.get_sobjects()

    if len(department_instructions_in_template_sobjects) > 0:
        department_instructions_codes = [department_instructions_in_template_sobject.get('department_instructions_code')
                                         for department_instructions_in_template_sobject
                                         in department_instructions_in_template_sobjects]

        department_instructions_code_string = ','.join(
            ["'{0}'".format(department_instructions_code) for department_instructions_code
             in department_instructions_codes]
        )

        department_instructions_search = Search('twog/department_instructions')
        department_instructions_search.add_where('\"code\" in ({0})'.format(department_instructions_code_string))
        department_instructions_sobjects = department_instructions_search.get_sobjects()

        return department_instructions_sobjects
    else:
        return []


def get_instructions_text_for_instructions_template_code(instructions_template_code):
    """
    Given the code to an instructions template, return the collected text of all the corresponding department
    instructions.

    :param instructions_template_code: twog/instructions_template unique code
    :return: Text (string) or None
    """

    department_instructions_sobjects = get_department_instructions_sobjects_for_instructions_template_code(
        instructions_template_code)

    if department_instructions_sobjects:
        full_instructions_text = ''

        for department_instructions_sobject in department_instructions_sobjects:
            full_instructions_text += department_instructions_sobject.get('name')
            full_instructions_text += '\n\n'
            full_instructions_text += department_instructions_sobject.get('instructions_text')
            full_instructions_text += '\n\n'

        return full_instructions_text.encode('utf-8')
    else:
        return None


def get_component_instructions_from_task_sobject(task):
    component_sobject = task.get_parent()

    return get_instructions_text_for_instructions_template_code(component_sobject.get('instructions_template_code'))
