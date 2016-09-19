from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement

import order_builder.order_builder_utils as obu

from common_tools import get_task_data_sobject_from_task_code, get_task_data_equipment, get_task_data_in_files,\
    get_task_data_out_files


def get_page_header(string):
    """
    Given a string, return a DivWdg containing the string in an H1 tag

    :param string: String
    :return: HtmlElement.label
    """

    return HtmlElement.h2(string)


def get_in_files_list(task_data_code):
    in_files_list = get_task_data_in_files(task_data_code)

    div_wdg = DivWdg()

    if in_files_list:
        div_wdg.add('<u>Input Files</u>')
        in_files_unordered_html_list = HtmlElement.ul()

        for file_path in sorted([in_file.get('file_path') for in_file in in_files_list]):
            file_li = HtmlElement.li()
            file_li.add(file_path)
            in_files_unordered_html_list.add(file_li)

        div_wdg.add(in_files_unordered_html_list)
    else:
        div_wdg.add('No input files exist for this task')

    return div_wdg


def get_out_files_list(task_data_code):
    out_files_list = get_task_data_out_files(task_data_code)

    div_wdg = DivWdg()

    if out_files_list:
        div_wdg.add('<u>Output Files</u>')
        out_files_unordered_html_list = HtmlElement.ul()

        for file_path in sorted([out_file.get('file_path') for out_file in out_files_list]):
            file_li = HtmlElement.li()
            file_li.add(file_path)
            out_files_unordered_html_list.add(file_li)

        div_wdg.add(out_files_unordered_html_list)
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

        div_wdg.add(self.parse_instruction_text(instructions.encode('utf-8')))

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

        move_input_file_to_output_button = ButtonNewWdg(title='Move Input File to Output', icon='RIGHT')
        move_input_file_to_output_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Move Input File to Output', 'widgets.MoveInputFileToOutputWdg', self.task_sobject.get_search_key(),
                'Task', 'widgets.TaskInspectWdg', self.task_sobject.get_search_key()
            )
        )
        move_input_file_to_output_button.add_style('display', 'inline-block')

        add_equipment_button = ButtonNewWdg(title='Add Equipment', icon='GEAR')
        add_equipment_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior('Add Equipment', 'widgets.EquipmentInTaskWdg',
                                                           self.task_sobject.get_search_key(), 'Task',
                                                           'widgets.TaskInspectWdg', self.task_sobject.get_search_key())
        )
        add_equipment_button.add_style('display', 'inline-block')

        div_wdg.add(add_input_file_button)
        div_wdg.add(add_output_file_button)
        div_wdg.add(move_input_file_to_output_button)
        div_wdg.add(add_equipment_button)

        return div_wdg
