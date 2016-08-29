from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import CalendarInputWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

import order_builder_utils as obu


def get_date_calendar_wdg():
    date_calendar_wdg = CalendarInputWdg("due_date")
    date_calendar_wdg.set_option('show_activator', 'true')
    date_calendar_wdg.set_option('show_time', 'false')
    date_calendar_wdg.set_option('width', '300px')
    date_calendar_wdg.set_option('id', 'due_date')
    date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

    return date_calendar_wdg


class InsertPackageInOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-package-in-order')

        outer_div.add(obu.get_text_input_wdg('new_package_name', 400))
        self.get_platform_select_widget(outer_div)

        outer_div.add(obu.get_label_widget('Due Date'))
        outer_div.add(get_date_calendar_wdg())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.order_sobject.get_code()))

        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_platform_select_widget(outer_div):
        platform_select_wdg = obu.get_select_widget_from_search_type('twog/platform', 'platform_code', 'name', 'code')
        platform_select_wdg.set_id('platform_code')

        outer_div.add(obu.get_label_widget('Platform'))
        outer_div.add(platform_select_wdg)

    @staticmethod
    def get_submit_button_behavior(order_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-package-in-order");
    var new_package_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var order_code = '%s';
    var name = new_package_values.new_package_name;
    var platform_code = new_package_values.platform_code;
    var due_date = new_package_values.due_date;

    // Set up the object for the new package entry.
    var new_package = {
        'name': name,
        'order_code': order_code,
        'platform_code': platform_code.value,
        'due_date': due_date
    }

    server.insert('twog/package', new_package);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (order_code)
        }

        return behavior
