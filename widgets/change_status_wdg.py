from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.biz import Pipeline
from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, Table
from pyasm.widget import CheckboxWdg, SelectWdg, SubmitWdg

from widgets.input_widgets import get_task_status_select_wdg

from common_tools.utils import get_file_in_package_sobjects_by_package_code,\
    get_file_sobjects_from_file_in_package_sobjects


def get_file_in_package_status_select():
    task_status_select = SelectWdg('file_status_select')
    task_status_select.set_id('file_status_select')
    task_status_select.add_style('width: 165px;')
    task_status_select.add_empty_option()

    pipeline = Pipeline.get_by_code('twog_Delivery')

    for status in pipeline.get_process_names():
        task_status_select.append_option(status, status)

    return task_status_select


class ChangeStatusWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var task_code = '%s';
var task_search_key = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#status_select_" + task_code);
var values = spt.api.get_input_values(containing_element, null, false);

var task_status = values["task_status_select"];

// Set up an object to hold the data
var kwargs = {
    'status': task_status
}

server.update(task_search_key, kwargs);

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.task_sobject.get_code(), self.task_sobject.get_search_key(),
       self.parent_widget_title, self.parent_widget_name, self.parent_widget_search_key)
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('status_select_{0}'.format(self.task_sobject.get_code()))

        outer_div.add(get_task_status_select_wdg(self.task_sobject))

        submit_button = SubmitWdg('Submit Changes')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        outer_div.add(submit_button)

        return outer_div


class ChangeMultipleFileStatusesOnPackageWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
function findValueByPrefix(object, prefix) {
    for (var property in object) {
    if (object.hasOwnProperty(property) && property.toString().startsWith(prefix)) {
        return object[property];
    }
}
}

// findValueByPrefix(obj, "key1");


var package_code = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#status_select_" + package_code);
var values = spt.api.get_input_values(containing_element, null, false);

var task_status = values["file_status_select"];

console.log(values);

// Set up an object to hold the data
var kwargs = {
    'status': task_status
}

// server.update(task_search_key, kwargs);

var file_codes = [];

for (var key in values) {
    if (key.toString().startsWith('FILE')) {
        console.log(key);
        file_codes.push(key);
    }
}

var file_codes_string = file_codes.join('|');

var files = server.eval("@SOBJECT(twog/file['code', 'in', '" + file_codes_string + "'])");

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;

    var file_checkbox_value = values[file_code];

    var existing_entry = server.eval("@SOBJECT(twog/file_in_package['file_code', '" + file_code +
                                     "']['package_code',  '" + package_code + "'])")[0];

    console.log(existing_entry);

    var task_sobject = existing_entry.get_all_children('sthpw/task');
    console.log(task_sobject);

    if (file_checkbox_value == "on") {
        // Only modify the entry if the user selected it
        if (existing_entry.length == 0) {
            var new_entry = {
                'package_code': package_code,
                'file_code': file_code
            }

            // server.insert('twog/file_in_package', new_entry);
        }
    }
    else {
        // If a box is unchecked, remove any entries in the database that exist (in other words, if a box was checked
        // but is now unchecked, the user meant to remove the connection)
        if (existing_entry.length > 0)
        {
            // server.delete_sobject(existing_entry[0].__search_key__);
        }
    }
}

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.package_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
       self.parent_widget_search_key)
        }

        return behavior

    def get_files_checkboxes(self):
        file_in_package_sobjects = get_file_in_package_sobjects_by_package_code(self.package_sobject.get_code())
        file_sobjects = get_file_sobjects_from_file_in_package_sobjects(file_in_package_sobjects)

        files_checkbox_table = Table()

        header_row = files_checkbox_table.add_row()
        header = files_checkbox_table.add_header(data='Files', row=header_row)
        header.add_style('text-align', 'center')
        header.add_style('text-decoration', 'underline')

        for file_sobject, file_in_package_sobject in zip(file_sobjects, file_in_package_sobjects):
            checkbox = CheckboxWdg(name=file_sobject.get_code())

            checkbox_row = files_checkbox_table.add_row()

            files_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
            files_checkbox_table.add_cell(data=file_sobject.get_value('file_path'), row=checkbox_row)

        return files_checkbox_table

    def get_list_of_file_statuses(self):
        outer_div = DivWdg()

        file_in_package_sobjects = get_file_in_package_sobjects_by_package_code(self.package_sobject.get_code())
        file_sobjects = get_file_sobjects_from_file_in_package_sobjects(file_in_package_sobjects)

        files_unordered_html_list = HtmlElement.ul()

        for file_sobject, file_in_package_sobject in zip(file_sobjects, file_in_package_sobjects):
            task_sobject = file_in_package_sobject.get_all_children('sthpw/task')[0]

            file_li = HtmlElement.li()
            file_li.add(file_sobject.get('file_path') + ' - ' + task_sobject.get('status'))

            files_unordered_html_list.add(file_li)

        outer_div.add(files_unordered_html_list)

        return outer_div

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('status_edit_{0}'.format(self.package_sobject.get_code()))

        outer_div.add(self.get_files_checkboxes())
        outer_div.add(get_file_in_package_status_select())

        submit_button = SubmitWdg('Submit Changes')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        outer_div.add(submit_button)

        return outer_div
