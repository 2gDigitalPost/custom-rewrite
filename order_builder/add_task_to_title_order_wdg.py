from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextInputWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from order_builder_utils import get_widget_header
from widgets.html_widgets import get_label_widget


def get_process_widget():
    process_input = TextInputWdg()
    process_input.set_name('process')

    return process_input


def get_submit_behavior():
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var submit_form = function(values) {
        spt.api.app_busy_show('Saving...');

        var env = spt.Environment.get();
        var login = env.user;

        // Get the values needed to submit the form
        var process = values.process;
        var description = values.description;
        var priority = values.priority;
        var assigned = values.assigned;
        var due_date = values.due_date;

        // Set up the object for the new task.
        var new_download_task = {
            'process': 'Download: ' + process,
            'description': description,
            'status': 'Pending',
            'priority': priority,
            'assigned_login_group': 'vault',
            'bid_end_date': due_date,
            'login': login
        }

        var server = TacticServerStub.get();

        // Have to set 'triggers' to false to avoid all the other stupid custom crap. Will remove once this method
        // of inserting becomes the norm.
        server.insert('sthpw/task', new_download_task, {'triggers': false});

        spt.api.app_busy_hide();

        // Get the board table by its ID
        var entry_form = document.getElementsByClassName('new-download-task-entry-form')[0];

        // Refresh the view
        spt.api.app_busy_show("Refreshing...");
        spt.api.load_panel(entry_form, 'tasks.NewDownloadTask');
        spt.api.app_busy_hide();
    }

    // Get the form values
    var outer_div = spt.api.get_parent(bvr.src_el, '.new-download-task-entry-form');
    var values = spt.api.get_input_values(outer_div);

    // Process is required, so if it is blank, alert the user
    if (!values.process || values.process == '') {
        spt.api.app_busy_hide();
        spt.alert("Process field is required.");
        return;
    }

    if (!values.due_date || values.due_date == '') {
        spt.api.app_busy_hide();
        spt.alert("Due Date field is required.");
        return;
    }

    submit_form(values);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}'''
    }

    return behavior


def get_submit_widget():
    submit_button = SubmitWdg('Submit')
    submit_button.add_behavior(get_submit_behavior())

    return submit_button


class AddTaskToTitleOrderWdg(BaseRefreshWdg):
    def init(self):
        title_order_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.add_class('add-task-to-title-order-wdg')

        page_label = 'Add Task'
        outer_div.add(get_widget_header(page_label))

        outer_div.add(get_label_widget('Process'))
        outer_div.add(get_process_widget())

        outer_div.add(get_submit_widget())

        return outer_div
