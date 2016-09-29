from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.biz import Pipeline
from pyasm.web import DivWdg, HtmlElement
from pyasm.widget import SelectWdg, SubmitWdg

import order_builder.order_builder_utils as obu

from widgets.html_widgets import get_label_widget

from common_tools import get_task_data_sobject_from_task_code, get_task_data_equipment, get_task_data_in_files,\
    get_task_data_out_files, get_task_instructions_text_from_instructions_code, get_order_sobject_from_component_sobject


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
        div_wdg.add(get_label_widget('Equipment:'))
        equipment_unordered_html_list = HtmlElement.ul()

        for name in [equipment_sobject.get('name') for equipment_sobject in equipment_sobjects_list]:
            equipment_li = HtmlElement.li()
            equipment_li.add(name)
            equipment_unordered_html_list.add(equipment_li)

        div_wdg.add(equipment_unordered_html_list)
    else:
        div_wdg.add('No equipment is assigned to this task')

    return div_wdg


def get_task_status_select_wdg(task_sobject):
    task_status_select = SelectWdg('task_status_select')
    task_status_select.set_id('task_status_select')
    task_status_select.add_style('width: 135px;')
    task_status_select.add_empty_option()

    task_pipe_code = task_sobject.get_value('pipeline_code')

    # if the current task has no pipeline, then search for
    # any task pipeline
    if not task_pipe_code:
        # just use the default
        task_pipe_code = 'task'

    pipeline = Pipeline.get_by_code(task_pipe_code)
    if not pipeline:
        pipeline = Pipeline.get_by_code('task')

    for status in pipeline.get_process_names():
        task_status_select.append_option(status, status)

    if task_sobject.get('status'):
        task_status_select.set_value(task_sobject.get('status'))

    return task_status_select


class TaskInspectWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())
        self.parent_component = self.task_sobject.get_parent()

    @staticmethod
    def parse_instruction_text(instructions):
        output_html = ''

        for line in instructions.split('\n'):
            if line:
                if line[0:3] == '###':
                    formatted_line = '<h4>{0}</h4>'.format(line[4:])
                else:
                    formatted_line = '<p>{0}</p>'.format(line)

                output_html += formatted_line

        return output_html

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var task_code = '%s';
var task_search_key = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#task_inspect_" + task_code);
var values = spt.api.get_input_values(containing_element, null, false);

var task_status = values["task_status_select"];

// Set up an object to hold the data
var kwargs = {
    'status': task_status
}

server.update(task_search_key, kwargs);

spt.app_busy.hide();

spt.api.load_tab('Task', 'widgets.TaskInspectWdg', {'search_key': task_search_key});
''' % (self.task_sobject.get_code(), self.task_sobject.get_search_key())
        }

        return behavior

    def get_display(self):
        div_wdg = DivWdg()
        div_wdg.set_id('task_inspect_{0}'.format(self.task_sobject.get_code()))

        div_wdg.add(get_page_header(self.task_sobject.get('process')))
        div_wdg.add(HtmlElement.h4('Code: {0}'.format(self.task_sobject.get_code())))
        div_wdg.add(HtmlElement.h4('Component: {0} ({1})'.format(self.parent_component.get('name'),
                                                                 self.parent_component.get_code())))

        # Get the order that contains the parent component and display its information
        order_sobject = get_order_sobject_from_component_sobject(self.parent_component)
        div_wdg.add(HtmlElement.h4('Order: {0} ({1})'.format(order_sobject.get('name'), order_sobject.get_code())))

        div_wdg.add(HtmlElement.h4('<u>Status</u>'))
        div_wdg.add(get_task_status_select_wdg(self.task_sobject))

        div_wdg.add(HtmlElement.h4('<u>Input Files</u>'))
        div_wdg.add(get_in_files_list(self.task_data.get_code()))

        div_wdg.add(HtmlElement.h4('<u>Output Files</u>'))
        div_wdg.add(get_out_files_list(self.task_data.get_code()))

        div_wdg.add(HtmlElement.h4('<u>Equipment</u>'))
        div_wdg.add(get_equipment_list(self.task_data.get_code()))

        div_wdg.add(HtmlElement.h4('<u>Instructions</u>'))

        instructions_code = self.parent_component.get('instructions_code')
        instructions = get_task_instructions_text_from_instructions_code(instructions_code,
                                                                         self.task_sobject.get('process'))

        if not instructions:
            instructions = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions.encode('utf-8')))

        add_input_file_button = ButtonNewWdg(title='Add Input Files', icon='INSERT_MULTI')
        add_input_file_button.add_behavior(
            obu.get_load_popup_widget_behavior('Add Input Files from Order',
                                               'widgets.AddInputFilesToTaskWdg',
                                               self.task_sobject.get_search_key())
        )
        add_input_file_button.add_style('display', 'inline-block')

        create_input_file_button = ButtonNewWdg(title='Create a new Input File', icon='NEW')
        create_input_file_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Create a new Input File', 'widgets.CreateNewInputFileForTaskWdg', self.task_sobject.get_search_key(),
                'Task', 'widgets.TaskInspectWdg', self.task_sobject.get_search_key()
            )
        )
        create_input_file_button.add_style('display', 'inline-block')

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

        submit_button = SubmitWdg('Submit Changes')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        div_wdg.add(add_input_file_button)
        div_wdg.add(create_input_file_button)
        div_wdg.add(move_input_file_to_output_button)
        div_wdg.add(add_equipment_button)
        div_wdg.add(submit_button)

        return div_wdg
