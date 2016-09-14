from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, Table
from pyasm.widget import CheckboxWdg, MultiSelectWdg, SubmitWdg

import order_builder.order_builder_utils as obu


def get_files_checkboxes_for_division(division_code):
    file_search = Search('twog/file')
    file_search.add_filter('division_code', division_code)
    files = file_search.get_sobjects()

    files_checkbox_table = Table()

    header_row = files_checkbox_table.add_row()
    header = files_checkbox_table.add_header(data='Files', row=header_row)
    header.add_style('text-align', 'center')
    header.add_style('text-decoration', 'underline')

    for file_sobject in files:
        checkbox = CheckboxWdg(name=file_sobject.get_code())

        checkbox_row = files_checkbox_table.add_row()

        files_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
        files_checkbox_table.add_cell(data=file_sobject.get_value('name'), row=checkbox_row)

    return files_checkbox_table

class AddFilesToOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()

        division_search = Search('twog/division')
        division_search.add_code_filter(self.order_sobject.get('division_code'))
        self.division_sobject = division_search.get_sobject()

    @staticmethod
    def get_submit_button_behavior(order_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#add_files_to_order");
var values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var order_code = '%s';

var files = server.eval("@SOBJECT(twog/file)");

for (var i = 0; i < files.length; i++) {
    var file_code = files[i].code;

    var file_checkbox_value = values[file_code];

    if (file_checkbox_value == "on") {
        var new_entry = {
            'order_code': order_code,
            'file_code': file_code
        }

        server.insert('twog/file_in_order', new_entry);
    }
}

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));
            ''' % order_code
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('add_files_to_order')

        outer_div.add(get_files_checkboxes_for_division(self.division_sobject.get_code()))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.order_sobject.get_code()))

        outer_div.add(submit_button)

        return outer_div
