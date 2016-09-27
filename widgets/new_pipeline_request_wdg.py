import widgets.html_widgets
import widgets.input_widgets
from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

import order_builder.order_builder_utils as obu


class NewPipelineRequestWdg(BaseRefreshWdg):
    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('new-pipeline-request-entry-form')

        page_label = "<div>Fill out the following form to request a new pipeline. The request will be added to the " \
                     "Onboarding department's list, and will be addressed as soon as possible. You will receive a " \
                     "notification when the request is complete.</div><br/>"
        outer_div.add(page_label)

        outer_div.add(widgets.html_widgets.get_label_widget('Process'))
        outer_div.add(widgets.input_widgets.get_text_input_wdg('process', 800))

        outer_div.add(widgets.html_widgets.get_label_widget('Description'))
        outer_div.add(obu.get_text_area_input_wdg('description', 800, [('display', 'block')]))

        outer_div.add(widgets.html_widgets.get_label_widget('Due Date'))
        outer_div.add(obu.get_date_calendar_wdg())

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
    var process = "Pipeline Request: " + values.process;
    var description = values.description;
    var due_date = values.due_date;

    // Find the pipeline saved that has the name 'twog_pipeline_request', and get its code
    var pipeline_code = server.eval("@GET(sthpw/pipeline['name', 'twog_pipeline_request'].code)");

    // Set up the object for the new task.
    var new_pipeline_request = {
        'process': process,
        'description': description,
        'bid_end_date': due_date,
        'login': login,
        'pipeline_code': pipeline_code,
        'status': 'Ready'
    }

    server.insert('sthpw/task', new_pipeline_request);

    // Refresh the view
    spt.api.app_busy_hide();
    spt.api.load_tab('New Pipeline Request', 'widgets.NewPipelineRequestWdg');
    spt.info("Your request for a new pipeline has been submitted. You will be notified when it is complete.");
}

// Get the server object
var server = TacticServerStub.get();

// Get the form values
var containing_element = bvr.src_el.getParent("#new-pipeline-request-entry-form");
var values = spt.api.get_input_values(containing_element, null, false);

if (!values.due_date || values.due_date == '') {
    spt.api.app_busy_hide();
    spt.alert("Due Date field is required.");
    return;
}

submit_form(values);
'''
        }

        return behavior
