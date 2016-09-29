from pyasm.search import Search
from pyasm.widget import SelectWdg


def get_order_sobject_from_component_sobject(component_sobject):
    """
    Given a twog/component code, get the order that it is assigned to.

    :param component_code: twog/component unique code
    :return: twog/order sobject
    """

    order_search = Search('twog/order')
    order_search.add_code_filter(component_sobject.get('order_code'))
    order_sobject = order_search.get_sobject()

    return order_sobject


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


def get_files_for_package(package_code):
    """
    Given the code for a package, get all the files that are associated with it in a list

    :param package_code: twog/package sobject's unique code
    :return: List of file sobjects
    """
    files_in_package_search = Search('twog/file_in_package')
    files_in_package_search.add_filter('package_code', package_code)
    files_in_package = files_in_package_search.get_sobjects()

    if len(files_in_package) > 0:
        files_in_package_string = ','.join(
            ["'{0}'".format(file_in_package.get('file_code')) for file_in_package in files_in_package]
        )

        files_search = Search('twog/file')
        files_search.add_where('\"code\" in ({0})'.format(files_in_package_string))
        files = files_search.get_sobjects()

        return files
    else:
        return []


def get_instructions_select_wdg():
    """
    Get a Select Widget with all the instructions options

    :return: SelectWdg
    """

    instructions_search = Search('twog/instructions')

    instructions_select_wdg = SelectWdg('instructions_select')
    instructions_select_wdg.set_id('instructions_select')
    instructions_select_wdg.add_empty_option()
    instructions_select_wdg.set_search_for_options(instructions_search, 'code', 'name')

    return instructions_select_wdg


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
    The list of department instructions will be sorted by the sort_order column in the join table.

    :param instructions_template_code: twog/instructions_template unique code
    :return: List of twog/department_instructions sobjects (possibly empty)
    """

    department_instructions_in_template_search = Search('twog/department_instructions_in_template')
    department_instructions_in_template_search.add_filter('instructions_template_code', instructions_template_code)
    department_instructions_in_template_sobjects = department_instructions_in_template_search.get_sobjects()

    # Sort the entries by their sort order
    department_instructions_in_template_sobjects = sorted(department_instructions_in_template_sobjects,
                                                          key=lambda x: x.get('sort_order'))
    # Get a list of the department_instructions codes, sorted
    sorted_department_instructions_codes = [
        department_instructions_in_template_sobject.get('department_instructions_code')
        for department_instructions_in_template_sobject in department_instructions_in_template_sobjects
        ]

    if len(department_instructions_in_template_sobjects) > 0:
        department_instructions_code_string = ','.join(
            ["'{0}'".format(department_instructions_code) for department_instructions_code
             in sorted_department_instructions_codes]
        )

        department_instructions_search = Search('twog/department_instructions')
        department_instructions_search.add_where('\"code\" in ({0})'.format(department_instructions_code_string))
        department_instructions_sobjects = department_instructions_search.get_sobjects()

        # Sort the department_instructions sobjects
        sorted_department_instructions_sobjects = []

        for department_instructions_sobject in department_instructions_sobjects:
            department_instructions_code = department_instructions_sobject.get_code()
            index = sorted_department_instructions_codes.index(department_instructions_code)

            sorted_department_instructions_sobjects.insert(index, department_instructions_sobject)

        return sorted_department_instructions_sobjects
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


def get_component_instructions_text_from_task_sobject(task):
    component_sobject = task.get_parent()

    return get_instructions_text_for_instructions_template_code(component_sobject.get('instructions_template_code'))


def get_instructions_sobject_from_instructions_code(instructions_code):
    """
    Given an instructions code, return the sobject that it refers to. If an instructions sobject is not found,
    return None

    :param instructions_code: instructions unique code
    :return: twog/instructions sobject or None
    """

    instructions_search = Search('twog/instructions')
    instructions_search.add_code_filter(instructions_code)
    instructions = instructions_search.get_sobject()

    return instructions or None


def get_instructions_text_from_instructions_code(instructions_code):
    """
    Given an instructions code, search for the instructions sobject, and return its text.

    :param instructions_code: instructions unique code
    :return: String
    """

    instructions = get_instructions_sobject_from_instructions_code(instructions_code)

    if instructions:
        return instructions.get('instructions_text')
    else:
        return 'Sorry, no instructions are available yet.'


def get_task_instructions_text_from_instructions_code(instructions_code, task_name):
    """
    Given an instructions code and a task name, get the task's instruction text from the instructions document.
    If none exists, return a string in its place.

    :param instructions_code: instructions unique code
    :param task_name: Task name (process)
    :return: String
    """

    instructions = get_instructions_sobject_from_instructions_code(instructions_code)

    if instructions:
        instructions_text = instructions.get('instructions_text')
    else:
        return 'Sorry, no instructions are available for this task.'

    task_instructions_text = ''
    instruction_text_in_task = False

    for line in instructions_text.split('\n'):
        if line:
            if line[0:3] == '###':
                if task_name == line[4:]:
                    task_instructions_text += line[4:] + '\n'
                    instruction_text_in_task = True
                else:
                    instruction_text_in_task = False
            elif instruction_text_in_task:
                task_instructions_text += line + '\n'

    if not task_instructions_text:
        task_instructions_text = 'Sorry, no instructions are available for this task.'

    return task_instructions_text


def get_client_division_sobject_from_order_sobject(order_sobject):
    """
    Given an order sobject, get the division code associated with it. If there isn't one, return None

    :param order_sobject: twog/order sobject
    :return: twog/division sobject or None
    """

    division_search = Search('twog/division')
    division_search.add_code_filter(order_sobject.get('division_code'))
    division_sobject = division_search.get_sobject()

    if division_sobject:
        return division_sobject
    else:
        return None


def get_client_division_sobject_for_task_sobject(task):
    """
    Given a task sobject, travel up the chain of Component and Order to get the Division the order is assigned
    to. This will only work for tasks that are assigned to components.

    :param task: task sobject
    :return: twog/division sobject
    """

    parent_component = task.get_parent()

    order_search = Search('twog/order')
    order_search.add_code_filter(parent_component.get('order_code'))
    order = order_search.get_sobject()

    division_search = Search('twog/division')
    division_search.add_code_filter(order.get('division_code'))
    division = division_search.get_sobject()

    return division


def get_deliverable_files_in_order(order_sobject):
    """
    Given an order sobject, return all the deliverable files associated with it.

    :param order_sobject: twog/order sobject
    :return: List of twog/file sobjects
    """

    files_in_order_search = Search('twog/file_in_order')
    files_in_order_search.add_filter('order_code', order_sobject.get_code())
    files_in_order = files_in_order_search.get_sobjects()

    if files_in_order:
        files_in_order_string = ','.join(
            ["'{0}'".format(files_in_order.get('file_code')) for files_in_order in files_in_order]
        )

        deliverable_files_search = Search('twog/file')
        deliverable_files_search.add_where('\"code\" in ({0})'.format(files_in_order_string))
        deliverable_files_search.add_filter('classification', 'deliverable')
        deliverable_files = deliverable_files_search.get_sobjects()

        return deliverable_files
    else:
        return []


def get_delivery_task_for_package(package_code):
    """

    :param package_code:
    :return:
    """

    package_search = Search('twog/package')
    package_search.add_code_filter(package_code)
    package_sobject = package_search.get_sobject()

    package_tasks = package_sobject.get_all_children('sthpw/task')

    for package_task in package_tasks:
        if package_task.get('process').lower() == 'deliver':
            return package_task

    return None
