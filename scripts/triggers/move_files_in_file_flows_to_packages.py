from pyasm.search import Search

from common_tools.utils import get_sobject_by_code, get_task_sobjects_from_component_code,\
    get_task_data_sobject_from_task_code, get_task_data_in_files, get_task_data_out_files


def main(server=None, input_data=None):
    if not input_data:
        return

    print("ENTER THE SCRIPT")

    # The input for the script should be a twog/component sobject
    component_sobject = input_data.get('sobject')

    # This script only applies to Components that are marked as Complete
    if component_sobject.get('status').lower() != 'complete':
        return

    component_code = component_sobject.get('code')

    # Get the file flow objects
    file_flows_search = Search('twog/file_flow')
    file_flows_search.add_filter('component_code', component_code)
    file_flows = file_flows_search.get_sobjects()

    # Only proceed if the file flows were found
    for file_flow in file_flows:
        # Get the destination packages for each file flow
        # Start by querying the twog/file_flow_to_package table
        file_flow_to_packages_search = Search('twog/file_flow_to_package')
        file_flow_to_packages_search.add_filter('file_flow_code', file_flow.get('code'))
        file_flow_to_packages = file_flow_to_packages_search.get_sobjects()

        # Get the package codes
        package_codes = [file_flow_to_package.get('package_code') for file_flow_to_package in file_flow_to_packages]

        for package_code in package_codes:
            package = get_sobject_by_code('twog/package', package_code)

            # Get a list of all the tasks attached to a package (might be empty)
            package_tasks = package.get_all_children('sthpw/task')

            # If no tasks are attached to the package, no need to do anything
            if package_tasks:
                first_task_in_package = package_tasks[0]
                first_task_data = get_task_data_sobject_from_task_code(first_task_in_package.get_code())
                first_task_data_code = first_task_data.get_code()

                existing_entry_search = Search('twog/task_data_in_file')
                existing_entry_search.add_filter('task_data_code', first_task_data_code)
                existing_entry_search.add_filter('file_code', file_flow.get('file_code'))
                existing_entry = existing_entry_search.get_sobject()

                if not existing_entry:
                    # Set up the data dictionary
                    data = {'task_data_code': first_task_data_code, 'file_code': file_flow.get('file_code')}

                    # Finally, insert the new twog/task_data_in_file object
                    server.insert('twog/task_data_in_file', data)
