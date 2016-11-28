from pyasm.search import Search
from pyasm.widget import SelectWdg


def get_sobject_by_code(search_type, sobject_code):
    """
    Given a search type and an sobject code, return the sobject associated with the code.

    :param search_type: Search type ('twog/order' for example)
    :param sobject_code: sobject unique code
    :return: sobject
    """

    search = Search(search_type)
    search.add_code_filter(sobject_code)
    search_result = search.get_sobject()

    if search_result:
        return search_result
    else:
        return None


def get_sobject_name_by_code(search_type, sobject_code):
    """
    Given a search type and an sobject code, return the sobject's name.

    :param search_type: Search type ('twog/order' for example)
    :param sobject_code: sobject unique code
    :return: String (sobject name)
    """

    search_result = get_sobject_by_code(search_type, sobject_code)

    if search_result:
        return search_result.get('name')
    else:
        return None


def get_order_sobject_from_component_sobject(component_sobject):
    """
    Given a twog/component sobject, get the order that it is assigned to.

    :param component_sobject: twog/component sobject
    :return: twog/order sobject
    """

    order_search = Search('twog/order')
    order_search.add_code_filter(component_sobject.get('order_code'))
    order_sobject = order_search.get_sobject()

    return order_sobject


def get_order_sobject_from_task_sobject(task_sobject):
    """
    Given a task sobject that is attached to a twog/component, travel up the foreign keys to get the parent twog/order
    sobject. This only works if the task is attached to a component.

    :param task_sobject: sthpw/task sobject
    :return: twog/order sobject
    """

    component_sobject = task_sobject.get_parent()

    return get_order_sobject_from_component_sobject(component_sobject)


def get_order_priority_relative_to_all_orders(order_sobject):
    higher_priority_order_search = Search('twog/order')
    higher_priority_order_search.add_filter('priority', order_sobject.get('priority'), op='<')
    higher_priority_orders = higher_priority_order_search.get_sobjects()

    return len(higher_priority_orders) + 1


def get_component_sobjects_from_order_code(order_code):
    """
    Given a twog/order unique code, get a list of all the twog/component sobjects attached to it

    :param order_code: twog/order code
    :return: List of twog/component sobjects (possibly empty)
    """

    component_search = Search('twog/component')
    component_search.add_filter('order_code', order_code)
    components = component_search.get_sobjects()

    return components


def get_package_sobjects_from_order_code(order_code):
    """
    Given a twog/order unique code, get a list of all the twog/package sobjects attached to it

    :param order_code: twog/order code
    :return: List of twog/package sobjects (possibly empty)
    """

    packages_search = Search('twog/package')
    packages_search.add_filter('order_code', order_code)
    packages = packages_search.get_sobjects()

    return packages


def get_task_sobjects_from_component_code(component_code):
    """
    Given a twog/component unique code, get a list of all the sthpw/task sobjects attached to it

    :param component_code: twog/component code
    :return: List of sthpw/task sobjects
    """

    task_search = Search('sthpw/task')
    task_search.add_filter('search_code', component_code)
    tasks = task_search.get_sobjects()

    return tasks


def get_task_sobjects_from_component_sobject(component_sobject):
    """
    Given a twog/component sobject, get a list of all the sthpw/task sobjects attached to it.

    :param component_sobject: twog/component
    :return: List of sthpw/task sobjects
    """

    return get_task_sobjects_from_component_code(component_sobject.get_code())


def get_task_sobjects_from_package_code(package_code):
    """
    Given a twog/package unique code, get a list of all the sthpw/task sobjects attached to it

    :param package_code: twog/package code
    :return: List of sthpw/task sobjects
    """

    task_search = Search('sthpw/task')
    task_search.add_filter('search_code', package_code)
    tasks = task_search.get_sobjects()

    return tasks


def get_task_sobjects_from_package_sobject(package_sobject):
    """
    Given a twog/package sobject, get a list of all the sthpw/task sobjects attached to it.

    :param package_sobject: twog/package
    :return: List of sthpw/task sobjects
    """

    return get_task_sobjects_from_package_code(package_sobject.get_code())


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


def get_component_sobject_from_task_data_code(task_data_code):
    task_data = get_sobject_by_code('twog/task_data', task_data_code)
    task = get_sobject_by_code('sthpw/task', task_data.get_code())
    component = task.get_parent()

    return component


def get_delivery_task_for_package(package_sobject):
    """
    Given a twog/package sobject, search for an attached task named 'Edel: Deliver'. This is the step that determines
    the status of the file delivery. Packages can have one or many tasks, but each one should have at least this task.

    :param package_sobject: twog/package sobject
    :return: sthpw/task sobject or None
    """
    task_search = Search('sthpw/task')
    task_search.add_filter('search_code', package_sobject.get_code())
    tasks = task_search.get_sobjects()

    for task in tasks:
        if task.get('process').lower() == 'edel: deliver':
            return task

    return None


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


def get_files_for_division(division_code):
    """
    Given the unique code for a twog/division sobject, get all the files that are associated with it in a list

    :param division_code: twog/division sobject's unique code
    :return: List of file sobjects (possibly empty)
    """

    file_search = Search('twog/file')
    file_search.add_filter('division_code', division_code)
    files = file_search.get_sobjects()

    return files


def get_file_in_package_sobjects_by_package_code(package_code):
    """
    Given a twog/package code, get all the entries associated with it in the twog/file_in_package table

    :param package_code: twog/package unique code
    :return: List of twog/file_in_package sobjects
    """
    files_in_package_search = Search('twog/file_in_package')
    files_in_package_search.add_filter('package_code', package_code)
    files_in_package = files_in_package_search.get_sobjects()

    return files_in_package


def get_file_sobjects_from_file_in_package_sobjects(file_in_package_sobjects):
    """
    Given a list of twog/file_in_package sobjects, return a list containing the actual twog/file sobjects associated
    with those entries.

    :param file_in_package_sobjects: List of twog/file_in_package sobjects
    :return: List of twog/file sobjects
    """
    if len(file_in_package_sobjects) > 0:
        files_in_package_string = ','.join(
            ["'{0}'".format(file_in_package.get('file_code')) for file_in_package in file_in_package_sobjects]
        )

        files_search = Search('twog/file')
        files_search.add_where('\"code\" in ({0})'.format(files_in_package_string))
        files = files_search.get_sobjects()

        return files
    else:
        return []


def get_task_sobjects_from_file_in_package_sobjects(file_in_package_sobjects):
    """
    Given a list of twog/file_in_package sobjects, return a list of containing the sthpw/task sobjects associated with
    those entries.

    :param file_in_package_sobjects: List of twog/file_in_package sobjects
    :return: List of sthpw/task sobjects
    """

    if len(file_in_package_sobjects) > 0:
        files_in_package_string = ','.join(
            ["'{0}'".format(file_in_package.get_code()) for file_in_package in file_in_package_sobjects]
        )

        task_search = Search('sthpw/task')
        task_search.add_where('\"search_code\" in ({0})'.format(files_in_package_string))
        tasks = task_search.get_sobjects()

        return tasks
    else:
        return []


def get_files_for_package(package_code):
    """
    Given the code for a package, get all the files that are associated with it in a list

    :param package_code: twog/package sobject's unique code
    :return: List of file sobjects
    """
    files_in_package = get_file_in_package_sobjects_by_package_code(package_code)
    files = get_file_sobjects_from_file_in_package_sobjects(files_in_package)

    return files


def get_file_in_package_status(file_sobject):
    task_list = file_sobject.get_all_children('sthpw/task')
    task = task_list[0]

    return task.get('status')


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

    instructions_sobjects = instructions_search.get_sobjects()
    instructions_sobjects = sorted(instructions_sobjects, key=lambda sobject: sobject.get('name'))

    for instructions_sobject in instructions_sobjects:
        instructions_template_select_wdg.append_option(instructions_sobject.get('name'),
                                                       instructions_sobject.get_code())

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


def get_instructions_text_from_instructions_code(instructions_code):
    """
    Given an instructions code, search for the instructions sobject, and return its text.

    :param instructions_code: instructions unique code
    :return: String
    """

    instructions = get_sobject_by_code('twog/instructions', instructions_code)

    if instructions:
        return instructions.get('instructions_text')
    else:
        return 'Sorry, no instructions are available yet.'


def get_task_instructions_text_from_instructions_code(instructions_code, task_name, package=False):
    """
    Given an instructions code and a task name, get the task's instruction text from the instructions document.
    If none exists, return a string in its place.

    :param instructions_code: instructions unique code
    :param task_name: Task name (process)
    :param package: Boolean (True if instructions are for a twog/package, False if for a twog/component)
    :return: String
    """

    if package:
        instructions = get_sobject_by_code('twog/package_instructions', instructions_code)
    else:
        instructions = get_sobject_by_code('twog/instructions', instructions_code)

    if instructions:
        instructions_text = instructions.get('instructions_text')
    else:
        return 'Sorry, no instructions are available for this task.'

    task_instructions_text = ''
    instruction_text_in_task = False

    for line in instructions_text.split('\n'):
        if line:
            if line.startswith('!@|'):
                name = line.split('|')[1].strip()

                if task_name == name:
                    task_instructions_text += name + '\n'
                    instruction_text_in_task = True
                else:
                    instruction_text_in_task = False
            elif instruction_text_in_task:
                task_instructions_text += line + '\n'

    if not task_instructions_text:
        task_instructions_text = 'Sorry, no instructions are available for this task.'

    return task_instructions_text


def get_task_estimated_hours_from_instructions_document(instructions_document, task_name):

    instructions_text = instructions_document.get('instructions_text')

    for line in instructions_text.split('\n'):
        if line:
            if line.startswith('!@|'):
                _, name, department, hours = line.split('|')
                name = name.strip()

                if name.lower() == task_name.lower().strip():
                    return float(hours)
    else:
        return 0


def get_task_estimated_hours_from_task_code(task_code):
    task_search = Search('sthpw/task')
    task_search.add_code_filter(task_code)
    task = task_search.get_sobject()

    component = task.get_parent()

    instructions_code = component.get('instructions_code')

    if instructions_code:
        instructions_sobject = get_sobject_by_code('twog/instructions', instructions_code)

        if instructions_sobject:
            return get_task_estimated_hours_from_instructions_document(instructions_sobject, task.get('process'))

    return 0


def get_task_estimated_hours_from_package_task_code(task_code):
    """
    From a sthpw/task sobject, assumed to be attached to a twog/package, get the estimated hours for the task.
    This is taken from the twog/platform_connection sobject related to the package.

    :param task_code: sthpw/task code (must be for a twog/package)
    :return: Float
    """

    # Get the task sobject
    task = get_sobject_by_code('sthpw/task', task_code)

    # Get the package sobject
    package = task.get_parent()

    # Get the platform code, used for the platform_connection search
    platform_code = package.get('platform_code')

    # Get the division code, also for the platform_connection search
    division = get_client_division_sobject_from_order_code(package.get('order_code'))
    division_code = division.get_code()

    # Search for the platform_connection
    platform_connection_search = Search('twog/platform_connection')
    platform_connection_search.add_filter('platform_code', platform_code)
    platform_connection_search.add_filter('division_code', division_code)
    platform_connection = platform_connection_search.get_sobject()

    # Get the estimated hours, and convert to a float
    estimated_hours = float(platform_connection.get('estimated_hours'))

    return estimated_hours


def get_component_estimated_total_hours_from_component_code(component_code):
    """
    Given a twog/component code, sum up all the estimated hours from its tasks.

    :param component_code: twog/component code
    :return: int or None
    """

    tasks = get_task_sobjects_from_component_code(component_code)

    estimated_hours_sum = 0

    for task in tasks:
        task_data = get_task_data_sobject_from_task_code(task.get_code())

        if task_data.get('estimated_hours'):
            task_estimated_hours = float(task_data.get('estimated_hours'))

            estimated_hours_sum += task_estimated_hours

    if estimated_hours_sum == 0:
        return None
    else:
        return estimated_hours_sum


def get_component_estimated_remaining_hours_from_component_code(component_code):
    """
    Same function as get_component_estimated_total_hours_from_component_code, but only takes into account tasks that
    are not marked as 'Complete'.

    :param component_code: twog/component code
    :return: int or None
    """

    tasks = get_task_sobjects_from_component_code(component_code)

    estimated_hours_sum = 0

    tasks = [task for task in tasks if task.get('status') != 'Complete']

    for task in tasks:
        task_data = get_task_data_sobject_from_task_code(task.get_code())

        if task_data.get('estimated_hours'):
            task_estimated_hours = float(task_data.get('estimated_hours'))

            estimated_hours_sum += task_estimated_hours

    if estimated_hours_sum == 0:
        return None
    else:
        return estimated_hours_sum


def get_order_estimated_total_hours_from_order_code(order_code):
    """
    Given a twog/order code, get the estimated total hours to complete the order. This is done by getting the estimated
    total hours for each of the components, and getting the highest one (because components can be completed in
    parallel).

    :param order_code: twog/order code
    :return: int or None
    """
    components = get_component_sobjects_from_order_code(order_code)

    estimated_total_hours = 0

    for component in components:
        component_estimated_hours = get_component_estimated_total_hours_from_component_code(component.get_code())

        if component_estimated_hours and component_estimated_hours > estimated_total_hours:
            estimated_total_hours = component_estimated_hours

    if estimated_total_hours == 0:
        return None
    else:
        return estimated_total_hours


def get_client_division_sobject_from_order_sobject(order_sobject):
    """
    Given an order sobject, get the division sobject associated with it. If there isn't one, return None

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


def get_client_division_sobject_from_order_code(order_code):
    """
    Given an order code, get the division sobject associated with it. If there isn't one, return None

    :param order_code: twog/order code
    :return: twog/division sobject or None
    """
    order_sobject = get_sobject_by_code('twog/order', order_code)

    return get_client_division_sobject_from_order_sobject(order_sobject)


def get_client_division_sobject_for_package_sobject(package_sobject):
    """
    Given a twog/package sobject, get the division sobject associated with it (through the parent twog/order sobject).

    :param package_sobject: twog/package sobject
    :return: twog/division sobject
    """

    order = get_sobject_by_code('twog/order', package_sobject.get('order_code'))
    division = get_sobject_by_code('twog/division', order.get('division_code'))

    return division


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


def get_platform_connection_by_package_sobject(package_sobject):
    order_search = Search('twog/order')
    order_search.add_code_filter(package_sobject.get('order_code'))
    order_sobject = order_search.get_sobject()

    platform_connection_search = Search('twog/platform_connection')
    platform_connection_search.add_filter('platform_code', package_sobject.get('platform_code'))
    platform_connection_search.add_filter('division_code', order_sobject.get('division_code'))
    platform_connection = platform_connection_search.get_sobject()

    return platform_connection


def get_component_status_label_and_color(component_status):
    """

    :param component_status:
    :return:
    """

    component_status_dictionary = {
        'in_progress': ('In Progress', '#1D8B98'),
        'on_hold': ('On Hold', '#FF0000'),
        'complete': ('Complete', '#A3D991')
    }

    return component_status_dictionary.get(component_status, (None, None))


def get_all_tasks_from_order_sobject(order_sobject):
    """
    Given a twog/order sobject, get all the sthpw/task sobjects attached to it (through the components and packages).

    :param order_sobject: twog/order sobject
    :return: List of sthpw/task sobjects
    """

    # Get a list of the components and tasks attached to the order
    components = get_component_sobjects_from_order_code(order_sobject.get_code())
    packages = get_package_sobjects_from_order_code(order_sobject.get_code())

    tasks = []

    # Add each component task to the list
    for component in components:
        tasks.extend(get_task_sobjects_from_component_sobject(component))

    # Add each package task to the list
    for package in packages:
        tasks.extend(get_task_sobjects_from_package_sobject(package))

    return tasks


def get_order_builder_url_on_click(url):
    """
    Gets the behavior that the button uses on click.
    This code was found on stackoverflow, edit with caution.

    NOTE: users MUST update to Chrome 44+, Firefox 41+, IE 11+
    Safari, Opera, etc. are untested

    :param url: the url as a string
    :return: a behavior dictionary
    """
    behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try{
    var url = '%s';
    var textArea = document.createElement("textarea");

    //
    // *** This styling is an extra step which is likely not required. ***
    //
    // Why is it here? To ensure:
    // 1. the element is able to have focus and selection.
    // 2. if element was to flash render it has minimal visual impact.
    // 3. less flakyness with selection and copying which **might** occur if
    //    the textarea element is not visible.
    //
    // The likelihood is the element won't even render, not even a flash,
    // so some of these are just precautions. However in IE the element
    // is visible whilst the popup box asking the user for permission for
    // the web page to copy to the clipboard.
    //

    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';

    textArea.value = url;

    document.body.appendChild(textArea);

    textArea.select();

    try{
        var successful = document.execCommand('copy');
        document.body.removeChild(textArea);
    }
    catch(err){
        var value = prompt('Your browser might be out of date. Please copy the url manually.', url);
    }
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % url}

    return behavior
