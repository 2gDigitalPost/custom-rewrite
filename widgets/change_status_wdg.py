from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from widgets.input_widgets import get_task_status_select_wdg


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
