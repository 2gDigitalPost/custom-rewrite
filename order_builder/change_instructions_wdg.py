from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_instructions_template_select_wdg


class ChangeInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('change-instructions')

        instructions_code = self.component_sobject.get_value('instructions_template_code')

        if instructions_code:
            instructions_search = Search('twog/instructions_template')
            instructions_search.add_code_filter(instructions_code)
            instructions_sobject = instructions_search.get_sobject()

            outer_div.add('Instruction Document is currently set to: {0}'.format(
                instructions_sobject.get_value('name')))
        else:
            outer_div.add('No Instructions Document currently selected')

        outer_div.add(get_instructions_template_select_wdg())

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
    var component_code = '%s';
    var instructions_template_code = values.instructions_template_select;

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/component', component_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'instructions_template_code': instructions_template_code,
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
}''' % (self.component_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
        self.parent_widget_search_key)
        }

        return behavior
