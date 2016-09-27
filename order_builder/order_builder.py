import widgets.html_widgets
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, SpanWdg

import order_builder_utils as obu

from common_tools.utils import get_task_data_in_files, get_task_data_out_files, get_task_data_equipment, \
    get_files_for_package


def get_task_data_div(task_code):
    outer_div = DivWdg()

    task_data_search = Search('twog/task_data')
    task_data_search.add_filter('task_code', task_code)
    task_data = task_data_search.get_sobject()

    in_files_list = get_task_data_in_files(task_data.get_code())
    out_files_list = get_task_data_out_files(task_data.get_code())
    equipment_list = get_task_data_equipment(task_data.get_code())

    if in_files_list:
        outer_div.add(widgets.html_widgets.get_label_widget('In Files:'))

        unordered_html_list = HtmlElement.ul()

        for file_path in [in_file.get('file_path') for in_file in in_files_list]:
            li = HtmlElement.li()
            li.add(file_path)
            unordered_html_list.add(li)

        outer_div.add(unordered_html_list)

    if out_files_list:
        outer_div.add(widgets.html_widgets.get_label_widget('Out Files:'))

        unordered_html_list = HtmlElement.ul()

        for file_path in [out_file.get('file_path') for out_file in out_files_list]:
            li = HtmlElement.li()
            li.add(file_path)
            unordered_html_list.add(li)

        outer_div.add(unordered_html_list)

    if equipment_list:
        outer_div.add(widgets.html_widgets.get_label_widget('Equipment:'))

        unordered_html_list = HtmlElement.ul()

        for name in [equipment.get('name') for equipment in equipment_list]:
            li = HtmlElement.li()
            li.add(name)
            unordered_html_list.add(li)

        outer_div.add(unordered_html_list)

    return outer_div


def get_load_assign_tasks_wdg(search_key):
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
var popup_id = 'Add Tasks to Selected';
var class_name = 'tactic.ui.app.AddTaskWdg';
var task_search_key = '%s';

var options = {'search_key_list': [task_search_key], 'table_id': 'Add Tasks'};
spt.panel.load_popup(popup_id, class_name, options);
''' % search_key
    }

    return behavior


class OrderBuilderWdg(BaseRefreshWdg):
    """
    My attempt at rewriting the Order Builder module.
    """

    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

    def setup_order_information(self):
        """
        Set up a div widget to go at the top of the page. It will hold information about the order, including it's
        name, the client, and PO number, if it exists.

        :return: DivWdg
        """

        order_div = DivWdg()

        # Show some information for the order at the top.
        order_name = self.order_sobject.get('name')
        division_name = obu.get_division_name_from_code(self.order_sobject.get('division_code'))
        client_name = obu.get_client_name_from_division_code(self.order_sobject.get('division_code'))
        po_number = self.order_sobject.get_value('po_number') or 'None'
        description = self.order_sobject.get('description')

        order_name_div = DivWdg()
        order_name_div.add_style('text-decoration', 'underline')
        order_name_div.add_style('font-size', '24px')
        order_name_div.add('Order: ' + order_name)

        client_name_div = DivWdg()

        if division_name:
            client_text = 'Client: ' + division_name

            if client_name:
                client_text += ' - ' + client_name
        else:
            client_text = 'No Client Selected'

        client_name_div.add(client_text)

        po_number_div = DivWdg()
        po_number_div.add('PO Number: ' + po_number)

        description_div = DivWdg()
        description_div.add_style('font-style', 'italic')

        if description:
            description_div.add('Description: ' + description)
        else:
            description_div.add('No description available')

        add_packages_button = ButtonNewWdg(title='Add Package', icon='INSERT')
        add_packages_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior('Insert Package', 'order_builder.InsertPackageInOrderWdg',
                                                           self.order_sobject.get_search_key(), 'Order Builder',
                                                           'order_builder.OrderBuilderWdg',
                                                           self.order_sobject.get_search_key())
        )

        add_packages_button.add_style('display', 'inline-block')

        add_packages_by_platform = ButtonNewWdg(title='Add Package By Platform', icon='INSERT_MULTI')
        add_packages_by_platform.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior('Insert Packages by Platform',
                                                           'order_builder.InsertPackageByPlatformWdg',
                                                           self.order_sobject.get_search_key(), 'Order Builder',
                                                           'order_builder.OrderBuilderWdg',
                                                           self.order_sobject.get_search_key())
        )
        add_packages_by_platform.add_style('display', 'inline-block')

        add_component_button = ButtonNewWdg(title='Add Component', icon='INSERT')
        add_component_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Insert Component', 'order_builder.InsertComponentInOrderWdg', self.order_sobject.get_search_key(),
                'Order Builder', 'order_builder.OrderBuilderWdg', self.order_sobject.get_search_key()
            )
        )
        add_component_button.add_style('display', 'inline-block')

        add_component_by_language_button = ButtonNewWdg(title='Add Component By Language', icon='INSERT_MULTI')
        add_component_by_language_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Insert Component by Language', 'order_builder.InsertComponentByLanguageWdg',
                self.order_sobject.get_search_key(), 'Order Builder', 'order_builder.OrderBuilderWdg',
                self.order_sobject.get_search_key()
            )
        )
        add_component_by_language_button.add_style('display', 'inline-block')

        add_file_to_order_button = ButtonNewWdg(title='Add Files to Order', icon='ADD')
        add_file_to_order_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Add Files to Order', 'widgets.AddFilesToOrderWdg', self.order_sobject.get_search_key(),
                'Order Builder', 'order_builder.OrderBuilderWdg', self.order_sobject.get_search_key()
            )
        )
        add_file_to_order_button.add_style('display', 'inline-block')

        create_file_for_order_button = ButtonNewWdg(title='Create a new File for this Order', icon='NEW')
        create_file_for_order_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Create a new File for this Order', 'widgets.CreateFileForOrderWdg',
                self.order_sobject.get_search_key(), 'Order Builder', 'order_builder.OrderBuilderWdg',
                self.order_sobject.get_search_key()
            )
        )
        create_file_for_order_button.add_style('display', 'inline-block')

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(obu.get_add_notes_behavior(self.order_sobject.get_search_key()))
        note_button.add_style('display', 'inline-block')

        # Add the divs to the outer_div for display
        order_div.add(order_name_div)
        order_div.add(client_name_div)
        order_div.add(po_number_div)
        order_div.add(description_div)
        order_div.add(add_packages_button)
        order_div.add(add_packages_by_platform)
        order_div.add(add_component_button)
        order_div.add(add_component_by_language_button)
        order_div.add(add_file_to_order_button)
        order_div.add(create_file_for_order_button)
        order_div.add(note_button)

        return order_div

    def get_task_div(self, task):
        """
        Take a task object and set up the Div to display it.

        :param task: sthpw/task object
        :return: DivWdg
        """

        task_div = DivWdg()
        task_div.add_style('display', 'inline-block')
        task_div.add_style('background-color', '#F2F2F2')
        task_div.add_style('padding-left', '10px')
        task_div.add_style('padding-top', '10px')
        task_div.add_style('border-radius', '10px')
        task_div.add_style('width', '100%')

        process_div = DivWdg()
        process_div.add_style('font-weight', 'bold')
        process_div.add(task.get('process'))

        status_div = DivWdg()
        status_span = SpanWdg()
        status = task.get('status')
        status_span.add(status)

        if status in obu.TASK_COLORS.keys():
            status_span.add_style('color', obu.TASK_COLORS.get(status))

        status_div.add('Status: ')
        status_div.add(status_span)

        priority_div = DivWdg()
        priority_div.add('Priority: ' + str(task.get('priority')))

        assigned_div = DivWdg()
        assigned_div.add_style('font-style', 'italic')
        assigned = task.get('assigned')

        if assigned:
            assigned_div.add('Assigned to: ' + assigned)
        else:
            assigned_div.add('Not yet assigned')

        department_div = DivWdg()
        department_div.add_style('font-style', 'italic')
        department = obu.get_assigned_group_from_task(task)

        if department:
            department_div.add('Department: ' + department)
        else:
            department_div.add('No department assigned')

        task_data_div = get_task_data_div(task.get_code())

        instructions_button = ButtonNewWdg(title='Instructions', icon='CONTENTS')
        instructions_button.add_behavior(obu.load_task_instructions_behavior(task.get_search_key()))

        inspect_button = ButtonNewWdg(title='Inspect', icon='WORK')
        inspect_button.add_behavior(obu.load_task_inspect_widget(task.get_search_key()))

        equipment_button = ButtonNewWdg(title='Equipment', icon='EQUIPMENT')
        equipment_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior('Equipment', 'widgets.EquipmentInTaskWdg',
                                                           task.get_search_key(), 'Order Builder',
                                                           'order_builder.OrderBuilderWdg',
                                                           self.order_sobject.get_search_key()))

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(obu.get_add_notes_behavior(task.get_search_key()))
        note_button.add_style('display', 'inline-block')

        task_div.add(process_div)
        task_div.add(status_div)
        task_div.add(priority_div)
        task_div.add(assigned_div)
        task_div.add(department_div)
        task_div.add(task_data_div)
        task_div.add(instructions_button)
        task_div.add(inspect_button)
        task_div.add(equipment_button)
        task_div.add(note_button)

        return task_div

    def setup_html_list_for_components_in_order(self):
        components_list = HtmlElement.ul()
        components_list.add_style('list-style-type', 'none')

        component_search = Search('twog/component')
        component_search.add_filter('order_code', self.order_sobject.get_code())
        components = component_search.get_sobjects()

        for component in components:
            component_name_div = DivWdg()
            component_name_div.add_style('font-weight', 'bold')
            component_name_div.add(component.get('name'))

            component_title_div = DivWdg()
            component_title_div.add_style('text-decoration', 'underline')
            component_title = obu.get_sobject_name_by_code('twog/title', component.get('title_code'))

            if component_title:
                component_title_div.add('Title: {0}'.format(component_title))
            else:
                component_title_div.add('No Title Selected')

            component_description_div = DivWdg()
            component_description_div.add_style('font-style', 'italic')
            component_description_div.add(component.get('description'))

            component_priority_div = DivWdg()
            component_priority_div.add(component.get('priority'))

            component_pipeline_div = DivWdg()
            component_pipeline_name = obu.get_sobject_name_by_code('sthpw/pipeline', component.get('pipeline_code'))

            if component_pipeline_name:
                component_pipeline_div.add('Pipeline: <i>{0}</i>'.format(component_pipeline_name))
            else:
                component_pipeline_div.add('<i>No Pipeline Assigned</i>')

            component_language_div = DivWdg()
            component_language = obu.get_sobject_name_by_code('twog/language', component.get_value('language_code'))

            if component_language:
                component_language_div.add('Language: <i>{0}</i>'.format(component_language))
            else:
                component_language_div.add('<i>No language selected</i>')

            component_div = DivWdg()
            component_div.add_style('background-color', '#d9edcf')
            component_div.add_style('padding', '10px')
            component_div.add_style('border-radius', '10px')

            component_div.add(component_name_div)
            component_div.add(component_title_div)
            component_div.add(component_description_div)
            component_div.add(component_priority_div)
            component_div.add(component_pipeline_div)
            component_div.add(component_language_div)

            instructions_button = ButtonNewWdg(title='Instructions', icon='CONTENTS')
            instructions_button.add_behavior(
                obu.get_load_popup_widget_behavior('Component Instructions',
                                                   'order_builder.ComponentInstructionsWdg',
                                                   component.get_search_key()))
            instructions_button.add_style('display', 'inline-block')

            change_instructions_button = ButtonNewWdg(title='Change Instructions', icon='DOCUMENTATION')
            change_instructions_button.add_behavior(
                obu.get_load_popup_widget_with_reload_behavior(
                    'Change Instructions', 'order_builder.ChangeInstructionsWdg', component.get_search_key(),
                    'Order Builder', 'order_builder.OrderBuilderWdg', self.order_sobject.get_search_key()
                )
            )
            change_instructions_button.add_style('display', 'inline-block')

            change_title_button = ButtonNewWdg(title='Change Title', icon='')
            change_title_button.add_behavior(
                obu.get_load_popup_widget_with_reload_behavior(
                    'Change Title', 'order_builder.ChangeTitleWdg', component.get_search_key(),
                    'Order Builder', 'order_builder.OrderBuilderWdg', self.order_sobject.get_search_key()
                )
            )
            change_title_button.add_style('display', 'inline-block')

            add_tasks_from_pipeline_wdg = ButtonNewWdg(title='Add Tasks from Pipeline', icon='INSERT_MULTI')
            add_tasks_from_pipeline_wdg.add_behavior(get_load_assign_tasks_wdg(component.get_search_key()))
            add_tasks_from_pipeline_wdg.add_style('display', 'inline-block')

            add_task_button = ButtonNewWdg(title='Add Task', icon='INSERT')
            add_task_button.add_behavior(obu.get_load_popup_widget_behavior('Add Task',
                                                                            'order_builder.InsertTaskWdg',
                                                                            component.get_search_key()))
            add_task_button.add_style('display', 'inline-block')

            note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
            note_button.add_behavior(obu.get_add_notes_behavior(component.get_search_key()))
            note_button.add_style('display', 'inline-block')

            button_row_div = SpanWdg()
            button_row_div.add_style('display', 'inline-block')
            button_row_div.add(instructions_button)
            button_row_div.add(change_instructions_button)
            button_row_div.add(change_title_button)
            button_row_div.add(add_tasks_from_pipeline_wdg)
            button_row_div.add(add_task_button)
            button_row_div.add(note_button)

            component_div.add(button_row_div)

            tasks = component.get_all_children('sthpw/task')

            component_task_div = DivWdg()
            component_task_div.add_style('width', '100%')
            component_task_div.add_style('margin-left', '30px')

            # If there are tasks associated with the component, add them as a sub-list below it
            if tasks:
                task_list = DivWdg()

                for task in tasks:
                    task_div = DivWdg()
                    task_div.add(self.get_task_div(task))
                    task_list.add(task_div)

                component_task_div.add(task_list)

            component_outer_div = DivWdg()
            component_outer_div.add(component_div)
            component_outer_div.add(component_task_div)

            components_list.add(component_outer_div)

        return components_list

    def setup_html_list_for_packages_in_orders(self):
        """
        Add the packages that go into the order to an HTML style unordered list

        :return: HtmlElement.ul containing the packages
        """

        packages_list = HtmlElement.ul()
        packages_list.add_style('list-style-type', 'none')

        for package in obu.get_packages_from_order(self.order_sobject.get_code()):
            package_div = DivWdg()
            package_div.add_style('background-color', '#d9edf7')
            package_div.add_style('padding', '10px')
            package_div.add_style('border-radius', '10px')

            package_name_div = DivWdg()
            package_name_div.add_style('font-weight', 'bold')
            package_name_div.add(package.get('name'))

            package_description_div = DivWdg()
            package_description_div.add_style('font-style', 'italic')
            package_description_div.add(package.get('description'))

            package_priority_div = DivWdg()
            package_priority_div.add('Priority: {0}'.format(package.get('priority')))

            package_platform_div = DivWdg()
            platform_code = package.get('platform_code')

            if platform_code:
                platform = obu.get_platform(platform_code)

                if platform:
                    package_platform_div.add('Platform: {0}'.format(platform.get('name')))

            package_due_date_div = DivWdg()

            if package.get('due_date'):
                package_due_date_div.add('Due: {0}'.format(package.get('due_date')))

            add_deliverable_file_to_package_button = ButtonNewWdg(title='Add Deliverable File', icon='ADD')
            add_deliverable_file_to_package_button.add_behavior(
                obu.get_load_popup_widget_with_reload_behavior(
                    'Add Deliverable Files', 'widgets.AddDeliverableFilesToPackageWdg', package.get_search_key(),
                    'Order Builder', 'order_builder.OrderBuilderWdg', self.order_sobject.get_search_key()
                )
            )
            add_deliverable_file_to_package_button.add_style('display', 'inline-block')

            note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
            note_button.add_behavior(obu.get_add_notes_behavior(package.get_search_key()))
            note_button.add_style('display', 'inline-block')

            button_row_div = SpanWdg()
            button_row_div.add_style('display', 'inline-block')
            button_row_div.add(add_deliverable_file_to_package_button)
            button_row_div.add(note_button)

            package_div.add(package_name_div)
            package_div.add(package_description_div)
            package_div.add(package_priority_div)
            package_div.add(package_due_date_div)
            package_div.add(package_platform_div)

            files_in_package_list = get_files_for_package(package.get_code())

            if files_in_package_list:
                package_div.add(widgets.html_widgets.get_label_widget('Deliverable Files:'))

                unordered_html_list = HtmlElement.ul()

                for file_path in [file_in_package.get('file_path') for file_in_package in files_in_package_list]:
                    li = HtmlElement.li()
                    li.add(file_path)
                    unordered_html_list.add(li)

                    package_div.add(unordered_html_list)

            package_div.add(button_row_div)

            package_list_div = DivWdg()
            package_list_div.add(package_div)

            packages_list.add(package_list_div)

        return packages_list

    @staticmethod
    def get_external_rejection_button_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Set External Rejection', 'order_builder.ExternalRejectionOnTitleOrderWdg');
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}'''
        }

        return behavior

    @staticmethod
    def get_upload_button_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Upload', 'tactic.ui.input.Html5UploadWdg');
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}'''
        }

        return behavior

    @staticmethod
    def get_element_evaluation_button_behavior(title_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Element Evaluation', 'qc_reports.ElementEvalWdg', {'title_code': '%s'});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
        }''' % title_code
        }

        return behavior

    @staticmethod
    def get_component_instructions_wdg(search_key):
        """
        Load the instructions for the component.

        :param search_key: Component's search key (unique ID)
        :return: Behavior (Instructions Widget)
        """
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Instructions', 'order_builder.ComponentInstructionsWdg', {'search_key': '%s'});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % search_key
        }

        return behavior

    @staticmethod
    def get_change_due_date_behavior(code, due_date):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Instructions', 'order_builder.ChangeDueDateWdg', {'title_order_code': '%s', 'due_date': '%s'});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (code, due_date)
        }

        return behavior

    @staticmethod
    def get_add_task_behavior(title_order_search_key):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Instructions', 'order_builder.AddTaskToTitleOrderWdg', {'title_order_search_key': '%s'});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % title_order_search_key
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.add_class('order-builder')
        outer_div.add_style('display', 'inline-block')

        order_div = DivWdg()

        order_div.add(self.setup_order_information())

        components_div = DivWdg()
        components_div.add_style('display', 'inline-block')
        components_div.add_style('width', '600px')
        components_div.add_style('float', 'left')
        components_div.add(self.setup_html_list_for_components_in_order())
        order_div.add(components_div)

        packages_div = DivWdg()
        packages_div.add_style('display', 'inline-block')
        packages_div.add_style('width', '600px')
        packages_div.add_style('float', 'left')
        packages_div.add(self.setup_html_list_for_packages_in_orders())
        order_div.add(packages_div)

        outer_div.add(order_div)

        return outer_div
