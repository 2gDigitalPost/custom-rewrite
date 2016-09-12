from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextAreaInputWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import MultiSelectWdg, SubmitWdg

import order_builder_utils as obu


class InsertTaskWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-task-in-component')

        outer_div.add(obu.get_text_input_wdg('process'))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.component_sobject.get_code()))

        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_submit_button_behavior(component_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.app_busy.show("Saving...");

    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-task-in-component");
    var new_package_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var component_code = '%s';
    var process = new_package_values.process;

    // Set up the object for the new task entry.
    var new_task = {
        'process': process,
        'search_code': component_code,
        'project_code': 'twog'
    }

    server.insert('sthpw/task', new_task);

    spt.app_busy.hide();
    spt.popup.close(spt.popup.get_popup(bvr.src_el));
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (component_code)
        }

        return behavior
