from xml.etree import ElementTree

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement
from pyasm.widget import SelectWdg, TextAreaWdg

from tactic.ui.input import TextInputWdg
from tactic.ui.widget import CalendarInputWdg

from tactic_client_lib import tactic_server_stub


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


def get_widget_header(text):
    """
    Given a string, return a DivWdg containing the label, bolded and underlined

    :param text: String
    :return: DivWdg
    """

    div = DivWdg(text)

    div.add_style('font-weight', 'bold')
    div.add_style('text-decoration', 'underline')

    return div


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


def get_next_tasks_codes_from_xml(xml, process):
    xml_tree = ElementTree.fromstring(xml)

    connected_processes = []

    for connect_xml in xml_tree.iter('connect'):
        if connect_xml.attrib.get('from') == process:
            connected_processes.append(connect_xml.attrib.get('to'))


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


def get_packages_from_order(order_code):
    """
    Using the Order's code, find all packages that are associated to it.

    :return: A list of sobjects (packages)
    """
    packages_search = Search('twog/package')
    packages_search.add_filter('order_code', order_code)

    return packages_search.get_sobjects()


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


def get_division_name_from_code(division_code):
    """
    Get the client division's name, using their code to search

    :param division_code: A unique division code
    :return: The division's name
    """
    division_search = Search('twog/division')
    division_search.add_code_filter(division_code)
    division = division_search.get_sobject()

    if division:
        return division.get('name')
    else:
        return None


def get_client_name_from_division_code(division_code):
    """
    Get the name of the client that owns the division.

    :param division_code: A unique division code
    :return: The client's name
    """
    division_search = Search('twog/division')
    division_search.add_code_filter(division_code)
    division = division_search.get_sobject()

    if division:
        client_search = Search('twog/client')
        client_search.add_code_filter(division.get('client_code'))
        client = client_search.get_sobject()

        if client:
            return client.get('name')

    return None


def get_tasks_for_component(component):
    """
    Get all the tasks associated with a component

    :param component: Component sobject (twog/component)
    :return: Sobject list
    """
    task_search = Search('sthpw/task')
    task_search.add_parent_filter(component)

    return task_search.get_sobjects()


def get_sobject_name_by_code(search_type, sobject_code):
    search = Search(search_type)
    search.add_code_filter(sobject_code)
    search_result = search.get_sobject()

    if search_result:
        return search_result.get_value('name')
    else:
        return None


def get_platform(platform_code):
    platform_search = Search('twog/platform')
    platform_search.add_code_filter(platform_code)

    return platform_search.get_sobject()


def get_date_calendar_wdg():
    date_calendar_wdg = CalendarInputWdg("due_date")
    date_calendar_wdg.set_option('show_activator', 'true')
    date_calendar_wdg.set_option('show_time', 'false')
    date_calendar_wdg.set_option('width', '300px')
    date_calendar_wdg.set_option('id', 'due_date')
    date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

    return date_calendar_wdg


def get_server():
    """

    :return:
    """
    try:
        server = tactic_server_stub.TacticServerStub.get()
    except tactic_server_stub.TacticApiException as e:
        # TODO: get a server object some other way
        raise e

    return server


def get_base_url(server=None, project='twog'):
    """
    Gets the base url for tactic. This would be used to get the
    beginning of a custom url (like for the order_builder).

    Note: the server from the browser already has .2gdigital.com

    :param server: a TacticServerStub object
    :param project: the project as a string
    :return: the base url as a string
    """
    if not server:
        server = get_server()

    url = 'http://{0}/tactic/{1}/'.format(server.server_name, project)
    return url


def get_text_input_wdg(name, width=200):
    textbox_wdg = TextInputWdg()
    textbox_wdg.set_id(name)
    textbox_wdg.set_name(name)
    textbox_wdg.add_style('width', '{0}px'.format(width))

    return textbox_wdg


def get_text_area_input_wdg(name, width=400, styles=None):
    textarea_wdg = TextAreaWdg()
    textarea_wdg.set_id(name)
    textarea_wdg.set_name(name)
    textarea_wdg.add_style('width', '{0}px'.format(width))

    if styles is None:
        styles = []

    for style in styles:
        textarea_wdg.add_style(style[0], style[1])

    return textarea_wdg


def get_order_builder_url(order_code, server=None, project='twog'):
    """
    Gets the order builder url for the given order code.
    Note that this does not format it as a hyperlink.

    Ex. get_order_builder_url('ORDER12345')
    -> 'http://tactic01.2gdigital.com/tactic/twog/order_builder/ORDER12345'

    :param order_code: the order code as a string
    :param server: a tactic server stub object
    :param project: the project as a string
    :return: a url to the order builder page
    """
    if not server:
        server = get_server()

    base_url = get_base_url(server, project)
    return "{0}order_builder/{1}".format(base_url, order_code)


def get_add_notes_behavior(search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    spt.api.load_popup('Add Note', 'tactic.ui.widget.discussion_wdg.DiscussionWdg', {'search_key': '%s'});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % search_key
    }

    return behavior


def load_task_instructions_behavior(task_search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var task_search_key = '%s';

    spt.tab.add_new('instructions_' + task_search_key, 'Instructions', 'order_builder.TaskInstructionsWdg',
                    {'search_key': task_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % task_search_key
    }

    return behavior


def load_task_inspect_widget(task_search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var task_search_key = '%s';

    spt.tab.add_new('instructions_' + task_search_key, 'Instructions', 'widgets.TaskInspectWdg',
                    {'search_key': task_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % task_search_key
    }

    return behavior


def get_load_popup_widget_behavior(widget_title, widget_name, search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var widget_title = '%s';
    var widget_name = '%s';
    var search_key = '%s';

    spt.api.load_popup(widget_title, widget_name, {'search_key': search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (widget_title, widget_name, search_key)
    }

    return behavior


def get_load_popup_widget_with_reload_behavior(widget_title, widget_name, search_key, parent_widget_title,
                                               parent_widget_name, parent_search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var widget_title = '%s';
    var widget_name = '%s';
    var search_key = '%s';
    var parent_widget_title = '%s';
    var parent_widget_name = '%s';
    var parent_widget_search_key = '%s';

    spt.api.load_popup(widget_title, widget_name, {'search_key': search_key,
                                                   'parent_widget_title': parent_widget_title,
                                                   'parent_widget_name': parent_widget_name,
                                                   'parent_widget_search_key': parent_widget_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (widget_title, widget_name, search_key, parent_widget_title, parent_widget_name, parent_search_key)
    }

    return behavior
