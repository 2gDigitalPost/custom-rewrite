from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg, SelectWdg

import order_builder.order_builder_utils as obu

from widgets.html_widgets import get_label_widget
from widgets.input_widgets import get_text_input_wdg, get_datetime_calendar_wdg


class DepartmentRequestWdg(BaseRefreshWdg):
    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('new-department-request-entry-form')

        page_label = "<div>Fill out the following form to submit a new request. The request will be added to the " \
                     "department's list, and will be addressed as soon as possible. You will receive a " \
                     "notification when the request is complete.</div><br/>"
        outer_div.add(page_label)

        outer_div.add(get_label_widget('Name'))
        outer_div.add(get_text_input_wdg('name', 800))

        outer_div.add(get_label_widget('Description'))
        outer_div.add(obu.get_text_area_input_wdg('description', 800, [('display', 'block')]))

        outer_div.add(get_label_widget('Due Date'))
        outer_div.add(get_datetime_calendar_wdg())

        department_select_wdg = SelectWdg('department_select')
        department_select_wdg.append_option('Onboarding', 'onboarding')
        department_select_wdg.append_option('Edel', 'edel')
        department_select_wdg.append_option('Compression', 'compression')
        department_select_wdg.append_option('QC', 'qc')

        outer_div.add(get_label_widget('Department'))
        outer_div.add(department_select_wdg)

        self.get_submit_widget(outer_div)

        return outer_div

    def get_submit_widget(self, outer_div):
        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.submit_button_behavior())

        outer_div.add(submit_button)

    @staticmethod
    def submit_button_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var submit_form = function(values) {
    spt.api.app_busy_show('Saving...');

    var server = TacticServerStub.get();

    var env = spt.Environment.get();
    var login = env.user;

    // Get the values needed to submit the form
    var name = values.name;
    var description = values.description;
    var due_date = values.datetime_calendar;
    var department = values.department_select;

    // Find the pipeline saved that has the name 'twog_pipeline_request', and get its code
    var pipeline_code = server.eval("@GET(sthpw/pipeline['name', 'department_request_pipeline'].code)");

    // Set up the object for the new task.
    var department_request_data = {
        'name': name,
        'description': description,
        'due_date': due_date,
        'assigned_department': department,
        'login': login,
        'pipeline_code': pipeline_code,
    }

    server.insert('twog/department_request', department_request_data);

    // Refresh the view
    spt.api.app_busy_hide();
    spt.api.load_tab('New Department Request', 'widgets.DepartmentRequestWdg');
    spt.info("Your request has been submitted.");
}

// Get the server object
var server = TacticServerStub.get();

// Get the form values
var containing_element = bvr.src_el.getParent("#new-department-request-entry-form");
var values = spt.api.get_input_values(containing_element, null, false);

console.log(values);

if (!values.datetime_calendar || values.datetime_calendar == '') {
    spt.api.app_busy_hide();
    spt.alert("Due Date field is required.");
    return;
}

submit_form(values);
'''
        }

        return behavior
