from pyasm.biz import Pipeline
from pyasm.search import Search

from order_builder.order_builder_utils import get_pipeline_xml


def main(server=None, input_data=None):
    if not input_data:
        return

    # The input for the script should be a sthpw/task sobject
    task_sobject = input_data.get('sobject')

    # This script only applies to tasks that are marked as Complete, and are attached to twog/component sobjects
    if not (task_sobject.get('status') == 'Complete' and task_sobject.get(
            'search_type') == u'twog/component?project=twog'):
        return

    # Tasks saved on twog/component have extra data associated with them, saved under twog/task_data
    # Retrieve the entry of twog/task_data for this task sobject
    task_data_search = Search('twog/task_data')
    task_data_search.add_filter('task_code', task_sobject.get('code'))
    task_data = task_data_search.get_sobject()

    if not task_data:
        return

    # Get the next task in the pipeline
    # Start by getting the component sobject the task is attached to
    component_search = Search('twog/component')
    component_search.add_code_filter(task_sobject.get('search_code'))
    component_sobject = component_search.get_sobject()

    if not component_sobject:
        return

    # Then get the output processes. Start by fetching the pipeline object
    pipeline = Pipeline('twog/component')
    pipeline.set_pipeline(get_pipeline_xml(component_sobject.get('pipeline_code')))

    # Then get the names of the processes contained in that pipeline (which corresponds to all the names of the tasks
    # within this component)
    output_processes = pipeline.get_output_processes(task_sobject.get('process'))

    # Now, get the actual task objects
    tasks_search = Search('sthpw/task')
    tasks_search.add_filter('process', output_processes)
    tasks_search.add_parent_filter(component_sobject)
    output_tasks = tasks_search.get_sobjects()

    # Fetch the output files attached to the original task
    out_files_search = Search('twog/task_data_out_file')
    out_files_search.add_filter('task_data_code', task_data.get_code())
    out_files = out_files_search.get_sobjects()

    if not out_files:
        return

    # Go through each output task and attach the output files as input files
    for output_task in output_tasks:
        output_task_data_search = Search('twog/task_data')
        output_task_data_search.add_filter('task_code', output_task.get_code())
        output_task_data = output_task_data_search.get_sobject()

        for out_file in out_files:
            inserted_data = {
                'task_data_code': output_task_data.get_code(),
                'file_code': out_file.get('file_code')
            }

            server.insert('twog/task_data_in_file', inserted_data)

            # The file should be added to the files in order list
            server.insert('twog/file_in_order', {'order_code': component_sobject.get('order_code'),
                                                 'file_code': out_file.get('file_code')})


if __name__ == '__main__':
    main()
