from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_task_data_sobject_from_task_code

from widgets.input_widgets import get_text_input_wdg


class ChangeEstimatedHoursForTaskWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())

        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('change-estimated-hours')

        current_estimated_hours = self.task_data.get('estimated_hours')

        if current_estimated_hours:
            current_hours_text = 'The estimated hours for this task is currently set to {0} hour(s).'.format(
                current_estimated_hours)
        else:
            current_hours_text = 'Estimated hours is not currently set for this task.'

        outer_div.add(current_hours_text)
        outer_div.add(get_text_input_wdg('new_estimated_hours', 100))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#change-instructions");
    var values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var task_data_code = '%s';
    var estimated_hours = values.new_estimated_hours;

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/task_data', task_data_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'estimated_hours': estimated_hours,
    }

    // Send the update to the server
    server.update(search_key, kwargs);

    spt.app_busy.hide();
    spt.popup.close(spt.popup.get_popup(bvr.src_el));

    var parent_widget_title = '%s';
    var parent_widget_name = '%s';
    var parent_widget_search_key = '%s';

    spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (self.task_data.get_code(), self.parent_widget_title, self.parent_widget_name, self.parent_widget_search_key)
        }

        return behavior
