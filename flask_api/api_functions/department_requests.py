def add_tasks_to_department_request_dictionary(server, department_request_dict):
    department_request_codes = [department_request.get('code') for department_request in department_request_dict]
    department_request_codes_string = '|'.join(department_request_codes)

    tasks = server.eval(
        "@SOBJECT(sthpw/task['search_code', 'in', '{0}'])".format(department_request_codes_string)
    )

    request_tasks_by_search_code = {}
    approval_tasks_by_search_code = {}

    for task in tasks:
        if task.get('process').lower() == 'approval':
            approval_tasks_by_search_code[task.get('search_code')] = task
        elif task.get('process').lower() == 'request':
            request_tasks_by_search_code[task.get('search_code')] = task

    for department_request in department_request_dict:
        department_request['request_task'] = request_tasks_by_search_code.get(department_request.get('code'))
        department_request['approval_task'] = approval_tasks_by_search_code.get(department_request.get('code'))

    # Give a summary status from one of the two tasks
    for department_request in department_request_dict:
        request_task = department_request.get('request_task')
        approval_task = department_request.get('approval_task')

        request_task_status = request_task.get('status').lower()
        approval_task_status = approval_task.get('status').lower()

        if request_task_status == 'ready':
            summary_status = 'Ready'
        elif request_task_status == 'in progress':
            summary_status = 'In Progress'
        elif request_task_status == 'additional info needed':
            summary_status = 'Additional Info Requested'
        elif request_task_status == 'revise':
            summary_status = 'Revise'
        elif approval_task_status == 'needs approval':
            summary_status = 'Needs Approval'
        else:
            summary_status = 'Approved'

        department_request['summary_status'] = summary_status
