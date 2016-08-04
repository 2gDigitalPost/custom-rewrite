from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import Html5UploadWdg
from tactic.ui.table import CheckinButtonElementWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, SpanWdg

import order_builder_utils as obu


class OrderBuilderWdg(BaseRefreshWdg):
    """
    My attempt at rewriting the Order Builder module.
    """

    def init(self):
        self.order_code = self.get_kwargs().get('code')

        order_sobject_search = Search('twog/order')
        order_sobject_search.add_code_filter(self.order_code)
        self.order_sobject = order_sobject_search.get_sobject()

        self.titles_in_order = obu.get_titles_from_order(self.order_sobject.get('code'))

    def setup_order_information(self):
        """
        Set up a div widget to go at the top of the page. It will hold information about the order, including it's
        name, the client, and PO number, if it exists.

        :return: DivWdg
        """

        order_div = DivWdg()

        # Show some information for the order at the top.
        order_name = self.order_sobject.get('name')
        client_name = obu.get_client_name_from_code(self.order_sobject.get('client_code'))
        po_number = self.order_sobject.get_value('po_number') or 'None'
        description = self.order_sobject.get('description')

        order_name_div = DivWdg()
        order_name_div.add_style('text-decoration', 'underline')
        order_name_div.add_style('font-size', '24px')
        order_name_div.add('Order: ' + order_name)

        client_name_div = DivWdg()
        client_name_div.add('Client: ' + client_name)

        po_number_div = DivWdg()
        po_number_div.add('PO Number: ' + po_number)

        description_div = DivWdg()
        description_div.add_style('font-style', 'italic')

        if description:
            description_div.add('Description: ' + description)
        else:
            description_div.add('No description available')

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(obu.get_add_notes_behavior(self.order_sobject.get_search_key()))

        # Add the divs to the outer_div for display
        order_div.add(order_name_div)
        order_div.add(client_name_div)
        order_div.add(po_number_div)
        order_div.add(description_div)
        order_div.add(note_button)
        order_div.add(HtmlElement.br)

        return order_div

    @staticmethod
    def get_task_div(task):
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

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(obu.get_add_notes_behavior(task.get_search_key()))

        task_div.add(process_div)
        task_div.add(status_div)
        task_div.add(priority_div)
        task_div.add(assigned_div)
        task_div.add(department_div)
        task_div.add(note_button)

        return task_div

    def setup_html_list_for_title_orders(self):
        """
        Add the titles that go into the order to an HTML style unordered list

        :return: HtmlElement.ul containing the titles
        """

        title_order_list = HtmlElement.ul()
        title_order_list.add_style('list-style-type', 'none')

        for title_order in self.titles_in_order:
            title_order_name_div = DivWdg()
            title_order_name_div.add_style('font-weight', 'bold')
            title_order_name_div.add(title_order.get('name'))

            title_order_description_div = DivWdg()
            title_order_description_div.add_style('font-style', 'italic')
            title_order_description_div.add(title_order.get('description'))

            title_order_priority_div = DivWdg()
            title_order_priority_div.add('Priority: {0}'.format(title_order.get('priority')))

            title_order_due_date_div = DivWdg()

            if title_order.get('due_date'):
                title_order_due_date_div.add('Due: {0}'.format(title_order.get('due_date')))

            external_rejection_button = ButtonNewWdg(title='External Rejection', icon='RED_BOMB')
            external_rejection_button.add_behavior(self.get_external_rejection_button_behavior())
            external_rejection_button.add_style('display', 'inline-block')

            element_evaluation_button = ButtonNewWdg(title='Element Evaluation', icon='REPORT')
            element_evaluation_button.add_behavior(self.get_element_evaluation_button_behavior(title_order.get('title_code')))
            element_evaluation_button.add_style('display', 'inline-block')

            note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
            note_button.add_behavior(obu.get_add_notes_behavior(title_order.get_search_key()))
            note_button.add_style('display', 'inline-block')

            instructions_button = ButtonNewWdg(title='Instructions', icon='CONTENTS')
            instructions_button.add_behavior(self.get_instructions_wdg(title_order.get_code()))
            instructions_button.add_style('display', 'inline-block')

            change_due_date_button = ButtonNewWdg(title='Change Due Date', icon='DATE')
            change_due_date_button.add_behavior(self.get_change_due_date_behavior(title_order.get_code(),
                                                                                  title_order.get('due_date')))
            change_due_date_button.add_style('display', 'inline-block')

            button_row_div = SpanWdg()
            button_row_div.add_style('display', 'inline-block')
            button_row_div.add(external_rejection_button)
            button_row_div.add(element_evaluation_button)
            button_row_div.add(note_button)
            button_row_div.add(instructions_button)
            button_row_div.add(change_due_date_button)

            title_div = DivWdg()
            title_div.add_style('background-color', '#d9edcf')
            title_div.add_style('padding', '10px')
            title_div.add_style('border-radius', '10px')

            title_div.add(title_order_name_div)
            title_div.add(title_order_description_div)
            title_div.add(title_order_priority_div)
            title_div.add(title_order_due_date_div)
            title_div.add(button_row_div)

            tasks = obu.get_tasks_for_title_order(title_order)

            title_task_div = DivWdg()
            title_task_div.add_style('width', '100%')
            title_task_div.add_style('margin-left', '30px')

            # If there are tasks associated to the title_order, add them as a sub-list below it
            if tasks:
                task_list = DivWdg()

                for task in tasks:
                    task_div = DivWdg()
                    task_div.add(self.get_task_div(task))
                    task_list.add(task_div)

                title_task_div.add(task_list)

            title_order_div = DivWdg()
            title_order_div.add(title_div)
            title_order_div.add(title_task_div)

            title_order_list.add(title_order_div)

        return title_order_list

    @staticmethod
    def get_add_titles_behavior(order_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    var order_code = '%s';

    spt.api.load_popup('Add Title to Order', 'order_builder.InsertTitleInOrderWdg', {'code': order_code});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % order_code
        }

        return behavior

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
    def get_instructions_wdg(code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.api.load_popup('Instructions', 'order_builder.InstructionsWdg', {'title_order_code': '%s'});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % code
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

    def get_add_titles_button(self):
        add_titles_button = ButtonNewWdg(title='Add Title', icon='ADD')
        add_titles_button.add_behavior(self.get_add_titles_behavior(self.order_code))

        return add_titles_button

    def get_display(self):
        outer_div = DivWdg()
        outer_div.add_class('order-builder')

        order_div = DivWdg()

        order_div.add(self.setup_order_information())
        outer_div.add(order_div)

        title_orders_div = DivWdg()
        title_orders_div.add_style('display', 'inline-block')
        title_orders_div.add_style('width', '600px')
        title_orders_div.add(self.setup_html_list_for_title_orders())
        outer_div.add(title_orders_div)

        outer_div.add(self.get_add_titles_button())

        return outer_div
