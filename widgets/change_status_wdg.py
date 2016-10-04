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
spt.app_busy.show('Saving...');

var package_code = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#status_select_" + package_code);
var values = spt.api.get_input_values(containing_element, null, false);

var task_status = values["file_status_select"];

// Set up an object to hold the data
var kwargs = {
    'status': task_status
}

var file_codes = [];

for (var key in values) {
    if (key.toString().startsWith('FILE')) {
        file_codes.push(key);
    }
}

var file_codes_string = file_codes.join('|');
var files = server.eval("@SOBJECT(twog/file['code', 'in', '" + file_codes_string + "'])");

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;
    var file_checkbox_value = values[file_code];

    var file_in_package_sobject = server.eval("@SOBJECT(twog/file_in_package['file_code', '" + file_code +
                                              "']['package_code',  '" + package_code + "'])")[0];

    var task_sobject = server.eval("@SOBJECT(sthpw/task['search_code', '" + file_in_package_sobject['code'] + "'])")[0];

    if (file_checkbox_value == "on") {
        // Only modify the entry if the user selected it
        if (task_sobject) {
            server.update(task_sobject['__search_key__'], kwargs);
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
