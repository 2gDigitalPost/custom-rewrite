from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg


def get_instructions_select_wdg():
    """
    Get a SelectWdg that contains all the possible instructions that the component can switch to.

    :return: SelectWdg
    """

    # Set up a basic select widget with an empty object
    instructions_select_wdg = SelectWdg('instructions_select')
    instructions_select_wdg.set_id('instructions_select')
    instructions_select_wdg.add_style('width', '300px')
    instructions_select_wdg.add_empty_option()

    # Get the instructions
    instructions_search = Search('twog/instructions')
    instructions_sobjects = instructions_search.get_sobjects()

    # Add the instructions names as the labels and the codes as the values
    for instructions_sobject in instructions_sobjects:
        instructions_select_wdg.append_option(instructions_sobject.get_value('name'), instructions_sobject.get_code())

    # Return the SelectWdg
    return instructions_select_wdg


class ChangeInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('change-instructions')

        instructions_code = self.component_sobject.get_value('instructions_code')

        if instructions_code:
            instructions_search = Search('twog/instructions')
            instructions_search.add_code_filter(instructions_code)
            instructions_sobject = instructions_search.get_sobject()

            outer_div.add('Instruction Document is currently set to: {0}'.format(
                instructions_sobject.get_value('name')))
        else:
            outer_div.add('No Instructions Document currently selected')

        outer_div.add(get_instructions_select_wdg())

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
    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#change-instructions");
    var values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var component_code = '%s';
    var instructions_code = values.instructions_select;

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/component', component_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'instructions_code': instructions_code,
    }

    // Send the update to the server
    server.update(search_key, kwargs);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (component_code)
        }

        return behavior
