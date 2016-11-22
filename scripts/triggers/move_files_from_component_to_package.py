from pyasm.search import Search

from common_tools.utils import get_sobject_by_code, get_task_sobjects_from_component_code,\
    get_task_data_sobject_from_task_code, get_task_data_in_files, get_task_data_out_files


def main(server=None, input_data=None):
    if not input_data:
        return

    # The input for the script should be a twog/component sobject
    component_sobject = input_data.get('sobject')

    # This script only applies to Components that are marked as Complete
    if component_sobject.get('status').lower() != 'complete':
        return

    component_code = component_sobject.get('code')

    # Search for this component in the twog/component_files_to_package table.
    component_files_to_package_search = Search('twog/component_files_to_package')
    component_files_to_package_search.add_filter('component_code', component_code)
    component_files_to_package_entries = component_files_to_package_search.get_sobjects()

    tasks = get_task_sobjects_from_component_code(component_code)

    task_data_sobjects = []

    for task in tasks:
        task_data_sobjects.append(get_task_data_sobject_from_task_code(task.get_code()))

    deliverable_files = []

    for task_data_sobject in task_data_sobjects:
        in_files = get_task_data_in_files(task_data_sobject.get_code())
        out_files = get_task_data_out_files(task_data_sobject.get_code())

        for in_file in in_files:
            classification = in_file.get('classification')

            if classification == 'deliverable' and in_file not in deliverable_files:
                deliverable_files.append(in_file)

        for out_file in out_files:
            classification = out_file.get('classification')

            if classification == 'deliverable' and out_file not in deliverable_files:
                deliverable_files.append(out_file)

    # Iterate through the entries in twog/component_files_to_package (If there aren't any then this script does nothing)
    for component_files_to_package_entry in component_files_to_package_entries:
        for deliverable_file in deliverable_files:
            deliverable_file_code = deliverable_file.get_code()

            package = get_sobject_by_code('twog/package', component_files_to_package_entry.get('package_code'))

            # Get a list of all the tasks attached to a package (might be empty)
            package_tasks = package.get_all_children('sthpw/task')

            # If no tasks are attached to the package, no need to do anything
            if package_tasks:
                first_task_in_package = package.get_all_children('sthpw/task')[0]
                first_task_data = get_task_data_sobject_from_task_code(first_task_in_package.get_code())
                first_task_data_code = first_task_data.get_code()

                existing_entry_search = Search('twog/task_data_in_file')
                existing_entry_search.add_filter('task_data_code', first_task_data_code)
                existing_entry_search.add_filter('file_code', deliverable_file_code)
                existing_entry = existing_entry_search.get_sobject()

                if not existing_entry:
                    # Set up the data dictionary
                    data = {'task_data_code': first_task_data_code, 'file_code': deliverable_file_code}

                    # Finally, insert the new twog/task_data_in_file object
                    server.insert('twog/task_data_in_file', data)


if __name__ == '__main__':
    main()
