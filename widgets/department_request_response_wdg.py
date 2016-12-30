from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from order_builder.order_builder_utils import get_text_area_input_wdg

from widgets.html_widgets import get_label_widget, get_pre_widget


class DepartmentRequestResponseWdg(BaseRefreshWdg):
    """

    """

    def init(self):
        self.department_request_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('department-request-response')

        if self.department_request_sobject.get('response'):
            current_response_div = DivWdg()
            current_response_div.add(get_pre_widget(self.department_request_sobject.get('response')))

            outer_div.add(current_response_div)

        outer_div.add(get_label_widget('Response'))
        outer_div.add(get_text_area_input_wdg('response', 800, [('display', 'block')]))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.submit_button_behavior(self.department_request_sobject.get_search_key(),
                                                               self.department_request_sobject.get_code()))
        outer_div.add(submit_button)

        return outer_div


    @staticmethod
    def submit_button_behavior(department_request_search_key, code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var submit_form = function(values) {
    spt.api.app_busy_show('Saving...');

    var server = TacticServerStub.get();

    var env = spt.Environment.get();
    var login = env.user;

    var department_request_search_key = '%s';
    var code = '%s';

    // Get the values needed to submit the form
    var response = values.response;
    var current_response_text = server.eval("@GET(twog/department_request['code', '" + code + "'].response)");

    var new_response_text;

    if (current_response_text !== '') {
        new_response_text = login + ' @ ' + new Date().toLocaleString() + ': ' + response + "\\n\\n" + current_response_text;
    }
    else {
        new_response_text = login + ' @ ' + new Date().toLocaleString() + ': ' + response;
    }

    var department_request_data = {
        'response': new_response_text
    }

    server.update(department_request_search_key, department_request_data);

    // Refresh the view
    spt.app_busy.hide();
    spt.popup.close("department_request_response");
}

// Get the server object
var server = TacticServerStub.get();

// Get the form values
var containing_element = bvr.src_el.getParent("#department-request-response");
var values = spt.api.get_input_values(containing_element, null, false);

console.log(values);

submit_form(values);
''' % (department_request_search_key, code)
        }

        return behavior
