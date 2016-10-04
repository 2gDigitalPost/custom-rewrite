from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from common_tools.utils import get_instructions_template_select_wdg


class AddInstructionsFromTemplateWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()

        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add-instructions-from-template')

        outer_div.add('Choose an Instructions Template from the dropdown list below. The resulting Instructions '
                      'Document will be added automatically to this Component.')

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

    // Create a new instructions document using the template code
    // Get all the department instructions linked to this instructions template. Start by querying the many-to-many table
    var department_instructions_in_template_sobjects = server.eval("@SOBJECT(twog/department_instructions_in_template['instructions_template_code', '" + instructions_template_code + "'])");
    var department_instructions_codes = [];

    for (var i = 0; i < department_instructions_in_template_sobjects.length; i++) {
        var department_instructions_in_template_sobject = department_instructions_in_template_sobjects[i];
        department_instructions_codes.push(department_instructions_in_template_sobject['department_instructions_code']);
    }

    // Get the codes into a string for searching
    var department_instructions_codes_string = department_instructions_codes.join('|');

    // Then get the individual department sobjects
    var department_instructions_sobjects = server.eval("@SOBJECT(twog/department_instructions['code', 'in', '" + department_instructions_codes_string + "'])");

    var sorted_department_instructions_sobjects = [];

    // TODO: Probably a much more efficient way of sorting the list
    for (var i = 0; i < department_instructions_sobjects.length; i++) {
        for (var j = 0; j < department_instructions_in_template_sobjects.length; j++) {
            var department_instructions_in_template_sobject = department_instructions_in_template_sobjects[j];

            if ((j + 1) === department_instructions_in_template_sobject['sort_order']) {
                sorted_department_instructions_sobjects.push(department_instructions_sobjects[i]);
                j = department_instructions_in_template_sobjects.length + 1;
            }
        }
    }
    // Go through each department_instructions entry, getting both the name and the instructions text. Add them to a string
    // that will be used when inserted the new instructions document
    var instructions_text = '';

    for (var i = 0; i < sorted_department_instructions_sobjects.length; i++) {
        var department_instructions_sobject = sorted_department_instructions_sobjects[i];

        instructions_text += '### ' + department_instructions_sobject['name'] + '\\n\\n';
        instructions_text += department_instructions_sobject['instructions_text'] + '\\n\\n';
    }

    // Finally, insert a new instructions entry with the name and compiled text.
    var inserted_instructions_doc = server.insert('twog/instructions', {'name': 'Instructions for ' + component_code,
                                                                        'instructions_text': instructions_text});

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/component', component_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'instructions_code': inserted_instructions_doc['code'],
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
