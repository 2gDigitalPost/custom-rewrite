from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.web import DivWdg, HtmlElement, Table
from pyasm.widget import CheckboxWdg, SubmitWdg

import order_builder.order_builder_utils as obu

from common_tools import get_component_sobjects_from_order_code, get_package_sobjects_from_order_code


class LinkComponentsToPackagesWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('link_components_to_packages_div')

        table = Table()
        table.add_attr('id', 'link_components_to_packages_table')
        table.add_style('width', '100%')
        table.add_border(style='solid', color='#F2F2F2', size='1px')

        order_code = self.order_sobject.get_code()

        components = get_component_sobjects_from_order_code(order_code)
        packages = get_package_sobjects_from_order_code(order_code)

        package_row = table.add_row()
        table.add_cell(row=package_row)

        for package in packages:
            table.add_cell(package.get('name'), row=package_row)

        for component in components:
            component_row = table.add_row()
            component_row.set_id(component.get_code())

            table.add_cell(component.get('name'), row=component_row)

            for package in packages:
                checkbox = CheckboxWdg(name='{0}_{1}'.format(component.get_code(), package.get_code()))

                checkbox_cell = table.add_cell(checkbox)
                checkbox_cell.add_style('text-align', 'center')

        outer_div.add(table)

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())

        outer_div.add(submit_button)

        return outer_div

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
spt.app_busy.show('Saving...');

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#link_components_to_packages_div");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var order_code = '%s';
var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

console.log(values);

component_package_keys = Object.keys(values);

for (var i = 0; i < component_package_keys.length; i++) {
    var component_package_key = component_package_keys[i];
    var split_component_package_key = component_package_key.split("_");

    var checkbox_value = values[component_package_key];

    var component_code = split_component_package_key[0];
    var package_code = split_component_package_key[1];

    var existing_entry = server.eval("@SOBJECT(twog/component_files_to_package['component_code', '" + component_code +
                                     "']['package_code', '" + package_code + "'])");

    if (checkbox_value == "on") {
        // Only insert a new entry if one does not already exist.
        if (existing_entry.length == 0) {
            var new_entry = {
                'component_code': component_code,
                'package_code': package_code
            }

            server.insert('twog/component_files_to_package', new_entry);
        }
    }
    else {
        // If a box is unchecked, remove any entries in the database that exist (in other words, if a box was checked
        // but is now unchecked, the user meant to remove the connection)
        if (existing_entry.length > 0)
        {
            server.delete_sobject(existing_entry[0].__search_key__);
        }
    }
}

/*
var equipment = server.eval("@SOBJECT(twog/equipment)");

for (var i = 0; i < equipment.length; i++) {
    var equipment_code = equipment[i].code;

    var file_checkbox_value = values[equipment_code];

    var existing_entry = server.eval("@SOBJECT(twog/equipment_in_task_data['equipment_code', '" +
                                     equipment_code + "']['task_data_code',  '" + task_data_code + "'])");

    if (file_checkbox_value == "on") {
        // Only insert a new entry if one does not already exist.
        if (existing_entry.length == 0) {
            var new_entry = {
                'task_data_code': task_data_code,
                'equipment_code': equipment_code
            }

            server.insert('twog/equipment_in_task_data', new_entry);
        }
    }
    else {
        // If a box is unchecked, remove any entries in the database that exist (in other words, if a box was checked
        // but is now unchecked, the user meant to remove the connection)
        if (existing_entry.length > 0)
        {
            server.delete_sobject(existing_entry[0].__search_key__);
        }
    }
}
*/

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
            ''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
                   self.parent_widget_search_key)
        }

        return behavior
