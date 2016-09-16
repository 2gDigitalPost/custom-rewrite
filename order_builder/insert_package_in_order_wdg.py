from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table
from pyasm.widget import CheckboxWdg, SubmitWdg

import order_builder_utils as obu


def get_platforms_checkboxes():
    platform_search = Search('twog/platform')
    platforms = platform_search.get_sobjects()

    platforms_checkbox_table = Table()

    header_row = platforms_checkbox_table.add_row()
    header = platforms_checkbox_table.add_header(data='Platforms', row=header_row)
    header.add_style('text-align', 'center')
    header.add_style('text-decoration', 'underline')

    for platform in platforms:
        checkbox = CheckboxWdg(name=platform.get_code())

        checkbox_row = platforms_checkbox_table.add_row()

        platforms_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
        platforms_checkbox_table.add_cell(data=platform.get_value('name'), row=checkbox_row)

    return platforms_checkbox_table


class InsertPackageInOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-package-in-order')

        outer_div.add(obu.get_label_widget('Name'))
        outer_div.add(obu.get_text_input_wdg('new_package_name', 400))

        self.get_platform_select_widget(outer_div)

        outer_div.add(obu.get_label_widget('Due Date'))
        outer_div.add(obu.get_date_calendar_wdg())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_platform_select_widget(outer_div):
        platform_select_wdg = obu.get_select_widget_from_search_type('twog/platform', 'platform_code', 'name', 'code')
        platform_select_wdg.set_id('platform_code')

        outer_div.add(obu.get_label_widget('Platform'))
        outer_div.add(platform_select_wdg)

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.app_busy.show("Saving...");

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
}''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name, self.parent_widget_search_key)
        }

        return behavior


class InsertPackageByPlatformWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-package-in-order')

        outer_div.add(obu.get_label_widget('Name'))
        outer_div.add(obu.get_text_input_wdg('new_package_name', 400))

        outer_div.add(get_platforms_checkboxes())

        outer_div.add(obu.get_label_widget('Due Date'))
        outer_div.add(obu.get_date_calendar_wdg())

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
    spt.app_busy.show("Saving...");

    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-package-by-platform");
    var new_package_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var order_code = '%s';
    var new_name = new_package_values.new_package_name;
    var due_date = new_package_values.due_date;

    // Get all the platforms saved in the database
    var platforms = server.eval("@SOBJECT(twog/platform)");

    for (var i = 0; i < platforms.length; i++) {
        var platform_code = platforms[i].code;

        var platform_checkbox_value = new_package_values[platform_code];

        if (platform_checkbox_value == "on") {
            var platform_name = platforms[i].name;

            // Set up the object for the new package entry.
            var new_package = {
                'name': new_name + " - " + platform_name,
                'order_code': order_code,
                'platform_code': platform_code,
                'due_date': due_date
            }

            server.insert('twog/package', new_package);
        }
    }

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
}''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name, self.parent_widget_search_key)
        }

        return behavior
