from pyasm.search import Search

from common_tools.utils import get_file_in_package_sobjects_by_package_code,\
    get_task_sobjects_from_file_in_package_sobjects


def main(server=None, input_data=None):
    if not input_data:
        return

    # Get the task
    task_sobject = input_data.get('sobject')

    # Only proceed if the task exists and is attached to a twog/package sobject
    if not (task_sobject and task_sobject.get('search_type') == u'twog/package?project=twog'):
        return

    # Only send the notification if the task is being marked as completed.
    if task_sobject.get('status') != 'Ready':
        return

    # Only run the script for the Edel: Deliver task
    if task_sobject.get('process').lower() != 'edel: deliver':
        return

    package_search_code = task_sobject.get('search_code')

    # Get the twog/file_in_package entries using the package code
    file_in_package_entries = get_file_in_package_sobjects_by_package_code(package_search_code)

    print(file_in_package_entries)

    # Return if no files were found for the package
    if not file_in_package_entries:
        return

    # Get all the sthpw/task sobjects associated with the twog/file_in_package entries (that's where the status is)
    file_in_package_tasks = get_task_sobjects_from_file_in_package_sobjects(file_in_package_entries)

    print(file_in_package_tasks)

    # Only continue if the tasks were found
    if not file_in_package_tasks:
        return

    # Set up an empty dictionary to hold the data sent to the server
    update_data = {}

    # Go through each entry in the twog/file_in_package table. If the status is set to 'waiting', then add it to
    # the update dictionary, with a status of 'ready'.
    for file_in_package_task in file_in_package_tasks:
        if file_in_package_task.get('status').lower() == 'waiting':
            file_in_package_search_key = server.build_search_key('sthpw/task', file_in_package_task.get_code(),
                                                                 project_code='twog')
            update_data[file_in_package_search_key] = {'status': 'Ready'}

    # Send the data, if there is any
    if update_data:
        server.update_multiple(update_data)


if __name__ == '__main__':
    main()
