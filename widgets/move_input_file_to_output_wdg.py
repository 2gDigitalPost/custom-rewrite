import widgets.html_widgets
import widgets.input_widgets
from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_task_data_in_files, get_task_data_sobject_from_task_code,\
    get_client_division_sobject_for_task_sobject, get_order_sobject_from_task_sobject, get_potential_origin_files

from input_widgets import get_files_checkbox_from_file_list, get_file_classification_select_wdg


class MoveInputFileToOutputWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()
        self.task_data = get_task_data_sobject_from_task_code(self.task_sobject.get_code())

        self.division = get_client_division_sobject_for_task_sobject(self.task_sobject)

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('move_input_file_to_output')

        outer_div.add(widgets.html_widgets.get_label_widget('Path'))
        outer_div.add(widgets.input_widgets.get_text_input_wdg('new_file_for_task_path', 800))

        outer_div.add(widgets.html_widgets.get_label_widget('Classification'))
        outer_div.add(get_file_classification_select_wdg())

        files = get_potential_origin_files(self.task_data.get_code())

        outer_div.add(widgets.html_widgets.get_label_widget('Original File'))
        outer_div.add(get_files_checkbox_from_file_list(files, []))

        order_sobject = get_order_sobject_from_task_sobject(self.task_sobject)
        order_code = order_sobject.get_code()

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(
            self.get_submit_button_behavior(self.task_data.get_code(), self.division.get_code(), order_code,
                                            self.task_sobject.get_search_key())
        )
        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_submit_button_behavior(task_data_code, division_code, order_code, task_search_key):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#move_input_file_to_output");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var task_data_code = '%s';

var file_path = values["new_file_for_task_path"];
var classification = values["file_classification_select"];
var original_file_code = values["file_select"];
var division_code = '%s';

var origin_files = [];

for (var property in values) {
    if (property.startsWith("FILE")) {
        var file_checkbox_value = values[property];

        if (file_checkbox_value == "on") {
            origin_files.push(property);
        }
    }
}

var kwargs = {
    'file_path': file_path,
    'classification': classification,
    'division_code': division_code,
    'san_status': 'exists'
}

var inserted_file = server.insert('twog/file', kwargs);
var file_code = inserted_file['code'];

server.insert('twog/task_data_out_file', {'file_code': file_code, 'task_data_code': task_data_code})

for (var i = 0; i < origin_files.length; i++) {
    server.insert('twog/file_to_origin_file', {'file_code': file_code, 'origin_file': origin_files[i]});
}

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var task_search_key = '%s';

spt.api.load_tab('Task', 'widgets.TaskInspectWdg', {'search_key': task_search_key});
            ''' % (task_data_code, division_code, task_search_key)
        }

        return behavior
