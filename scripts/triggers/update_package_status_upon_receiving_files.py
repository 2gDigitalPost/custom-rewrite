from pyasm.search import Search

from common_tools.utils import get_sobject_by_code, get_delivery_task_for_package


def main(server=None, input_data=None):
    if not input_data:
        return

    # The input for the script should be a twog/file_in_package sobject
    file_in_package_sobject = input_data.get('sobject')

    # Get the package sobject
    package = get_sobject_by_code('twog/package', file_in_package_sobject.get('package_code'))
    # Get the delivery task for the package
    delivery_task = get_delivery_task_for_package(package)

    # There should always be a delivery task attached to a package, but check just in case
    if not delivery_task:
        return

    # This script only applies to Packages that are marked as Waiting for Files
    if delivery_task.get('status').lower() != 'waiting for files':
        return

    # Get the twog/component_files_to_package sobjects based on the package code
    component_files_to_package_search = Search('twog/component_files_to_package')
    component_files_to_package_search.add_filter('package_code', package.get_code())
    component_files_to_package_entries = component_files_to_package_search.get_sobjects()

    if not component_files_to_package_entries:
        return

    # Iterate through the twog/component_files_to_package entries, checking each component. If any of the components
    # listed are not yet complete, return.
    for component_files_to_package_entry in component_files_to_package_entries:
        component = get_sobject_by_code('twog/component', component_files_to_package_entry.get('component_code'))

        if component.get('status').lower() != 'complete':
            return

    # Build the task search key
    package_task_search_key = server.build_search_key('sthpw/task', delivery_task.get('code'), project_code='twog')

    # Send the update data to the server
    server.update(package_task_search_key, {'status': 'Ready'})
