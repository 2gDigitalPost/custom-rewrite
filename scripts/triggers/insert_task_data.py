def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    task_sobject = input_data.get('sobject')
    task_code = task_sobject.get('code')

    search_type = 'twog/task_data'
    task_data = {'task_code': task_code}

    server.insert(search_type, task_data)


if __name__ == '__main__':
    main()