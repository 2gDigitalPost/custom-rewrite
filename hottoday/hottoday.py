import datetime

from pyasm.web import DivWdg, Table
from pyasm.search import Search
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from tactic_client_lib import TacticServerStub

from common_tools.utils import get_order_sobject_from_task_sobject
from order_builder.order_builder_utils import get_load_popup_widget_behavior, get_add_notes_behavior


def abbreviate_text(string, max_len):
    """
    Take a string and return an abbreviated version, cut off at max_len. Note that the "..." is factored into max_len.
    If the last character is a space, remove it.

    Examples:
    abbreviate_text("Testing this function", 8) => "Testing..."
    abbreviate_text("This is my example", 10) => "This is my..."

    :param string: A string
    :param max_len: The desired length for the abbreviated text
    :return:
    """

    if len(string) > max_len:
        abbreviated_string = string[:max_len]

        # Remove trailing space, if exists
        if abbreviated_string[-1] == ' ':
            abbreviated_string = abbreviated_string[:-1]

        return abbreviated_string + '...'
    else:
        return string


def get_scrollbar_width():
    return {'type': 'load', 'cbjs_action':
            '''
function getScrollbarWidth() {
    var outer = document.createElement("div");
    outer.style.visibility = "hidden";
    outer.style.width = "100px";
    document.body.appendChild(outer);

    var widthNoScroll = outer.offsetWidth;
    // force scrollbars
    outer.style.overflow = "scroll";

    // add innerdiv
    var inner = document.createElement("div");
    inner.style.width = "100%";
    outer.appendChild(inner);

    var widthWithScroll = inner.offsetWidth;

    // remove divs
    outer.parentNode.removeChild(outer);

    return widthNoScroll - widthWithScroll;
}

var thead = document.getElementById('thead-section');
thead.style.padding = "0px " + getScrollbarWidth() + "px 0px 0px";
            '''
            }


def get_order_builder_launch_behavior(order_search_key):
    behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var order_search_key = '%s';

    spt.tab.add_new('order_' + order_search_key, 'Order Builder', 'order_builder.OrderBuilderWdg',
                    {'search_key': order_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % order_search_key
                }
    return behavior


class HotTodayWdg(BaseRefreshWdg):
    """
    My attempt at rewriting the Hot Today table.
    """

    TASK_COLOR_DICT = {
        'pending': '#D7D7D7',
        'ready': 'B2CEE8',
        'in progress': 'F5F3A4',
        'on hold': '#E8B2B8',
        'client response': '#DDD5B8',
        'completed': '#B7E0A5',
        'need buddy check': '#E3701A',
        'internal rejection': '#FF0000',
        'external rejection': '#FF0000',
        'failed qc': '#FF0000',
        'rejected': '#FF0000',
        'fix needed': '#C466A1',
        'dr in progress': '#D6E0A4',
        'amberfin01 in progress': '#D8F1A8',
        'amberfin02 in progress': '#F3D291',
        'baton in progress': '#C6E0A4',
        'export in progress': '#796999',
        'buddy check in progress': '#1AADE3'
    }

    DATE_STATUS_COLOR = {
        'on_time': '#66DC00',
        'due_today': '#E0B600',
        'late': '#FF0000'
    }

    @staticmethod
    def get_header_groups(tasks):
        header_groups = []

        for task in tasks:
            process_name = task.get('process')

            if len(process_name.split(':')) > 1:
                group = process_name.split(':')[0]

                if group not in header_groups:
                    header_groups.append(group)

        return header_groups

    @staticmethod
    def sort_header_groups(header_groups):
        """
        Given a list of header groups, return a sorted set of those groups

        :param header_groups: List of header groups
        :return: Set (sorted)
        """
        group_order = ['MR', 'Vault', 'Onboarding', 'Compression', 'Audio', 'Localization', 'QC', 'Edel']

        header_groups_set = set(header_groups)

        sorted_header_groups_set = [group for group in group_order if group in header_groups_set]

        return sorted_header_groups_set

    @staticmethod
    def set_header(table, groups):
        """
        Construct the header for the Hot Today table, then add it to the table.

        :param table: The table to add the header to
        :param groups: The columns for the header
        :return: None
        """
        header_row = table.add_row()

        header_row.add_style('background-color', '#E0E0E0')
        header_row.add_style('width', '100%')
        header_row.add_style('display', 'table')

        # Add the title cell, it won't be included in the groups list since it should always be there by default
        title_cell = table.add_header('Order', row=header_row)
        title_cell.add_style('padding', '10px')
        title_cell.add_style('width', '24%')
        title_cell.add_style('background-color', '#F2F2F2')
        title_cell.add_style('border', '1px solid #E0E0E0')

        for group in groups:
            group_cell = table.add_header(group.title(), row=header_row)
            group_cell.add_style('padding', '10px')
            group_cell.add_style('background-color', '#F2F2F2')
            group_cell.add_style('border', '1px solid #E0E0E0')
            group_cell.add_style('width', '{0}%'.format(76.0 / len(groups)))

    @staticmethod
    def set_extra_info_row(info_text, color, table):
        extra_info_row = table.add_row()
        extra_info_row.add_style('color', color)
        extra_info_row.add_style('font-size', '14px')
        extra_info_row.add_style('font-weight', 'bold')

        table.add_cell(data=info_text, row=extra_info_row)

    def set_row(self, order, table, counter, header_groups, tasks):
        order_name = order.get('name')
        order_code = order.get('code')
        division_code = order.get('division_code')
        due_date = order.get('due_date')

        order_table = Table()
        order_table.add_style('width', '100%')

        name_row = order_table.add_row()
        name_row.add_style('font-size', '14px')
        name_row.add_style('font-weight', 'bold')

        name_data = '<span style="color: #FF0000">{0}.</span> <u>{1}</u>'.format(counter, order_name)

        order_table.add_cell(data=name_data, row=name_row, css='order-row')

        code_row = order_table.add_row()
        code_row.add_style('font-size', '12px')

        code_cell = order_table.add_cell(data='<strong>Order code:</strong> {0}'.format(order_code), row=code_row)
        code_cell.add_style('padding-top', '3px')
        code_cell.add_style('padding-bottom', '3px')
        code_cell.add_style('padding-left', '3px')

        division_row = order_table.add_row()

        division_search = Search('twog/division')
        division_search.add_code_filter(division_code)
        division = division_search.get_sobject()

        # TODO: Find the division image
        division_data = '<b>Division:</b> {0}'.format(division.get('name'))

        order_table.add_cell(data=division_data, row=division_row)

        date_row = order_table.add_row()
        due_date_data = '<b>Due:</b> {0}'.format(due_date)
        order_table.add_cell(data=due_date_data, row=date_row)

        # Add the buttons for the Order
        button_row = order_table.add_row()

        order_builder_button = ButtonNewWdg(title='Order Builder', icon='WORK')
        order_builder_button.add_behavior(get_order_builder_launch_behavior(order.get('__search_key__')))

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(get_add_notes_behavior(order.get('__search_key__')))
        note_button.add_style('display', 'inline-block')

        order_table.add_cell(data=order_builder_button, row=button_row)
        order_table.add_cell(data=note_button, row=button_row)

        current_row = table.add_row()
        current_row.add_style('width', '100%')
        current_row.add_style('vertical-align', 'top')

        order_cell_background_color = '#D7D7D7'

        order_cell = table.add_cell(order_table, row=current_row)
        order_cell.add_style('background-color', order_cell_background_color)
        order_cell.add_style('border', '1px solid #EEE')
        order_cell.add_style('padding', '4px')
        order_cell.add_style('width', '24%')

        for column in header_groups:
            if tasks:
                column_tasks = tasks.get(column)
            else:
                column_tasks = []

            if column_tasks:
                task_table = Table()
                task_table.add_style('width', '100%')
                task_table.add_style('font-size', '10px')

                for task in column_tasks:
                    current_task_row = task_table.add_row()
                    current_task_row.add_style('background-color',
                                               self.TASK_COLOR_DICT.get(task.get_value('status').lower(), '#FFFFFF'))
                    current_task_row.add_style('padding', '3px')
                    current_task_row.add_style('min-height', '20px')
                    current_task_row.add_style('border-top-left-radius', '10px')
                    current_task_row.add_style('border-bottom-left-radius', '10px')

                    inspect_button = ButtonNewWdg(title='Task Inspect', icon='WORK')
                    inspect_button.add_behavior(get_load_popup_widget_behavior('Task Inspect',
                                                                               'widgets.TaskInspectWdg',
                                                                               task.get_search_key(),
                                                                               width=600, height=600))
                    task_table.add_cell(data=inspect_button, row=current_task_row)

                    # Each task in the row will have the following properties to be displayed
                    cell_names = ['process', 'status']

                    # Add each property from left to right in the current task row. Abbreviate the text to make it
                    # fit better
                    for cell_name in cell_names:
                        task_table.add_cell(data=abbreviate_text(task.get_value(cell_name), 15), row=current_task_row)

                row_cell = table.add_cell(task_table)
                row_cell.add_style('border', '1px solid #EEE')
                row_cell.add_style('vertical-align', 'top')
                row_cell.add_style('width', '{0}%'.format(76.0 / len(header_groups)))
            else:
                table.add_cell()

    @staticmethod
    def set_priority_row(table, priority):
        """
        Set the row showing the priority of the titles. This appears above a title row, and simply displays a decimal
        number corresponding to the following titles' priority.

        :param table: The "Hot Today" table
        :param priority: The priority of the following items (decimal)
        :return: None
        """
        current_row = table.add_row()
        current_row.add_style('width', '100%')
        current_row.add_style('height', 'auto')

        priority_row = table.add_cell(priority, row=current_row)
        priority_row.add_style('background-color', '#DCE3EE')

    @staticmethod
    def get_component_or_package_list(order_list, search_type):
        order_codes = []

        for order in order_list:
            order_codes.append("'{0}'".format(order.get('code')))

        if not order_codes:
            return []

        order_codes_string = ','.join(order_codes)

        search = Search(search_type)
        search.add_where('\"order_code\" in ({0})'.format(order_codes_string))

        packages = search.get_sobjects()

        return packages

    @staticmethod
    def get_tasks_for_search_type(sobject_list, search_type):
        codes = []

        for sobject in sobject_list:
            codes.append("'{0}'".format(sobject.get_code()))

        if not codes:
            return []

        codes_string = ','.join(codes)

        tasks_search = Search('sthpw/task')
        tasks_search.add_filter('search_type', search_type)
        tasks_search.add_filter('status', 'Complete', op='!=')
        tasks_search.add_where('\"search_code\" in ({0})'.format(codes_string))

        tasks = tasks_search.get_sobjects()

        return tasks

    def get_display(self):
        table = Table()
        table.add_attr('id', 'hot_today')
        table.add_style('width', '100%')
        table.add_style('background-color', '#FCFCFC')
        table.add_style('font-size', '12px')
        table.add_style('font-family', 'Helvetica')
        table.add_border(style='solid', color='#F2F2F2', size='1px')

        # Because Tactic doesn't allow for the <thead> element (that I know of), the table header has to be split
        # into it's own <tbody>. Highly inelegant, but I don't have a choice.
        header_body = table.add_tbody()
        header_body.add_attr('id', 'thead-section')

        # Initialize the Tactic server
        server = TacticServerStub.get()

        # Get today's date as a string
        todays_date = datetime.datetime.today()
        due_date_string = todays_date.strftime('%Y-%m-%d')

        # Search for orders that are either due today or are past due.
        orders_due_today_or_earlier_list = server.eval(
            "@SOBJECT(twog/order['due_date', 'is before', '{0}']['@ORDER_BY', 'due_date asc'])".format(
                due_date_string))

        orders_due_today_or_earlier_not_complete_list = [
            order for order in orders_due_today_or_earlier_list if order.get('status') != 'complete'
        ]

        components_list = self.get_component_or_package_list(orders_due_today_or_earlier_not_complete_list,
                                                             'twog/component')
        packages_list = self.get_component_or_package_list(orders_due_today_or_earlier_not_complete_list,
                                                           'twog/package')

        task_list = self.get_tasks_for_search_type(components_list, 'twog/component?project=twog')
        task_list.extend(self.get_tasks_for_search_type(packages_list, 'twog/package?project=twog'))

        header_groups = self.get_header_groups(task_list)

        # Get the header groups as a sorted set
        header_groups = self.sort_header_groups(header_groups)

        self.set_header(table, header_groups)

        hotlist_body = table.add_tbody()
        hotlist_body.add_style('display', 'table')
        hotlist_body.add_style('overflow-x', 'hidden')
        hotlist_body.add_style('overflow-y', 'scroll')
        hotlist_body.add_style('height', '850px')
        hotlist_body.add_style('width', '100%')
        hotlist_body.add_attr('id', 'hotlist-body')

        dictionary_of_tasks = {}

        for task in task_list:
            order_sobject = get_order_sobject_from_task_sobject(task)
            order_code = order_sobject.get_code()

            process_name = task.get('process')

            if len(process_name.split(':')) > 1:
                task_header = process_name.split(':')[0]

            if order_code not in dictionary_of_tasks.keys():
                dictionary_of_tasks[order_code] = {task_header: None}

            if not dictionary_of_tasks[order_code].get(task_header):
                dictionary_of_tasks[order_code][task_header] = [task]
            else:
                dictionary_of_tasks[order_code][task_header].append(task)

        counter = 1

        for hot_item in orders_due_today_or_earlier_not_complete_list:
            # Get the tasks that correspond to a title by comparing the task's title_code to the title's code
            item_tasks = dictionary_of_tasks.get(hot_item.get('code'))

            if item_tasks:
                self.set_row(hot_item, table, counter, header_groups, item_tasks)

                counter += 1

        # Put the table in a DivWdg, makes it fit better with the Tactic side bar
        hotlist_div = DivWdg()
        hotlist_div.add_attr('id', 'hotlist_div')
        hotlist_div.add_attr('overflow', 'hidden')

        hotlist_div.add(table)

        # Add an 'outer' div that holds the hotlist div, with the buttons below.
        outer_div = DivWdg()
        outer_div.add(hotlist_div)
        outer_div.add_behavior(get_scrollbar_width())

        return outer_div
