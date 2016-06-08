from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextAreaInputWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import MultiSelectWdg, SubmitWdg

import order_builder_utils as obu


class InsertTitleInOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_code = self.get_kwargs().get('code')

        order_sobject_search = Search('twog/order')
        order_sobject_search.add_code_filter(self.order_code)
        self.order_sobject = order_sobject_search.get_sobject()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-title-in-order')

        # TODO: Allow users to open a popup to add a title
        self.get_title_select_widget(outer_div)
        self.get_description_input_widget(outer_div)
        self.get_platform_select_widget(outer_div)
        self.get_languages_widget(outer_div)
        self.get_territory_widget(outer_div)

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.order_code))

        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_title_select_widget(outer_div):
        title_select_wdg = obu.get_select_widget_from_search_type('twog/title', 'code', 'name', 'code',
                                                                  search_order_bys=['name'])
        title_select_wdg.set_id('new-title-code')

        outer_div.add(obu.get_label_widget('Title'))
        outer_div.add(title_select_wdg)

    @staticmethod
    def get_description_input_widget(outer_div):
        description_input = TextAreaInputWdg()
        description_input.set_name('description')
        description_input.add_class('new-title-order-description')

        outer_div.add(obu.get_label_widget('Description'))
        outer_div.add(description_input)

    @staticmethod
    def get_platform_select_widget(outer_div):
        platform_select_wdg = obu.get_select_widget_from_search_type('twog/platform', 'platform_code', 'name', 'code')
        platform_select_wdg.set_id('new-platform-code')

        outer_div.add(obu.get_label_widget('Platform'))
        outer_div.add(platform_select_wdg)

    @staticmethod
    def get_languages_widget(outer_div):
        languages_search = Search('twog/language')

        languages_wdg = MultiSelectWdg('Languages')
        languages_wdg.add_empty_option('----')
        languages_wdg.set_search_for_options(languages_search, label_column='name', value_column='code')

        outer_div.add(obu.get_label_widget('Language'))
        outer_div.add(languages_wdg)

    @staticmethod
    def get_territory_widget(outer_div):
        territory_wdg = obu.get_select_widget_from_search_type('twog/territory', 'territory', 'name', 'code')

        outer_div.add(obu.get_label_widget('Territory'))
        outer_div.add(territory_wdg)

    @staticmethod
    def get_submit_button_behavior(order_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Get the server object
    var server = TacticServerStub.get();

    // Get the form values
    var order_code = '%s';
    var title_code = document.getElementById('new-title-code');
    var platform_code = document.getElementById('new-platform-code');
    var description = document.getElementsByClassName('new-title-order-description')[0];

    // Set up the object for the new title_order entry.
    var new_title_order = {
        'name': String(title_code.options[title_code.selectedIndex].text + " in " + order_code),
        'order_code': order_code,
        'title_code': title_code.value,
        'platform_code': platform_code.value,
        'description': description.value,
    }

    server.insert('twog/title_order', new_title_order);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (order_code)
        }

        return behavior
