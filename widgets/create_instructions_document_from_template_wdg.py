from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from widgets.input_widgets import get_text_input_wdg
from widgets.html_widgets import get_label_widget


class CreateInstructionsDocumentFromTemplateWdg(BaseRefreshWdg):
    def init(self):
        self.instructions_template_sobject = self.get_sobject_from_kwargs()

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#create_instructions_document_from_template");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var new_instructions_document_name = values["new_instructions_name"];
var instructions_template_code = '%s';

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
server.insert('twog/instructions', {'name': new_instructions_document_name, 'instructions_text': instructions_text});

// Close the popup. The original widget did not change, to there is no point in reloading it.
spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

// Let the user know the transaction was a success.
spt.info('New Instructions Document created successfully.');
''' % (self.instructions_template_sobject.get_code())
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('create_instructions_document_from_template')

        outer_div.add(get_label_widget('Name'))
        outer_div.add(get_text_input_wdg('new_instructions_name', 600))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div
