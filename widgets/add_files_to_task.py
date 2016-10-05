from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table
from pyasm.widget import CheckboxWdg, SubmitWdg

from common_tools.utils import get_files_for_order, get_client_division_sobject_for_task_sobject,\
    get_task_data_in_files, get_task_data_sobject_from_task_code

from widgets.html_widgets import get_label_widget
from widgets.input_widgets import get_text_input_wdg, get_file_classification_select_wdg


class AddInputFilesToTaskWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())
        component = self.task_sobject.get_parent()

        order_search = Search('twog/order')
        order_search.add_code_filter(component.get('order_code'))
        order = order_search.get_sobject()

        self.order_files = get_files_for_order(order.get_code())
        self.selected_files = get_task_data_in_files(self.task_data.get_code())

    def get_files_checkbox_for_task(self):
        files_checkbox_table = Table()

        header_row = files_checkbox_table.add_row()
        header = files_checkbox_table.add_header(data='Files', row=header_row)
        header.add_style('text-align', 'center')
        header.add_style('text-decoration', 'underline')

        for file_sobject in self.order_files:
            checkbox = CheckboxWdg(name=file_sobject.get_code())

            if file_sobject.get_code() in [selected_file.get_code() for selected_file in self.selected_files]:
                checkbox.set_checked()

            checkbox_row = files_checkbox_table.add_row()

            files_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
            files_checkbox_table.add_cell(data=file_sobject.get_value('file_path'), row=checkbox_row)

        return files_checkbox_table

    @staticmethod
    def get_submit_button_behavior(task_data_code, task_search_key):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
spt.app_busy.show('Saving...');

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

    var existing_entry = server.eval("@SOBJECT(twog/task_data_in_file['file_code', '" + file_code +
                                     "']['task_data_code',  '" + task_data_code + "'])");

    if (file_checkbox_value == "on") {
        // Only insert a new entry if one does not already exist.
        if (existing_entry.length == 0) {
            var new_entry = {
                'task_data_code': task_data_code,
                'file_code': file_code
            }

            server.insert('twog/task_data_in_file', new_entry);
        }
    }
    else {
        // If a box is unchecked, remove any entries in the database that exist (in other words, if a box was checked
        // but is now unchecked, the user meant to remove the connection)
        if (existing_entry.length > 0)
        {
            server.delete_sobject(existing_entry[0].__search_key__);
        }
    }
}

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var task_search_key = '%s';

spt.api.load_tab('Task', 'widgets.TaskInspectWdg', {'search_key': task_search_key});
            ''' % (task_data_code, task_search_key)
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_files_to_task')

        if self.order_files:
            outer_div.add(self.get_files_checkbox_for_task())

            submit_button = SubmitWdg('Submit')
            submit_button.add_behavior(self.get_submit_button_behavior(self.task_data.get_code(),
                                                                       self.task_sobject.get_search_key()))

            outer_div.add(submit_button)
        else:
            outer_div.add('<div>No files exist for this Order yet.</div>')

        return outer_div


class CreateNewInputFileForTaskWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())

        self.division = get_client_division_sobject_for_task_sobject(self.task_sobject)

        component = self.task_sobject.get_parent()

        order_search = Search('twog/order')
        order_search.add_code_filter(component.get('order_code'))
        self.order_sobject = order_search.get_sobject()

        self.order_files = get_files_for_order(self.order_sobject.get_code())
        self.selected_files = get_task_data_in_files(self.task_data.get_code())

    @staticmethod
    def get_submit_button_behavior(task_data_code, division_code, order_code, task_search_key):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#add_new_files_to_task");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var task_data_code = '%s';

var file_path = values["new_file_path"];
var classification = values["file_classification_select"];
var division_code = '%s';

// Set up an object to hold the data
var kwargs = {
    'file_path': file_path,
    'classification': classification,
    'division_code': division_code
}

// Save the new file sobject, and get the code that it saved as
var inserted_file = server.insert('twog/file', kwargs);
var file_code = inserted_file['code'];

// Using the code from the saved file, insert an entry into task_data's input files
server.insert('twog/task_data_in_file', {'task_data_code': task_data_code, 'file_code': file_code});

// Also insert an entry into the file_in_order table, since this file is part of the order
var order_code = '%s';

server.insert('twog/file_in_order', {'file_code': file_code, 'order_code': order_code});

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var task_search_key = '%s';

spt.api.load_tab('Task', 'widgets.TaskInspectWdg', {'search_key': task_search_key});
            ''' % (task_data_code, division_code, order_code, task_search_key)
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_new_files_to_task')

        outer_div.add(get_label_widget('Path'))
        outer_div.add(get_text_input_wdg('new_file_path', 800))

        outer_div.add(get_label_widget('Classification'))
        outer_div.add(get_file_classification_select_wdg())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.task_data.get_code(),
                                                                   self.division.get_code(),
                                                                   self.order_sobject.get_code(),
                                                                   self.task_sobject.get_search_key()))

        outer_div.add(submit_button)

        return outer_div
