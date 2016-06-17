from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseTableElementWdg

from pyasm.prod.biz import ProdSetting
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import SelectWdg


def get_add_colons_for_time_behavior():
    behavior = {'css_class': 'clickme', 'type': 'keyup', 'cbjs_action': '''
try {
    var entered = bvr.src_el.value;
    var new_str = '';
    entered = entered.replace(/:/g,'');
    for(var r = 0; r < entered.length; r++) {
        if(r % 2 == 0 && r != 0) {
            new_str = new_str + ':';
        }
        new_str = new_str + entered[r];
    }
    bvr.src_el.value = new_str;
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
'''
    }

    return behavior


class ElementEvalLinesWdg(BaseTableElementWdg):
    def init(self):
        self.report_lines = self.get_kwargs().get('report_lines')



        if self.report_lines:
            self.number_of_lines = len(self.report_lines)
        else:
            self.number_of_lines = 1

    def get_add_row_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    var element_eval_lines_table = document.getElementById('element_eval_lines_table');
    var element_eval_lines_table_rows = element_eval_lines_table.getElementsByTagName('tr');

    // One 'tr' is the header, so ignore that
    var number_of_lines = element_eval_lines_table_rows.length - 1;

    var lines = [];

    for (var i = 0; i < number_of_lines; i++) {
        var timecode_in_value = document.getElementsByName("timecode-in-" + String(i))[0].value;
        var field_in_value = document.getElementsByName("field-in-" + String(i))[0].value;
        var description_value = document.getElementsByName("description-" + String(i))[0].value;
        var in_safe_value = document.getElementById("in_safe-" + String(i)).value;
        var timecode_out_value = document.getElementsByName("timecode-out-" + String(i))[0].value;
        var field_out_value = document.getElementsByName("field-out-" + String(i))[0].value;
        var type_code_value = document.getElementById("type-code-" + String(i)).value;
        var scale_value = document.getElementById("scale-" + String(i)).value;
        var sector_or_channel_value = document.getElementsByName("sector-or-channel-" + String(i))[0].value;
        var in_source_value = document.getElementById("in_source-" + String(i))[0].value;

        var line_data = {
            'timecode_in': timecode_in_value,
            'field_in': field_in_value,
            'description': description_value,
            'in_safe': in_safe_value,
            'timecode_out': timecode_out_value,
            'field_out': field_out_value,
            'type_code': type_code_value,
            'scale': scale_value,
            'sector_or_channel': sector_or_channel_value,
            'in_source': in_source_value
        };

        lines.push(line_data);
    }

    // Refresh the widget
    var element_eval_lines_div = document.getElementById('element_eval_lines_div');

    spt.api.load_panel(element_eval_lines_div, 'qc_reports.ElementEvalLinesWdg', {'report_lines': lines});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
'''
        }

        return behavior

    def get_remove_row_behavior(self, row_number):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    if(confirm("Do you really want to delete this line?)) {
        var server = TacticServerStub.get();

        server.retire_sobject(server.build_search_key('twog/element_evaluation_line', code));
    }
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
'''
        }

        return behavior

    def set_header_rows(self, table):
        table.add_row()
        table.add_header("Timecode In")
        table.add_header("&nbsp;F")
        table.add_header("Description")
        table.add_header("In Safe")

        # Some clients want "Duration" instead
        duration_clients = ProdSetting.get_seq_by_key('qc_report_duration_clients')

        if self.kwargs.get('client_code') in duration_clients:
            time_out_label = "Duration"
        else:
            time_out_label = "Timecode Out"

        table.add_header(time_out_label)
        table.add_header("&nbsp;F")
        table.add_header("Code")
        table.add_header("Scale")
        table.add_header("Sector/Ch")
        table.add_header("In Source")

    def get_text_input_wdg(self, name, width=200):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if hasattr(self, name):
            textbox_wdg.set_value(getattr(self, name))

        return textbox_wdg

    def get_timecode_textbox(self, name, width=200):
        timecode_textbox = TextInputWdg()
        timecode_textbox.set_id(name)
        timecode_textbox.set_name(name)
        timecode_textbox.add_style('width', '{0}px'.format(width))

        timecode_textbox.add_behavior(get_add_colons_for_time_behavior())

        if hasattr(self, name):
            self.set_value(getattr(self, name))

        return timecode_textbox

    def get_select_wdg(self, name, options):
        select_wdg = SelectWdg(name)
        select_wdg.set_id(name)
        select_wdg.add_empty_option()

        for option_set in options:
            label = option_set[0]
            value = option_set[1]

            select_wdg.append_option(label, value)

        return select_wdg

    def get_add_row_button(self):
        span_wdg = SpanWdg()

        add_row_button = ButtonNewWdg(title='Add Row', icon='ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_style('display', 'inline-block')
        add_row_button.add_behavior(self.get_add_row_behavior())

        span_wdg.add(add_row_button)

        return span_wdg

    def get_remove_row_button(self, row_number):
        span_wdg = SpanWdg()

        remove_row_button = ButtonNewWdg(title='Remove Row', icon='REMOVE')

        remove_row_button.add_class('subtract_row_button')
        remove_row_button.add_style('display', 'inline-block')
        remove_row_button.add_behavior(self.get_remove_row_behavior(row_number))

        span_wdg.add(remove_row_button)

        return span_wdg

    def add_row(self, table, current_row, data=None):
        table.add_row()

        in_safe_options = [('Yes', True), ('No', False)]
        type_code_options = [('Film', 'film'), ('Video', 'video'), ('Telecine', 'telecine'), ('Audio', 'audio')]
        scale_select_options = [('1', '1'), ('2', '2'), ('3', '3'), ('FYI', 'fyi')]
        in_source_options = [('No', 'no'), ('Yes', 'yes'), ('New', 'new'), ('Approved', 'approved'),
                             ('Fixed', 'fixed'), ('Not Fixed', 'not_fixed'),
                             ('Approved by Production', 'approved_by_production'),
                             ('Approved by Client', 'approved_by_client'), ('Approved as is', 'approved_as_is'),
                             ('Approved by Territory', 'approved_by_territory')]

        table.add_cell(self.get_timecode_textbox('timecode-in-{0}'.format(current_row), 100))
        table.add_cell(self.get_text_input_wdg('field-in-{0}'.format(current_row), 30))
        table.add_cell(self.get_text_input_wdg('description-{0}'.format(current_row), 450))
        table.add_cell(self.get_select_wdg('in_safe-{0}'.format(current_row), in_safe_options))
        table.add_cell(self.get_timecode_textbox('timecode-out-{0}'.format(current_row), 100))
        table.add_cell(self.get_text_input_wdg('field-out-{0}'.format(current_row), 30))
        table.add_cell(self.get_select_wdg('type-code-{0}'.format(current_row), type_code_options))
        table.add_cell(self.get_select_wdg('scale-{0}'.format(current_row), scale_select_options))
        table.add_cell(self.get_text_input_wdg('sector-or-channel-{0}'.format(current_row), 100))
        table.add_cell(self.get_select_wdg('in_source-{0}'.format(current_row), in_source_options))
        table.add_cell(self.get_remove_row_button(current_row))

    def get_display(self):
        table = Table()
        table.set_id('element_eval_lines_table')

        self.set_header_rows(table)

        current_row = 0

        if self.report_lines:
            for report_line in self.report_lines:
                self.add_row(table, current_row, report_line)
                current_row += 1

        self.add_row(table, current_row)

        table.add_cell(self.get_add_row_button())

        main_div = DivWdg()
        main_div.set_id('element_eval_lines_div')
        main_div.add(table)

        return main_div
