from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement

import order_builder.order_builder_utils as obu

from common_tools import get_task_data_sobject_from_task_code, get_task_data_equipment


def get_page_header(string):
    """
    Given a string, return a DivWdg containing the string in an H1 tag

    :param string: String
    :return: HtmlElement.label
    """

    return HtmlElement.h2(string)


def get_in_files_list(task_data_code):
    in_files_search = Search('twog/task_data_in_file')
    in_files_search.add_filter('task_data_code', task_data_code)
    in_files = in_files_search.get_sobjects()

    div_wdg = DivWdg()
    files_list = HtmlElement.ul()

    if in_files:
        div_wdg.add('<u>Input Files</u>')

        for in_file in in_files:
            file_search = Search('twog/file')
            file_search.add_code_filter(in_file.get('file_code'))
            file_sobject = file_search.get_sobject()

            file_li = HtmlElement.li()
            file_li.add(file_sobject.get('file_path'))
            files_list.add(file_li)

        div_wdg.add(files_list)
    else:
        div_wdg.add('No input files exist for this task')

    return div_wdg


def get_out_files_list(task_data_code):
    out_files_search = Search('twog/task_data_out_file')
    out_files_search.add_filter('task_data_code', task_data_code)
    out_files = out_files_search.get_sobjects()

    div_wdg = DivWdg()
    files_list = HtmlElement.ul()

    if out_files:
        div_wdg.add('<u>Output Files</u>')

        for out_file in out_files:
            file_search = Search('twog/file')
            file_search.add_code_filter(out_file.get('file_code'))
            file_sobject = file_search.get_sobject()

            file_li = HtmlElement.li()
            file_li.add(file_sobject.get('file_path'))
            files_list.add(file_li)

        div_wdg.add(files_list)
    else:
        div_wdg.add('No output files exist for this task')

    return div_wdg


def get_equipment_list(task_data_code):
    equipment_sobjects_list = get_task_data_equipment(task_data_code)

    div_wdg = DivWdg()

    if equipment_sobjects_list:
        div_wdg.add(obu.get_label_widget('Equipment:'))
        equipment_unordered_html_list = HtmlElement.ul()

        for name in [equipment_sobject.get('name') for equipment_sobject in equipment_sobjects_list]:
            equipment_li = HtmlElement.li()
            equipment_li.add(name)
            equipment_unordered_html_list.add(equipment_li)

        div_wdg.add(equipment_unordered_html_list)
    else:
        div_wdg.add('No equipment is assigned to this task')

    return div_wdg


class TaskInspectWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())
        self.parent_component = self.task_sobject.get_parent()

    @staticmethod
    def get_instructions_for_task_name(name, instructions):
        instructions_lines = []
        within_instructions = False

        for line in instructions.split('\n'):
            if line.startswith('#'):
                if line == '# {0}'.format(name):
                    within_instructions = True
                else:
                    within_instructions = False

            if within_instructions:
                instructions_lines.append(line)

        return '\n'.join(instructions_lines[1:])

    @staticmethod
    def parse_instruction_text(instructions):
        output_html = ''

        for line in instructions.split('\n'):
            if line:
                if line[0] == '*':
                    formatted_line = '<h2>{0}</h2>'.format(line[2:])
                elif line[0] == '#':
                    formatted_line = '<h4>{0}</h4>'.format(line[2:])
                else:
                    formatted_line = '<p>{0}</p>'.format(line)

                output_html += formatted_line

        return output_html

    @staticmethod
    def get_title_order_instructions_from_task(task):
        title_order_sobject = task.get_parent()

        instructions_search = Search('twog/instructions')
        instructions_search.add_code_filter(title_order_sobject.get('instructions_code'))
        instructions = instructions_search.get_sobject()

        return instructions.get('instructions_text')

    def get_display(self):
        div_wdg = DivWdg()

        div_wdg.add(get_page_header(self.task_sobject.get('process')))
        div_wdg.add(HtmlElement.h4('Code: {0}'.format(self.task_sobject.get_code())))
        div_wdg.add(HtmlElement.h4('Component: {0} ({1})'.format(self.parent_component.get('name'),
                                                                 self.parent_component.get_code())))

        div_wdg.add(HtmlElement.h4('<u>Instructions</u>'))
        instructions = self.get_instructions_for_task_name(self.task_sobject.get_value('process'),
                                                           self.get_title_order_instructions_from_task(
                                                               self.task_sobject
                                                           ))

        if not instructions:
            instructions = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions))

        div_wdg.add(get_in_files_list(self.task_data.get_code()))
        div_wdg.add(get_out_files_list(self.task_data.get_code()))
        div_wdg.add(get_equipment_list(self.task_data.get_code()))

        add_input_file_button = ButtonNewWdg(title='Add Input Files', icon='INSERT_MULTI')
        add_input_file_button.add_behavior(
            obu.get_load_popup_widget_behavior('Add Input Files',
                                               'widgets.AddInputFilesToTaskWdg',
                                               self.task_sobject.get_search_key())
        )
        add_input_file_button.add_style('display', 'inline-block')

        add_output_file_button = ButtonNewWdg(title='Add Output Files', icon='INSERT_MULTI')
        add_output_file_button.add_behavior(
            obu.get_load_popup_widget_behavior('Add Output Files',
                                               'widgets.AddOutputFilesToTaskWdg',
                                               self.task_sobject.get_search_key())
        )
        add_output_file_button.add_style('display', 'inline-block')

        add_equipment_button = ButtonNewWdg(title='Add Equipment', icon='EQUIPMENT')
        add_equipment_button.add_behavior(
            obu.get_load_popup_widget_behavior('Add Equipment',
                                               'widgets.EquipmentInTaskWdg',
                                               self.task_sobject.get_search_key())
        )
        add_equipment_button.add_style('display', 'inline-block')

        div_wdg.add(add_input_file_button)
        div_wdg.add(add_output_file_button)
        div_wdg.add(add_equipment_button)

        return div_wdg
