from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.web import DivWdg, HtmlElement
from pyasm.widget import SubmitWdg

import order_builder.order_builder_utils as obu

from common_tools import get_task_data_sobject_from_task_code, get_task_instructions_text_from_instructions_code,\
    get_order_sobject_from_component_sobject

from widgets.html_widgets import get_page_header
from widgets.input_widgets import get_task_status_select_wdg


class DeliveryTaskInspectWdg(BaseRefreshWdg):
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
        div_wdg.add(HtmlElement.h4('Package: {0} ({1})'.format(self.parent_component.get('name'),
                                                                 self.parent_component.get_code())))

        # Get the order that contains the parent component and display its information
        order_sobject = get_order_sobject_from_component_sobject(self.parent_component)
        div_wdg.add(HtmlElement.h4('Order: {0} ({1})'.format(order_sobject.get('name'), order_sobject.get_code())))

        div_wdg.add(HtmlElement.h4('<u>Status</u>'))
        div_wdg.add(get_task_status_select_wdg(self.task_sobject))

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

        move_input_file_to_output_button = ButtonNewWdg(title='Move Input File to Output', icon='RIGHT')
        move_input_file_to_output_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Move Input File to Output', 'widgets.MoveInputFileToOutputWdg', self.task_sobject.get_search_key(),
                'Task', 'widgets.TaskInspectWdg', self.task_sobject.get_search_key()
            )
        )
        move_input_file_to_output_button.add_style('display', 'inline-block')
        div_wdg.add(move_input_file_to_output_button)

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

            instructions = self.parent_component.get('delivery_instructions')

            if not instructions:
                instructions = 'Sorry, instructions have not been added yet.'

            div_wdg.add(self.parse_instruction_text(instructions.encode('utf-8')))

        div_wdg.add(self.get_buttons_row())

        submit_button = SubmitWdg('Submit Changes')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        div_wdg.add(submit_button)

        return div_wdg
