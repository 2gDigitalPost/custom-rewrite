from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_deliverable_files_in_order, get_files_for_package

from input_widgets import get_files_checkbox_from_file_list


class AddDeliverableFilesToPackageWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_deliverable_files_to_package')

        order_sobject = self.package_sobject.get_parent()
        deliverable_files = get_deliverable_files_in_order(order_sobject)
        selected_files = get_files_for_package(self.package_sobject.get_code())

        deliverable_file_select_wdg = get_files_checkbox_from_file_list(deliverable_files, selected_files)

        outer_div.add(deliverable_file_select_wdg)

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#add_deliverable_files_to_package");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var package_code = '%s';

var files = server.eval("@SOBJECT(twog/file)");

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;

    var file_checkbox_value = values[file_code];

    var existing_entry = server.eval("@SOBJECT(twog/file_in_package['file_code', '" + file_code +
                                     "']['package_code',  '" + package_code + "'])");

    if (file_checkbox_value == "on") {
        // Only insert a new entry if one does not already exist.
        if (existing_entry.length == 0) {
            var new_entry = {
                'package_code': package_code,
                'file_code': file_code
            }

            server.insert('twog/file_in_package', new_entry);
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

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.package_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
        self.parent_widget_search_key)
        }

        return behavior