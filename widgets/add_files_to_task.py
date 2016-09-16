from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table
from pyasm.widget import CheckboxWdg, SubmitWdg

from common_tools import get_task_data_sobject_from_task_code, get_files_for_order, get_task_data_in_files


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
function getAllElementsWithAttribute(attribute)
{
  var matchingElements = [];
  var allElements = document.getElementsByTagName('spt_class_name');
  for (var i = 0, n = allElements.length; i < n; i++)
  {
    if (allElements[i].getAttribute(attribute) !== null)
    {
      // Element exists with attribute. Add to array.
      matchingElements.push(allElements[i]);
    }
  }
  return matchingElements;
}


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

        outer_div.add(self.get_files_checkbox_for_task())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.task_data.get_code(),
                                                                   self.task_sobject.get_search_key()))

        outer_div.add(submit_button)

        return outer_div
