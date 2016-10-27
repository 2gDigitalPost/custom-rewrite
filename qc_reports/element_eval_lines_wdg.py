from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseRefreshWdg

from pyasm.prod.biz import ProdSetting
from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import HiddenWdg, SelectWdg

from utils import get_text_input_wdg, get_add_colons_for_time_behavior


class ElementEvalLinesWdg(BaseRefreshWdg):
    def init(self):
        self.element_evaluation_code = self.kwargs.get('element_evaluation_code')

        if self.element_evaluation_code:
            lines_search = Search('twog/element_evaluation_line')
            lines_search.add_filter('element_evaluation_code', self.element_evaluation_code)

            lines = lines_search.get_sobjects()
            lines_with_values = []
            lines_without_values = []

            for line in lines:
                if line.get_value('timecode_in'):
                    lines_with_values.append(line)
                else:
                    lines_without_values.append(line)

            self.lines = sorted(lines_with_values, key=lambda x: x.get_value('timecode_in'))
            self.lines.extend(lines_without_values)
        else:
            self.lines = []

    def get_add_row_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    var element_evaluation_code = '%s';

    var server = TacticServerStub.get();

    var number_of_lines = 0;

    while (true)
    {
        if (report_values.hasOwnProperty("timecode-in-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

    // Get a dictionary of all the line items, indexed by search key. This is to send all the lines to the database
    // at once and avoid multiple insert queries (ends up being really slow).
    lines = {};

    for (var i = 0; i < number_of_lines; i++) {
        var line_data = {};

        line_data['timecode_in'] = report_values["timecode-in-" + String(i)];
        line_data['field_in'] = report_values["field-in-" + String(i)];
        line_data['description'] = report_values["description-" + String(i)];
        line_data['in_safe'] = report_values["in-safe-" + String(i)];
        line_data['timecode_out'] = report_values["timecode-out-" + String(i)];
        line_data['field_out'] = report_values["field-out-" + String(i)];
        line_data['type_code'] = report_values["type-code-" + String(i)];
        line_data['scale'] = report_values["scale-" + String(i)];
        line_data['sector_or_channel'] = report_values["sector-or-channel-" + String(i)];
        line_data['in_source'] = report_values["in-source-" + String(i)];

        line_data_code = report_values["element-eval-line-code-" + String(i)];

        var search_key = server.build_search_key('twog/element_evaluation_line', line_data_code, 'twog');

        lines[search_key] = line_data;
    }

    // Update all the lines at once
    server.update_multiple(lines);

    // Insert a blank line
    server.insert('twog/element_evaluation_line', {'element_evaluation_code': element_evaluation_code,
                                                   'checked': true});

    // Refresh the widget
    spt.api.load_panel(bvr.src_el.getParent('#element_eval_lines_div'), 'qc_reports.ElementEvalLinesWdg',
                       {'element_evaluation_code': element_evaluation_code});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % self.element_evaluation_code
        }

        return behavior

    def get_add_multiple_rows_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    var element_evaluation_code = '%s';

    var server = TacticServerStub.get();

    var number_of_lines_to_insert = Number(prompt('Enter the amount of lines you want to add.'));

    if (isNaN(number_of_lines_to_insert)) {
        alert("Your entry was invalid, please enter only a number");
        return;
    }

    var number_of_lines = 0;

    while (true)
    {
        if (report_values.hasOwnProperty("timecode-in-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

    // Get a dictionary of all the line items, indexed by search key. This is to send all the lines to the database
    // at once and avoid multiple insert queries (ends up being really slow).
    lines = {};

    for (var i = 0; i < number_of_lines; i++) {
        var line_data = {};

        line_data['timecode_in'] = report_values["timecode-in-" + String(i)];
        line_data['field_in'] = report_values["field-in-" + String(i)];
        line_data['description'] = report_values["description-" + String(i)];
        line_data['in_safe'] = report_values["in-safe-" + String(i)];
        line_data['timecode_out'] = report_values["timecode-out-" + String(i)];
        line_data['field_out'] = report_values["field-out-" + String(i)];
        line_data['type_code'] = report_values["type-code-" + String(i)];
        line_data['scale'] = report_values["scale-" + String(i)];
        line_data['sector_or_channel'] = report_values["sector-or-channel-" + String(i)];
        line_data['in_source'] = report_values["in-source-" + String(i)];

        line_data_code = report_values["element-eval-line-code-" + String(i)];

        var search_key = server.build_search_key('twog/element_evaluation_line', line_data_code, 'twog');

        lines[search_key] = line_data;
    }

    // Update all the lines at once
    server.update_multiple(lines);

    // Insert multiple blank lines. Unfortunately, as far as I know, insert_multiple does not work, and each line
    // must be inserted individually
    for (var x = 0; x < number_of_lines_to_insert; x++) {
        server.insert('twog/element_evaluation_line', {'element_evaluation_code': element_evaluation_code,
                                                       'checked': true});
    }

    // Refresh the widget
    spt.api.load_panel(bvr.src_el.getParent('#element_eval_lines_div'), 'qc_reports.ElementEvalLinesWdg',
                       {'element_evaluation_code': element_evaluation_code});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
        ''' % self.element_evaluation_code
        }

        return behavior

    def get_remove_row_behavior(self, row_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    if(confirm("Do you really want to delete this line?")) {
        var server = TacticServerStub.get();
        var element_evaluation_code = '%s';
        var code = '%s';

        server.retire_sobject(server.build_search_key('twog/element_evaluation_line', code, 'twog'));

        // Refresh the widget
        spt.api.load_panel(bvr.src_el.getParent('#element_eval_lines_div'), 'qc_reports.ElementEvalLinesWdg',
                           {'element_evaluation_code': element_evaluation_code});
    }
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % (self.element_evaluation_code, row_code)
        }

        return behavior

    def get_checked_row_behavior(self, row_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Return an object containing the element evaluation's values
var top = bvr.src_el.getParent("#element_eval_panel");
var report_values = spt.api.get_input_values(top, null, false);

var element_evaluation_code = '%s';

var server = TacticServerStub.get();

var number_of_lines = 0;

while (true)
{
    if (report_values.hasOwnProperty("timecode-in-" + String(number_of_lines))) {
        number_of_lines++;
    }
    else {
        break;
    }
}

// Get a dictionary of all the line items, indexed by search key. This is to send all the lines to the database
// at once and avoid multiple insert queries (ends up being really slow).
lines = {};

for (var i = 0; i < number_of_lines; i++) {
    var line_data = {};

    line_data['timecode_in'] = report_values["timecode-in-" + String(i)];
    line_data['field_in'] = report_values["field-in-" + String(i)];
    line_data['description'] = report_values["description-" + String(i)];
    line_data['in_safe'] = report_values["in-safe-" + String(i)];
    line_data['timecode_out'] = report_values["timecode-out-" + String(i)];
    line_data['field_out'] = report_values["field-out-" + String(i)];
    line_data['type_code'] = report_values["type-code-" + String(i)];
    line_data['scale'] = report_values["scale-" + String(i)];
    line_data['sector_or_channel'] = report_values["sector-or-channel-" + String(i)];
    line_data['in_source'] = report_values["in-source-" + String(i)];

    line_data_code = report_values["element-eval-line-code-" + String(i)];

    var search_key = server.build_search_key('twog/element_evaluation_line', line_data_code, 'twog');

    lines[search_key] = line_data;
}

// Update all the lines at once
server.update_multiple(lines);

var line_code = '%s';

var checked_line_search_key = server.build_search_key('twog/element_evaluation_line', line_code, 'twog');

server.update(checked_line_search_key, {'checked': true});

// Refresh the widget
spt.api.load_panel(bvr.src_el.getParent('#element_eval_lines_div'), 'qc_reports.ElementEvalLinesWdg',
                   {'element_evaluation_code': element_evaluation_code});
''' % (self.element_evaluation_code, row_code)
        }

        return behavior

    @staticmethod
    def get_text_input_for_element_eval_line_wdg(name, data, is_checked, width=200, timecode=False):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if not is_checked:
            textbox_wdg.add_style('font-weight', 'bold')

        if timecode:
            textbox_wdg.add_behavior(get_add_colons_for_time_behavior())

        if data:
            textbox_wdg.set_value(data)

        return textbox_wdg

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
        table.add_header("Code")
        table.add_header("Scale")
        table.add_header("Sector/Ch")
        table.add_header("In Source")

    @staticmethod
    def get_select_wdg(name, options, is_checked, saved_value=None):
        select_wdg = SelectWdg(name)
        select_wdg.set_id(name)
        select_wdg.add_empty_option()

        for option_set in options:
            label = option_set[0]
            value = option_set[1]

            select_wdg.append_option(label, value)

        if not is_checked:
            select_wdg.add_style('font-weight', 'bold')

        if saved_value:
            select_wdg.set_value(saved_value)

        return select_wdg

    def get_add_row_button(self):
        span_wdg = SpanWdg()

        add_row_button = ButtonNewWdg(title='Add Row', icon='ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_style('display', 'inline-block')
        add_row_button.add_behavior(self.get_add_row_behavior())

        span_wdg.add(add_row_button)

        return span_wdg

    def get_add_multiple_rows_button(self):
        span_wdg = SpanWdg()

        # TODO: Find a better icon for this
        add_row_button = ButtonNewWdg(title='Add Multiple Row', icon='PLUS_ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_style('display', 'inline-block')
        add_row_button.add_behavior(self.get_add_multiple_rows_behavior())

        span_wdg.add(add_row_button)

        return span_wdg

    def get_remove_row_button(self, row_code):
        span_wdg = SpanWdg()

        remove_row_button = ButtonNewWdg(title='Remove Row', icon='DELETE')

        remove_row_button.add_class('subtract_row_button')
        remove_row_button.add_style('display', 'inline-block')
        remove_row_button.add_behavior(self.get_remove_row_behavior(row_code))

        span_wdg.add(remove_row_button)

        return span_wdg

    def get_row_checked_button(self, row_code):
        span_wdg = SpanWdg()

        checked_row_button = ButtonNewWdg(title='Checked Row', icon='CHECK')
        checked_row_button.add_style('display', 'inline-block')
        checked_row_button.add_behavior(self.get_checked_row_behavior(row_code))

        span_wdg.add(checked_row_button)

        return span_wdg

    def get_display(self):
        table = Table()
        table.set_id('element_eval_lines_table')

        if self.lines:
            self.set_header_rows(table)

            in_safe_options = [('Yes', True), ('No', False)]
            type_code_options = [('Film', 'film'), ('Video', 'video'), ('Telecine', 'telecine'), ('Audio', 'audio')]
            scale_select_options = [('1', '1'), ('2', '2'), ('3', '3'), ('FYI', 'fyi')]
            in_source_options = [('No', 'no'), ('Yes', 'yes'), ('New', 'new'), ('Approved', 'approved'),
                                 ('Fixed', 'fixed'), ('Not Fixed', 'not_fixed'),
                                 ('Approved by Production', 'approved_by_production'),
                                 ('Approved by Client', 'approved_by_client'), ('Approved as is', 'approved_as_is'),
                                 ('Approved by Territory', 'approved_by_territory'),
                                 ('From Approved Master', 'from_approved_master')]

            for iterator, line in enumerate(self.lines):
                table.add_row()

                table.add_cell(
                    self.get_text_input_for_element_eval_line_wdg('timecode-in-{0}'.format(iterator),
                                                                  line.get_value('timecode_in'),
                                                                  line.get_value('checked'), 150, timecode=True)
                )
                table.add_cell(
                    self.get_text_input_for_element_eval_line_wdg('field-in-{0}'.format(iterator),
                                                                  line.get_value('field_in'), line.get_value('checked'),
                                                                  50)
                )
                table.add_cell(
                    self.get_text_input_for_element_eval_line_wdg('description-{0}'.format(iterator),
                                                                  line.get_value('description'),
                                                                  line.get_value('checked'), 400)
                )
                table.add_cell(
                    self.get_select_wdg('in-safe-{0}'.format(iterator), in_safe_options, line.get_value('checked'),
                                        line.get_value('in_safe'))
                )
                table.add_cell(
                    self.get_text_input_for_element_eval_line_wdg('timecode-out-{0}'.format(iterator),
                                                                  line.get_value('timecode_out'),
                                                                  line.get_value('checked'), 150, timecode=True)
                )
                table.add_cell(
                    self.get_select_wdg('type-code-{0}'.format(iterator), type_code_options,
                                        line.get_value('checked'), line.get_value('type_code'))
                )
                table.add_cell(
                    self.get_select_wdg('scale-{0}'.format(iterator), scale_select_options,
                                        line.get_value('checked'), line.get_value('scale'))
                )
                table.add_cell(
                    self.get_text_input_for_element_eval_line_wdg('sector-or-channel-{0}'.format(iterator),
                                                                  line.get_value('sector_or_channel'),
                                                                  line.get_value('checked'), 150)
                )
                table.add_cell(
                    self.get_select_wdg('in-source-{0}'.format(iterator), in_source_options,
                                        line.get_value('checked'), line.get_value('in_source'))
                )
                table.add_cell(
                    HiddenWdg('element-eval-line-code-{0}'.format(iterator), line.get_code())
                )
                table.add_cell(
                    self.get_remove_row_button(line.get_code())
                )

                if not line.get_value('checked'):
                    table.add_cell(self.get_row_checked_button(line.get_code()))
        else:
            table.add_cell("No Element Evaluation lines exist yet. Add one?")

        table.add_cell(self.get_add_row_button())
        table.add_cell(self.get_add_multiple_rows_button())

        main_div = DivWdg()
        main_div.set_id('element_eval_lines_div')
        main_div.add_style('margin', '10px')
        main_div.add(table)

        return main_div
