from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import CalendarTimeWdg, TimeInputWdg, CalendarInputWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_task_data_sobject_from_task_code

from widgets.input_widgets import get_text_input_wdg
from widgets.html_widgets import get_label_widget


class ChangeOrderExpectedCompletionDate(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#change-order-expected-completion-date");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var file_path = values["file_path_input"];
var classification = values["file_classification_select"];

// Set up the kwargs dictionary to submit to the server
var kwargs = {
    'file_path': file_path,
    'classification': classification
}

// Get the search key for the server.update method
var file_search_key = server.build_search_key('twog/file', file_code, 'twog');

// Send the data
server.update(file_search_key, kwargs);

// Refresh the page
spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.parent_widget_title, self.parent_widget_name, self.parent_widget_search_key)
        }

        return behavior

    def get_display(self):
        div_wdg = DivWdg()
        div_wdg.set_id('change-order-expected-completion-date')

        calendar_wdg = CalendarInputWdg(name='change-expected-completion-date-calendar', width='120px')
        time_wdg = TimeInputWdg(name='change-expected-completion-date-time')

        div_wdg.add(get_label_widget('Date'))
        div_wdg.add(calendar_wdg)
        div_wdg.add(get_label_widget('Time'))
        div_wdg.add(time_wdg)

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.submit_button_behavior())
        div_wdg.add(submit_button)

        return div_wdg
