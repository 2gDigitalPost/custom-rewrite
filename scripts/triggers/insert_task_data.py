from common_tools.utils import get_task_estimated_hours_from_task_code, get_task_estimated_hours_from_package_task_code


"""
For any sthpw/task object that is created for a twog/component or twog/package, create a corresponding twog/task_data
sobject. This will hold data that the task needs, but does not include by default. The task_data object can be thought
of as an extension of the task. This is done to prevent modifying the original sthpw/task sobject schema.

twog/task_data will include information like input and output files for a task, and the estimated hours to complete a
task.
"""


def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    task_sobject = input_data.get('sobject')

    # Set up a list of search types. If the task is being attached to any of these search types, then a twog/task_data
    # object will be created
    task_data_search_types = [u'twog/component?project=twog', u'twog/package?project=twog']
    task_search_type = task_sobject.get('search_type')

    if task_sobject and task_search_type in task_data_search_types:
        task_code = task_sobject.get('code')

        # Give the task_data object a default name (shouldn't really matter but might help for searching)
        task_data_name = 'Data for Task: {0}'.format(task_code)

        # Get the estimated hours, which may or may not be available (can be set later)
        # Where the estimated hours comes from depends on the search type
        if task_search_type == u'twog/component?project=twog':
            estimated_hours = get_task_estimated_hours_from_task_code(task_code)
        elif task_search_type == u'twog/package?project=twog':
            estimated_hours = get_task_estimated_hours_from_package_task_code(task_code)
        else:
            estimated_hours = 0

        # Set up the dictionary for inserting
        task_data = {'task_code': task_code, 'name': task_data_name, 'estimated_hours': estimated_hours}

        # Finally, insert the new task_data object
        server.insert('twog/task_data', task_data)


if __name__ == '__main__':
    main()
