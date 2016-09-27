from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from widgets.input_widgets import get_files_checkboxes_for_division


class AddFilesToOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#add_files_to_order");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var order_code = '%s';

var files = server.eval("@SOBJECT(twog/file)");

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;

    var file_checkbox_value = values[file_code];

    var existing_entry = server.eval("@SOBJECT(twog/file_in_order['file_code', '" + file_code +
                                     "']['order_code',  '" + order_code + "'])");

    if (file_checkbox_value == "on") {
        // Only insert a new entry if one does not already exist.
        if (existing_entry.length == 0) {
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
            ''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
                   self.parent_widget_search_key)
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_files_to_order')

        division_search = Search('twog/division')
        division_search.add_code_filter(self.order_sobject.get('division_code'))
        division_sobject = division_search.get_sobject()

        if division_sobject:
            outer_div.add(get_files_checkboxes_for_division(division_sobject.get_code(), self.order_sobject.get_code()))
        else:
            outer_div.add('<div>You cannot add files to an Order until a Client Division has been selected.</div>')

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div
