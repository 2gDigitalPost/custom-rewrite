from common_tools.utils import get_task_estimated_hours_from_task_code


def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    task_sobject = input_data.get('sobject')

    if task_sobject and task_sobject.get('search_type') == u'twog/component?project=twog':
        task_code = task_sobject.get('code')

        task_data_name = 'Data for Task: {0}'.format(task_code)

        estimated_hours = get_task_estimated_hours_from_task_code(task_code)

        task_data = {'task_code': task_code, 'name': task_data_name}

        if estimated_hours:
            task_data['estimated_hours'] = estimated_hours

        server.insert('twog/task_data', task_data)


if __name__ == '__main__':
    main()
