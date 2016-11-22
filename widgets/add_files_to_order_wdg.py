from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_sobject_by_code
from widgets.input_widgets import get_files_checkboxes_for_division


class AddFilesToOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_submit_button_behavior(self, division_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
spt.app_busy.show('Saving...');

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#add_files_to_order");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var order_code = '%s';
var division_code = '%s';

// Get a list of all the files belonging to the division
var files = server.eval("@SOBJECT(twog/file['division_code', '" + division_code + "'])");

// Get all the existing entries in the twog/file_in_order table for this order
var existing_entries = server.eval("@SOBJECT(twog/file_in_order['order_code', '" + order_code + "'])");

// Get a list of all the existing file codes
var existing_entry_file_codes = [];
for (var y = 0; y < existing_entries.length; y++) {
    existing_entry_file_codes.push(existing_entries[y].file_code);
}

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;

    var file_checkbox_value = values[file_code];

    if (file_checkbox_value == "on") {
        // Only insert a new entry if one does not already exist.
        if (existing_entry_file_codes.indexOf(file_code) == -1) {
            var new_entry = {
                'order_code': order_code,
                'file_code': file_code
            }

            server.insert('twog/file_in_order', new_entry);
        }
    }
    else {
        // If a box is unchecked, remove any entries in the database that exist (in other words, if a box was checked
        // but is now unchecked, the user meant to remove the connection)
        if (existing_entry_file_codes.indexOf(file_code) > -1) {
            for (var j = 0; j < existing_entries.length; j++) {
                if (existing_entries[j].file_code == file_code) {
                    server.delete_sobject(existing_entries[j].__search_key__);
                }
            }
        }
    }
}

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
            ''' % (self.order_sobject.get_code(), division_code, self.parent_widget_title, self.parent_widget_name,
                   self.parent_widget_search_key)
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_files_to_order')

        division_sobject = get_sobject_by_code('twog/division', self.order_sobject.get('division_code'))

        if division_sobject:
            division_code = division_sobject.get_code()

            outer_div.add(get_files_checkboxes_for_division(division_code, self.order_sobject.get_code()))

            submit_button = SubmitWdg('Submit')
            submit_button.add_behavior(self.get_submit_button_behavior(division_code))

            outer_div.add(submit_button)
        else:
            outer_div.add('<div>You cannot add files to an Order until a Client Division has been selected.</div>')


        return outer_div
