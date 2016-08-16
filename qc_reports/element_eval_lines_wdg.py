from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseRefreshWdg

from pyasm.prod.biz import ProdSetting
from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import SelectWdg

from utils import get_add_colons_for_time_behavior


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
function getTableRowsWithAttribute(table, attribute)
{
  var matchingElements = [];
  var allElements = table.getElementsByTagName('tr');
  for (var i = 0, n = allElements.length; i < n; i++)
  {
    if (allElements[i].getAttribute(attribute) !== null)
    {
      // Element exists with attribute. Add to array.
      matchingElements.push(allElements[i]);
    }
  }
  return matchingElements;
}

try {
    var element_evaluation_code = '%s';

    var element_eval_lines_table = document.getElementById('element_eval_lines_table');
    var table_rows = getTableRowsWithAttribute(element_eval_lines_table, 'code');

    var server = TacticServerStub.get();

    // Get a dictionary of all the line items, indexed by search key. This is to send all the lines to the database
    // at once and avoid multiple insert queries (ends up being really slow).
    var lines = {};

    for (var i = 0; i < table_rows.length; i++) {
        var line_data = {};

        line_data['timecode_in'] = document.getElementsByName("timecode-in-" + String(i))[0].value;
        line_data['field_in'] = document.getElementsByName("field-in-" + String(i))[0].value;
        line_data['description'] = document.getElementsByName("description-" + String(i))[0].value;
        line_data['in_safe'] = document.getElementById("in-safe-" + String(i)).value;
        line_data['timecode_out'] = document.getElementsByName("timecode-out-" + String(i))[0].value;
        line_data['field_out'] = document.getElementsByName("field-out-" + String(i))[0].value;
        line_data['type_code'] = document.getElementById("type-code-" + String(i)).value;
        line_data['scale'] = document.getElementById("scale-" + String(i)).value;
        line_data['sector_or_channel'] = document.getElementsByName("sector-or-channel-" + String(i))[0].value;
        line_data['in_source'] = document.getElementById("in-source-" + String(i))[0].value;

        var search_key = server.build_search_key('twog/element_evaluation_line', table_rows[i].getAttribute('code'),
                                                 'twog');

        lines[search_key] = line_data;
    }

    // Update all the lines at once
    server.update_multiple(lines);

    // Insert a blank line
    server.insert('twog/element_evaluation_line', {'element_evaluation_code': element_evaluation_code});

    // Refresh the widget
    var element_eval_lines_div = document.getElementById('element_eval_lines_div');

    spt.api.load_panel(element_eval_lines_div, 'qc_reports.ElementEvalLinesWdg',
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
function getTableRowsWithAttribute(table, attribute)
{
  var matchingElements = [];
  var allElements = table.getElementsByTagName('tr');
  for (var i = 0, n = allElements.length; i < n; i++)
  {
    if (allElements[i].getAttribute(attribute) !== null)
    {
      // Element exists with attribute. Add to array.
      matchingElements.push(allElements[i]);
    }
  }
  return matchingElements;
}

try {
    var element_evaluation_code = '%s';

    var element_eval_lines_table = document.getElementById('element_eval_lines_table');
    var table_rows = getTableRowsWithAttribute(element_eval_lines_table, 'code');

    var server = TacticServerStub.get();

    var number_of_lines = Number(prompt('Enter the amount of lines you want to add.'));

    if (isNaN(number_of_lines)) {
        alert("Your entry was invalid, please enter only a number");
        return;
    }

    // Get a dictionary of all the line items, indexed by search key. This is to send all the lines to the database
    // at once and avoid multiple insert queries (ends up being really slow).
    var lines = {};

    for (var i = 0; i < table_rows.length; i++) {
        var line_data = {};

        line_data['timecode_in'] = document.getElementsByName("timecode-in-" + String(i))[0].value;
        line_data['field_in'] = document.getElementsByName("field-in-" + String(i))[0].value;
        line_data['description'] = document.getElementsByName("description-" + String(i))[0].value;
        line_data['in_safe'] = document.getElementById("in-safe-" + String(i)).value;
        line_data['timecode_out'] = document.getElementsByName("timecode-out-" + String(i))[0].value;
        line_data['field_out'] = document.getElementsByName("field-out-" + String(i))[0].value;
        line_data['type_code'] = document.getElementById("type-code-" + String(i)).value;
        line_data['scale'] = document.getElementById("scale-" + String(i)).value;
        line_data['sector_or_channel'] = document.getElementsByName("sector-or-channel-" + String(i))[0].value;
        line_data['in_source'] = document.getElementById("in-source-" + String(i))[0].value;

        var search_key = server.build_search_key('twog/element_evaluation_line', table_rows[i].getAttribute('code'),
                                                 'twog');

        lines[search_key] = line_data;
    }

    // Update all the lines at once
    server.update_multiple(lines);

    // Insert multiple blank lines. Unfortunately, as far as I know, insert_multiple does not work, and each line
    // must be inserted individually
    for (var x = 0; x < number_of_lines; x++) {
        server.insert('twog/element_evaluation_line', {'element_evaluation_code': element_evaluation_code})
    }

    // Refresh the widget
    var element_eval_lines_div = document.getElementById('element_eval_lines_div');

    spt.api.load_panel(element_eval_lines_div, 'qc_reports.ElementEvalLinesWdg',
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
        var element_eval_lines_div = document.getElementById('element_eval_lines_div');

        spt.api.load_panel(element_eval_lines_div, 'qc_reports.ElementEvalLinesWdg',
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

    @staticmethod
    def get_text_input_wdg_for_element_eval_lines(name, width=200, line_data=None):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if line_data:
            textbox_wdg.set_value(line_data)

        return textbox_wdg

    def get_timecode_textbox(self, name, width=200, line_data=None):
        timecode_textbox = TextInputWdg()
        timecode_textbox.set_id(name)
        timecode_textbox.set_name(name)
        timecode_textbox.add_style('width', '{0}px'.format(width))

        timecode_textbox.add_behavior(get_add_colons_for_time_behavior())

        if line_data:
            timecode_textbox.set_value(line_data)

        return timecode_textbox

    @staticmethod
    def get_select_wdg(name, options, saved_value=None):
        select_wdg = SelectWdg(name)
        select_wdg.set_id(name)
        select_wdg.add_empty_option()

        for option_set in options:
            label = option_set[0]
            value = option_set[1]

            select_wdg.append_option(label, value)

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
                                 ('Approved by Territory', 'approved_by_territory')]

            for iterator, line in enumerate(self.lines):
                current_row = table.add_row()
                current_row.add_attr('code', line.get_code())

                table.add_cell(
                    self.get_timecode_textbox('timecode-in-{0}'.format(iterator), 150, line.get_value('timecode_in'))
                )
                table.add_cell(
                    self.get_text_input_wdg_for_element_eval_lines('field-in-{0}'.format(iterator), 30,
                                                                   line.get_value('field_in'))
                )
                table.add_cell(
                    self.get_text_input_wdg_for_element_eval_lines('description-{0}'.format(iterator), 400,
                                                                   line.get_value('description'))
                )
                table.add_cell(
                    self.get_select_wdg('in-safe-{0}'.format(iterator), in_safe_options, line.get_value('in_safe'))
                )
                table.add_cell(
                    self.get_timecode_textbox('timecode-out-{0}'.format(iterator), 150, line.get_value('timecode_out'))
                )
                table.add_cell(
                    self.get_text_input_wdg_for_element_eval_lines('field-out-{0}'.format(iterator), 30,
                                                                   line.get_value('field_out'))
                )
                table.add_cell(
                    self.get_select_wdg('type-code-{0}'.format(iterator), type_code_options, line.get_value('type_code'))
                )
                table.add_cell(
                    self.get_select_wdg('scale-{0}'.format(iterator), scale_select_options, line.get_value('scale'))
                )
                table.add_cell(
                    self.get_text_input_wdg_for_element_eval_lines('sector-or-channel-{0}'.format(iterator), 150,
                                                                   line.get_value('sector_or_channel'))
                )
                table.add_cell(
                    self.get_select_wdg('in-source-{0}'.format(iterator), in_source_options, line.get_value('in_source'))
                )
                table.add_cell(
                    self.get_remove_row_button(line.get_code())
                )
        else:
            table.add_cell("No Element Evaluation lines exist yet. Add one?")

        table.add_cell(self.get_add_row_button())
        table.add_cell(self.get_add_multiple_rows_button())

        main_div = DivWdg()
        main_div.set_id('element_eval_lines_div')
        main_div.add_style('margin', '10px')
        main_div.add(table)

        return main_div
