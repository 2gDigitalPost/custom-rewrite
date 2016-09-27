from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from widgets.input_widgets import get_file_classification_select_wdg, get_text_input_wdg
from widgets.html_widgets import get_label_widget


class CreateFileForOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

        division_search = Search('twog/division')
        division_search.add_code_filter(self.order_sobject.get('division_code'))
        self.division_sobject = division_search.get_sobject()

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
var containing_element = bvr.src_el.getParent("#add_new_files_to_task");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var order_code = '%s';

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

// Using the code from the saved file, insert an entry into the file in order table
server.insert('twog/file_in_order', {'order_code': order_code, 'file_code': file_code});

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.order_sobject.get_code(), self.division_sobject.get_code(), self.parent_widget_title,
       self.parent_widget_name, self.parent_widget_search_key)
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
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div
