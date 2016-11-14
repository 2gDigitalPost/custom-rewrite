from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, SpanWdg
from pyasm.widget import SubmitWdg, TextAreaWdg


def get_components_attached_to_instructions(instructions_sobject):
    """
    Given a twog/instructions sobject, return the list of twog/component sobjects that are pointing to the instructions.

    :param instructions_sobject: twog/instructions sobject
    :return: List of twog/component sobjects
    """
    component_search = Search('twog/component')
    component_search.add_filter('instructions_code', instructions_sobject.get_code())
    components = component_search.get_sobjects()

    return components


def get_instructions_textarea_wdg(instructions_sobject, width=600, height=600):
    """
    Given an instructions sobject, get a TextArea widget to hold all of its text. Optionally, pass in the width and
    height of the TextArea widget.

    :param instructions_sobject: twog/instructions sobject
    :param width: int
    :param height: int
    :return: DivWdg (holding the TextArea widget)
    """

    instructions_div = DivWdg()
    instructions_div.add_style('margin', '10px')
    instructions_textarea_wdg = TextAreaWdg()
    instructions_textarea_wdg.set_id('instructions_textarea')
    instructions_textarea_wdg.set_name('instructions_textarea')
    instructions_textarea_wdg.add_style('width', '{0}px'.format(width))
    instructions_textarea_wdg.add_style('height', '{0}px'.format(height))

    instructions_text = instructions_sobject.get('instructions_text')
    instructions_textarea_wdg.set_value(instructions_text)

    instructions_div.add(instructions_textarea_wdg)

    return instructions_div


class EditInstructionsWdg(BaseRefreshWdg):
    """
    A very basic TextArea widget to edit a twog/instructions instance. Also displays a list of the the Components the
    instructions are attached to.

    This widget will likely evolve a lot in the future. For now, we just need a way for an operator to edit
    instructions.
    """

    def init(self):
        self.instructions_sobject = self.get_sobject_from_kwargs()

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
spt.app_busy.show('Saving...');

var instructions_code = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#edit_instructions_" + instructions_code);
var values = spt.api.get_input_values(containing_element, null, false);

var instructions_textarea_input = values["instructions_textarea"];

// Set up an object to hold the data
var kwargs = {
    'instructions_text': instructions_textarea_input
}

var instructions_search_key = server.build_search_key('twog/instructions', instructions_code, 'twog');

server.update(instructions_search_key, kwargs);

spt.app_busy.hide();

// Reload the tab
spt.api.load_tab('Edit Instructions', 'widgets.EditInstructionsWdg', {'search_key': instructions_search_key});

spt.info('Changes saved successfully');
''' % (self.instructions_sobject.get_code())
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('edit_instructions_{0}'.format(self.instructions_sobject.get_code()))

        # Get a list of the components the instructions are attached to
        attached_components = get_components_attached_to_instructions(self.instructions_sobject)
        component_div = DivWdg()
        title_span = SpanWdg()

        if attached_components:
            title_span.add('The following Components are attached to this Instructions Document:')
            component_div.add(title_span)

            component_list = HtmlElement.ul()

            for component in attached_components:
                li = HtmlElement.li()
                li.add('{0} ({1})'.format(component.get('name'), component.get_code()))
                component_list.add(li)

            component_div.add(component_list)
        else:
            title_span.add('Instructions are not currently attached to any Components')
            component_div.add(title_span)

        outer_div.add(component_div)
        outer_div.add(get_instructions_textarea_wdg(self.instructions_sobject))

        submit_button = SubmitWdg('Submit Changes')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        outer_div.add(submit_button)

        return outer_div
