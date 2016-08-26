from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextAreaInputWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import MultiSelectWdg, SubmitWdg

import order_builder_utils as obu


class InsertPackageInOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-package-in-order')

        outer_div.add(obu.get_text_input_wdg('new_package_name', 400))
        self.get_platform_select_widget(outer_div)

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

    console.log(new_package_values);

    // Get the form values
    var order_code = '%s';
    var name = new_package_values.new_package_name;
    var platform_code = new_package_values.platform_code;

    console.log(name);

    // Set up the object for the new package entry.
    // Set up the object for the new package entry.
    var new_package = {
        'name': name,
        'order_code': order_code,
        'platform_code': platform_code.value,
    }

    server.insert('twog/package', new_package);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (order_code)
        }

        return behavior
