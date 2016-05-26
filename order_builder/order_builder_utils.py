from xml.etree import ElementTree

from pyasm.search import Search
from pyasm.widget import SelectWdg

from pyasm.web import HtmlElement


TASK_COLORS = {
    "Assignment":      "#ffc500",
    "Pending":         "#34def2",
    "In Progress":     "#01949b",
    "Waiting":         "#4212ae",
    "Need Assistance": "#4212ae",
    "Review":          "#ff0800",
    "Approved":        "#00c611",
    "Complete":        "#a3d991"
}


def get_label_widget(label_text):
    """
    Given a label string, return a DivWdg containing the label

    :param label_text: String
    :return: HtmlElement.label
    """

    return HtmlElement.label(label_text)


def get_select_widget_from_search_type(search_type, label, label_column, value_column, search_filters=None,
                                       search_order_bys=None):
    """
    Given a search_type, create a SelectWdg. Provide label, label_column, and value_column to set the SearchWdg
    attributes. If filters are given, apply those to the search as well.

    :param search_type: s_type ('twog/title' for example)
    :param label: String, set as 'label' on the select html element
    :param label_column: String, the database column to use for the option labels
    :param value_column: String, the database column to use for the option values
    :param search_filters: A list of tuples containing search filters (optional)
    :param search_order_bys: A list of strings corresponding to database columns to sort by (optional)
    :return: SelectWdg
    """
    search = Search(search_type)

    if search_filters:
        for search_filter in search_filters:
            filter_name = search_filter[0]
            filter_value = search_filter[1]

            try:
                filter_operator = search_filter[2]
            except IndexError:
                filter_operator = None

            if filter_operator:
                search.add_filter(filter_name, filter_value, filter_operator)
            else:
                search.add_filter(filter_name, filter_value)

    if search_order_bys:
        for search_order_by in search_order_bys:
            search.add_order_by(search_order_by)

    search_wdg = SelectWdg(label)
    search_wdg.add_empty_option('----')
    search_wdg.set_search_for_options(search, label_column=label_column, value_column=value_column)

    return search_wdg


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
        if process_xml.attrib.get('name') == process and process_xml.attrib.get('assigned_login_group') == group:
            return True
    else:
        return False


def get_assigned_group_from_xml(xml, process):
    xml_tree = ElementTree.fromstring(xml)

    for process_xml in xml_tree.iter('process'):
        if process_xml.attrib.get('name') == process:
            return process_xml.attrib.get('assigned_login_group')
    else:
        return None


def get_assigned_group_from_task(task):
    process = task.get_value('process')

    process_search = Search('config/process')
    process_search.add_filter('process', process)

    process_search_results = process_search.get_sobjects()

    if process_search_results:
        pipeline_search = Search('sthpw/pipeline')
        pipeline_search.add_filter('code', task.get_parent().get_value('pipeline_code'))

        pipeline_search_result = pipeline_search.get_sobject()

        xml = get_pipeline_xml(task.get_parent().get_value('pipeline_code'))

        if pipeline_search_result:
            return get_assigned_group_from_xml(xml, process)


def get_titles_from_order(order_code):
    """
    Using the Order's code, find all titles that are associated to it in the twog/title_order table.

    :return: A list of sobjects
    """
    titles_in_order_search = Search('twog/title_order')
    titles_in_order_search.add_filter('order_code', order_code)

    return titles_in_order_search.get_sobjects()


def get_client_name_from_code(client_code):
    """
    Get the client's name, using their code to search

    :param client_code: A unique client code
    :return: The client's name
    """
    client_search = Search('twog/client')
    client_search.add_code_filter(client_code)
    client = client_search.get_sobject()

    if client:
        return client.get('name')
    else:
        return None


def get_tasks_for_title_order(title_order):
    task_search = Search('sthpw/task')
    task_search.add_parent_filter(title_order)

    return task_search.get_sobjects()
