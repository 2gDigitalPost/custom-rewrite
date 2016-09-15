from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table
from pyasm.widget import CheckboxWdg, SubmitWdg


class EquipmentInTaskWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()

        task_data_search = Search('twog/task_data')
        task_data_search.add_filter('task_code', self.task_sobject.get_code())
        self.task_data = task_data_search.get_sobject()

        equipment_in_task_data_search = Search('twog/equipment_in_task_data')
        equipment_in_task_data_search.add_filter('task_data_code', self.task_data.get_code())
        equipment_in_task_data = equipment_in_task_data_search.get_sobjects()
        equipment_in_task_data_string = ','.join(
            ["'{0}'".format(equipment.get('equipment_code')) for equipment in equipment_in_task_data])

        equipment_search = Search('twog/equipment')
        equipment_search.add_where('\"code\" in ({0})'.format(equipment_in_task_data_string))
        self.selected_equipment = equipment_search.get_sobjects()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('equipment-in-task')

        outer_div.add(self.get_equipment_checkboxes())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.task_data.get_code()))

        outer_div.add(submit_button)

        return outer_div

    def get_equipment_checkboxes(self):
        equipment_search = Search('twog/equipment')
        equipment = equipment_search.get_sobjects()

        equipment_checkbox_table = Table()

        for equipment_sobject in equipment:
            checkbox = CheckboxWdg(name=equipment_sobject.get_code())

            if equipment_sobject.get_code() in [equipment.get_code() for equipment in self.selected_equipment]:
                checkbox.set_checked()

            checkbox_row = equipment_checkbox_table.add_row()

            equipment_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
            equipment_checkbox_table.add_cell(data=equipment_sobject.get_value('name'), row=checkbox_row)

        return equipment_checkbox_table

    @staticmethod
    def get_submit_button_behavior(task_data_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#equipment-in-task");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var task_data_code = '%s';

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

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));
            ''' % task_data_code
        }

        return behavior
