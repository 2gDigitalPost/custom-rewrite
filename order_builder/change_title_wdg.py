from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg


def get_title_select_wdg():
    """
    Get a SelectWdg that contains all the possible titles that the component can switch to.

    :return: SelectWdg
    """

    # Set up a basic select widget with an empty object
    title_select_wdg = SelectWdg('title_select')
    title_select_wdg.set_id('title_select')
    title_select_wdg.add_style('width', '300px')
    title_select_wdg.add_empty_option()

    # Get the titles
    titles_search = Search('twog/title')
    titles = titles_search.get_sobjects()

    # Add the title names as the labels and the codes as the values
    for title in titles:
        title_select_wdg.append_option(title.get_value('name'), title.get_code())

    # Return the SelectWdg
    return title_select_wdg


class ChangeTitleWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('change-title')

        title_code = self.component_sobject.get_value('title_code')

        if title_code:
            title_sobject_search = Search('twog/title')
            title_sobject_search.add_code_filter(title_code)
            title_sobject = title_sobject_search.get_sobject()

            outer_div.add('Title is currently set to: {0}'.format(title_sobject.get_value('name')))
        else:
            outer_div.add('No Title currently selected')

        outer_div.add(get_title_select_wdg())

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
    var containing_element = bvr.src_el.getParent("#change-title");
    var values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var component_code = '%s';
    var title_code = values.title_select;

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/component', component_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'title_code': title_code,
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
