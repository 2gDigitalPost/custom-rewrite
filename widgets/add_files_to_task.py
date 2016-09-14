from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, Table
from pyasm.widget import CheckboxWdg, MultiSelectWdg, SubmitWdg

import order_builder.order_builder_utils as obu

from common_tools import get_task_data_sobject_from_task_code


class AddInputFilesToTaskWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())
        component = self.task_sobject.get_parent()

        package_search = Search('twog/package')
        package_search.add_code_filter(component.get('package_code'))
        package = package_search.get_sobject()

        order_search = Search('twog/order')
        order_search.add_code_filter(package.get('order_code'))
        order = order_search.get_sobject()

        files_in_order_search = Search('twog/file_in_order')
        files_in_order_search.add_filter('order_code', order.get_code())
        files_in_order = files_in_order_search.get_sobjects()

        self.files = []

        for file_in_order in files_in_order:
            file_search = Search('twog/file')
            file_search.add_code_filter(file_in_order.get('file_code'))
            self.files.append(file_search.get_sobject())

    def get_files_checkbox_for_task(self):
        files_checkbox_table = Table()

        header_row = files_checkbox_table.add_row()
        header = files_checkbox_table.add_header(data='Files', row=header_row)
        header.add_style('text-align', 'center')
        header.add_style('text-decoration', 'underline')

        for file_sobject in self.files:
            checkbox = CheckboxWdg(name=file_sobject.get_code())

            checkbox_row = files_checkbox_table.add_row()

            files_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
            files_checkbox_table.add_cell(data=file_sobject.get_value('file_path'), row=checkbox_row)

        return files_checkbox_table

    @staticmethod
    def get_submit_button_behavior(task_data_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#add_files_to_task");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var task_data_code = '%s';

var files = server.eval("@SOBJECT(twog/file)");

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;

    var file_checkbox_value = values[file_code];

    if (file_checkbox_value == "on") {
        var new_entry = {
            'task_data_code': task_data_code,
            'file_code': file_code
        }

        server.insert('twog/task_data_in_file', new_entry);
    }
}

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));
            ''' % task_data_code
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_files_to_task')

        outer_div.add(self.get_files_checkbox_for_task())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.task_data.get_code()))

        outer_div.add(submit_button)

        return outer_div
