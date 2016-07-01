from xml.etree import ElementTree

from pyasm.search import Search


def get_pipeline_xml(pipeline_code):
    pipeline_search = Search('sthpw/pipeline')
    pipeline_search.add_filter('code', pipeline_code)

    pipeline_search_result = pipeline_search.get_sobject()

    if pipeline_search_result:
        return pipeline_search_result.get_value('pipeline')
    else:
        return None


def task_is_assigned_to_group(xml, process, group):
    xml_tree = ElementTree.fromstring(xml)

    for process_xml in xml_tree.iter('process'):
        print(process_xml.attrib)
        if process_xml.attrib.get('name') == process and process_xml.attrib.get('assigned_login_group') == group:
            return True
    else:
        return False


def main():
    task_search = Search('sthpw/task')
    task_search.add_filter('search_type', 'twog/title_order?project=twog')
    task_search.add_filter('status', 'Complete', '!=')

    tasks = task_search.get_sobjects()
    tasks = [task for task in tasks if task.get_parent()]

    final_tasks = []

    for task in tasks:
        print(task.get_value('process'))
        print(task.get_parent())
        process_search = Search('config/process')
        process_search.add_filter('process', task.get_value('process'))

        process_search_results = process_search.get_sobjects()

        if process_search_results:
            pipeline_search = Search('sthpw/pipeline')
            pipeline_search.add_filter('code', task.get_parent().get_value('pipeline_code'))

            pipeline_search_result = pipeline_search.get_sobject()

            xml = get_pipeline_xml(task.get_parent().get_value('pipeline_code'))

            if pipeline_search_result and task_is_assigned_to_group(xml, task.get_value('process'), 'Edel'):
                final_tasks.append(task)

    print([final_task.get('code') for final_task in final_tasks])
    return [final_task.get('code') for final_task in final_tasks]
    # return final_tasks


if __name__ == '__main__':
    main()