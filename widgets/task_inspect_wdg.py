from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.web import DivWdg, HtmlElement
from pyasm.widget import SubmitWdg

import order_builder.order_builder_utils as obu

from common_tools import get_task_data_sobject_from_task_code, get_task_data_equipment, get_task_data_in_files,\
    get_task_data_out_files, get_task_instructions_text_from_instructions_code,\
    get_order_sobject_from_component_sobject, get_order_sobject_from_task_sobject

from widgets.html_widgets import get_page_header
from widgets.input_widgets import get_task_status_select_wdg


def load_order_builder_wdg(order_search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var task_search_key = '%s';

    spt.tab.add_new('task_inspect_' + task_search_key, 'Task', 'widgets.TaskInspectWdg',
                    {'search_key': task_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % order_search_key
    }

    return behavior


def get_in_files_list(task_data_code):
    in_files_list = get_task_data_in_files(task_data_code)

    div_wdg = DivWdg()

    if in_files_list:
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
    def parse_instruction_text(instructions):
        output_html = ''

        for line in instructions.split('\n'):
            if line:
                if line[0:3] == '!@|':
                    task_name = line.split('|')[1]
                    formatted_line = '<h4>{0}</h4>'.format(task_name)
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

    def get_buttons_row(self):
        outer_div = DivWdg()

        download_attached_files_button =  ButtonNewWdg(title='Download Attached Files', icon='DOWNLOAD')
        download_attached_files_button.add_behavior(obu.get_download_attached_files_behavior(
            self.task_sobject.get_search_key()
        ))
        download_attached_files_button.add_style('display', 'inline-block')

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(obu.get_add_notes_behavior(self.task_sobject.get_search_key()))
        note_button.add_style('display', 'inline-block')

        outer_div.add(download_attached_files_button)
        outer_div.add(note_button)

        return outer_div

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

        load_order_builder_button = ButtonNewWdg(title='Load Order', icon='WORK')
        load_order_builder_button.add_behavior(
            obu.get_load_new_tab_behavior(
                'order_{0}'.format(order_sobject.get_code()), 'Order Builder', 'order_builder.OrderBuilderWdg',
                order_sobject.get_search_key()
            )
        )
        load_order_builder_button.add_style('display', 'inline-block')
        div_wdg.add(load_order_builder_button)

        div_wdg.add(HtmlElement.h4('<u>Status</u>'))
        div_wdg.add(get_task_status_select_wdg(self.task_sobject))

        submit_button = SubmitWdg('Submit Changes')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        div_wdg.add(submit_button)

        div_wdg.add(HtmlElement.h4('<u>Estimated Hours: {0}</u>'.format(self.task_data.get('estimated_hours'))))

        change_estimated_hours_button = ButtonNewWdg(title='Change Estimated Hours', icon='TIME')
        change_estimated_hours_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Change Estimated Hours', 'widgets.ChangeEstimatedHoursForTaskWdg', self.task_sobject.get_search_key(),
                'Task', 'widgets.TaskInspectWdg', self.task_sobject.get_search_key()
            )
        )
        change_estimated_hours_button.add_style('display', 'inline-block')
        div_wdg.add(change_estimated_hours_button)

        div_wdg.add(HtmlElement.h4('<u>Input Files</u>'))
        div_wdg.add(get_in_files_list(self.task_data.get_code()))

        add_input_file_button = ButtonNewWdg(title='Add Input Files', icon='INSERT_MULTI')
        add_input_file_button.add_behavior(
            obu.get_load_popup_widget_behavior('Add Input Files from Order',
                                               'widgets.AddInputFilesToTaskWdg',
                                               self.task_sobject.get_search_key())
        )
        add_input_file_button.add_style('display', 'inline-block')
        div_wdg.add(add_input_file_button)

        create_input_file_button = ButtonNewWdg(title='Create a new Input File', icon='ADD')
        create_input_file_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Create a new Input File', 'widgets.CreateNewInputFileForTaskWdg', self.task_sobject.get_search_key(),
                'Task', 'widgets.TaskInspectWdg', self.task_sobject.get_search_key()
            )
        )
        create_input_file_button.add_style('display', 'inline-block')
        div_wdg.add(create_input_file_button)

        div_wdg.add(HtmlElement.h4('<u>Output Files</u>'))
        div_wdg.add(get_out_files_list(self.task_data.get_code()))

        move_input_file_to_output_button = ButtonNewWdg(title='Move Input File to Output', icon='RIGHT')
        move_input_file_to_output_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Move Input File to Output', 'widgets.MoveInputFileToOutputWdg', self.task_sobject.get_search_key(),
                'Task', 'widgets.TaskInspectWdg', self.task_sobject.get_search_key()
            )
        )
        move_input_file_to_output_button.add_style('display', 'inline-block')
        div_wdg.add(move_input_file_to_output_button)

        div_wdg.add(HtmlElement.h4('<u>Equipment</u>'))
        div_wdg.add(get_equipment_list(self.task_data.get_code()))

        add_equipment_button = ButtonNewWdg(title='Add Equipment', icon='INSERT_MULTI')
        add_equipment_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior('Add Equipment', 'widgets.EquipmentInTaskWdg',
                                                           self.task_sobject.get_search_key(), 'Task',
                                                           'widgets.TaskInspectWdg', self.task_sobject.get_search_key())
        )
        add_equipment_button.add_style('display', 'inline-block')
        div_wdg.add(add_equipment_button)

        if self.parent_component.get_search_type() == u'twog/component?project=twog':
            div_wdg.add(HtmlElement.h4('<u>Instructions</u>'))

            instructions_code = self.parent_component.get('instructions_code')
            instructions = get_task_instructions_text_from_instructions_code(instructions_code,
                                                                             self.task_sobject.get('process'))

            if not instructions:
                instructions = 'Sorry, instructions have not been added yet.'

            div_wdg.add(self.parse_instruction_text(instructions.encode('utf-8')))
        elif self.parent_component.get_search_type() == u'twog/package?project=twog':
            div_wdg.add(HtmlElement.h4('<u>Instructions</u>'))

            package_instructions_code = self.parent_component.get('package_instructions_code')
            instructions = get_task_instructions_text_from_instructions_code(package_instructions_code,
                                                                             self.task_sobject.get('process'),
                                                                             package=True)

            if not instructions:
                instructions = 'Sorry, instructions have not been added yet.'

            div_wdg.add(self.parse_instruction_text(instructions.encode('utf-8')))

        div_wdg.add(self.get_buttons_row())

        return div_wdg
