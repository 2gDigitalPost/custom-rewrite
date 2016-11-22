from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg

from common_tools.utils import get_sobject_by_code, get_client_division_sobject_for_package_sobject


def get_instructions_select_wdg(division_code, platform_code):
    """
    Get a Select Widget with all the package instructions options

    :return: SelectWdg
    """

    package_instructions_search = Search('twog/package_instructions')
    package_instructions_search.add_filter('division_code', division_code)
    package_instructions_search.add_filter('platform_code', platform_code)

    instructions_select_wdg = SelectWdg('package_instructions_select')
    instructions_select_wdg.set_id('package_instructions_select')
    instructions_select_wdg.add_empty_option()
    instructions_select_wdg.set_search_for_options(package_instructions_search, 'code', 'name')

    return instructions_select_wdg


class ChangePackageInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('change-package-instructions')

        package_instructions_code = self.package_sobject.get_value('package_instructions_code')

        if package_instructions_code:
            package_instructions_sobject = get_sobject_by_code('twog/package_instructions', package_instructions_code)

            outer_div.add('Instruction Document is currently set to: {0}'.format(
                package_instructions_sobject.get_value('name')))
        else:
            outer_div.add('No Instructions Document currently selected')

        division_sobject = get_client_division_sobject_for_package_sobject(self.package_sobject)
        division_code = division_sobject.get_code()
        platform_code = self.package_sobject.get('platform_code')

        outer_div.add(get_instructions_select_wdg(division_code, platform_code))

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
    var containing_element = bvr.src_el.getParent("#change-package-instructions");
    var values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var package_code = '%s';
    var package_instructions_code = values.package_instructions_select;

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/package', package_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'package_instructions_code': package_instructions_code,
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
}''' % (self.package_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
        self.parent_widget_search_key)
        }

        return behavior
