from xml.etree import ElementTree

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.panel import ViewPanelWdg, FastTableLayoutWdg
from tactic.ui.table import WorkElementWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table


def get_tasks():
    task_search = Search('sthpw/task')
    task_search.add_filter('search_type', 'twog/title_order?project=twog')

    task_search_results = task_search.get_sobjects()

    return task_search_results


def get_title_order_from_code(title_order_code):
    title_order_search = Search('twog/title_order')
    title_order_search.add_filter('code', title_order_code)

    return title_order_search.get_sobject()


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


def get_edel_tasks():
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

    return final_tasks


class EdelTaskWdg(BaseTableElementWdg):
    def set_header(self, table):
        """
        Construct the table header
        """

        header_row = table.add_row()

        header_row.add_style('background-color', '#E0E0E0')
        header_row.add_style('width', '100%')

        task_cell = table.add_header('Task', row=header_row)
        status_cell = table.add_header('Status', row=header_row)
        title_order_name_cell = table.add_header('Title Order Name', row=header_row)

        self.apply_styling_to_cells([task_cell, status_cell, title_order_name_cell])

        table.add_row()

    @staticmethod
    def apply_styling_to_cells(cells):
        """
        Take a list of table cells and apply the same CSS to each of them
        """

        map(lambda cell: cell.add_style('padding: 4px'), cells)

    def get_display(self):
        table = Table()

        self.set_header(table)

        tasks = get_edel_tasks()

        for task in tasks:
            process_cell = table.add_cell(task.get_value('process'))
            
            status_cell = table.add_cell(task.get_value('status'))

            title_order = get_title_order_from_code(task.get_value('search_code'))
            if (title_order):
                title_order_cell = table.add_cell(title_order.get_value('name'))
            else:
                title_order_cell = table.add_cell()

            # work_on_task_cell = table.add_cell(WorkElementWdg(search_key='sthpw/task?code=TASK00000009'))

            # self.apply_styling_to_cells([process_cell, status_cell, title_order_cell, work_on_task_cell])
            self.apply_styling_to_cells([process_cell, status_cell, title_order_cell])

            table.add_row()

        outer_div = DivWdg()
        outer_div.add(table)

        return outer_div

"""
class EdelTaskWdg(FastTableLayoutWdg):
    def __init__(self):

        tasks = get_edel_tasks()

        self.search_type = 'sthpw/task'

        self.set_sobjects(tasks)
"""
"""
        for task in tasks:
            table.add_cell(task.get_value('process'))
            table.add_cell(task.get_value('status'))

            title_order = get_title_order_from_code(task.get_value('search_code'))
            table.add_cell(title_order.get_value('name'))

            table.add_row()
"""
