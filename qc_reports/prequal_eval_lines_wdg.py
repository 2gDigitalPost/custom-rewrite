from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import SelectWdg

from utils import get_add_colons_for_time_behavior


class PrequalEvalLinesWdg(BaseRefreshWdg):
    def init(self):
        self.prequal_eval_code = self.kwargs.get('prequal_eval_code')

        if self.prequal_eval_code:
            lines_search = Search('twog/prequal_evaluation_line')
            lines_search.add_filter('prequal_evaluation_code', self.prequal_eval_code)

            lines = lines_search.get_sobjects()
            lines_with_values = []
            lines_without_values = []

            for line in lines:
                if line.get_value('timecode'):
                    lines_with_values.append(line)
                else:
                    lines_without_values.append(line)

            self.lines = sorted(lines_with_values, key=lambda x: x.get_value('timecode'))
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
    var prequal_eval_code = '%s';

    var prequal_eval_lines_table = document.getElementById('prequal_eval_lines_table');
    var table_rows = getTableRowsWithAttribute(prequal_eval_lines_table, 'code');

    var server = TacticServerStub.get();

    for (var i = 0; i < table_rows.length; i++) {
        var line_data = {};

        line_data['timecode'] = document.getElementsByName("timecode-" + String(i))[0].value;
        line_data['field'] = document.getElementsByName("field-" + String(i))[0].value;
        line_data['description'] = document.getElementsByName("description-" + String(i))[0].value;
        line_data['type_code'] = document.getElementById("type-code-" + String(i)).value;
        line_data['scale'] = document.getElementById("scale-" + String(i)).value;
        line_data['sector_or_channel'] = document.getElementsByName("sector-or-channel-" + String(i))[0].value;
        line_data['in_source'] = document.getElementById("in-source-" + String(i))[0].value;

        var search_key = server.build_search_key('twog/prequal_evaluation_line', table_rows[i].getAttribute('code'),
                                                 'twog');

        server.update(search_key, line_data);
    }

    // Insert a blank line
    server.insert('twog/prequal_evaluation_line', {'prequal_evaluation_code': prequal_eval_code});

    // Refresh the widget
    var prequal_eval_lines_div = document.getElementById('prequal_eval_lines_div');

    spt.api.load_panel(prequal_eval_lines_div, 'qc_reports.ElementEvalLinesWdg',
                       {'prequal_eval_code': prequal_eval_code});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
    ''' % self.prequal_eval_code
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
        var prequal_eval_code = '%s';
        var code = '%s';

        server.retire_sobject(server.build_search_key('twog/prequal_evaluation_line', code, 'twog'));

        // Refresh the widget
        var prequal_eval_lines_div = document.getElementById('prequal_eval_lines_div');

        spt.api.load_panel(prequal_eval_lines_div, 'qc_reports.PrequalEvalLinesWdg',
                           {'prequal_eval_code': prequal_eval_code});
    }
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % (self.prequal_eval_code, row_code)
        }

        return behavior

    def set_header_rows(self, table):
        table.add_row()
        table.add_header("Timecode")
        table.add_header("F")
        table.add_header("Description")
        table.add_header("Code")
        table.add_header("Scale")
        table.add_header("Sector/Ch")
        table.add_header("In Source")

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
    def get_text_input_wdg(name, width=200, line_data=None):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if line_data:
            textbox_wdg.set_value(line_data)

        return textbox_wdg

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

    def get_remove_row_button(self, row_code):
        span_wdg = SpanWdg()

        remove_row_button = ButtonNewWdg(title='Remove Row', icon='REMOVE')

        remove_row_button.add_class('subtract_row_button')
        remove_row_button.add_style('display', 'inline-block')
        remove_row_button.add_behavior(self.get_remove_row_behavior(row_code))

        span_wdg.add(remove_row_button)

        return span_wdg

    def get_display(self):
        table = Table()
        table.set_id('prequal_eval_lines_table')

        if self.lines:
            self.set_header_rows(table)

            description_options = (
                "A - Audio dropout: ( )",
                "A - Audio clipping: ( )",
                "A - Audio flutter: ( )",
                "A - Audio tick: ( )",
                "A - Audio tick during dialogue: ( )",
                "A - Audio pop: ( )",
                "A - Audio pop during dialogue: ( )",
                "A - Audio crackle: ( )",
                "A - Audio phasing error: ( )",
                "A - Bad Audio Edit: ( )",
                "A - Missing Effects: ( )",
                "A - Out of sync dialogue: ( )",
                "A - Out of sync effect: ( )",
                "A - Loose ADR: ( )",
                "A - Example of() found throughout program",
                "A - Z Other...",
                "V - Aliasing: ( )",
                "V - Animation Error: ( )",
                "V - Artifacting: ( )",
                "V - Banding: ( )",
                "V - Color Correction Error: ( )",
                "V - Dead Pixel: ( )",
                "V - Digital Hit: ( )",
                "V - Freeze Frame: ( )",
                "V - Interlacing: ( )",
                "V - High Video Levels() mV",
                "V - Low Black Levels - ( ) mV",
                "V - Jump Cut: ( )",
                "V - Luminance Shift: ( )",
                "V - Moire Pattern: ( )",
                "V - Recorded In Digital Hit: ( )",
                "V - Text out of 16x9 safe action: ( )",
                "V - Text out of 4x3 punch safe: ( )",
                "V - Video Dropout: ( )",
                "V - Video Stepping: ( )",
                "V - Example of() found throughout program",
                "V - Z Other...",
                "V - Start Of Program: ( )",
                "V - Aliasing During Fox Logo: ( )",
                "V - Start Of Program: ( )",
                "V - Aliasing During Fox Logo: ( )",
                "V - Force Narrative Translation Overlaps ENG Burned in Narrative: ( )",
                "V - End Of Program: ( )",
                "V - Dub Card: ( )",
                "V - Text Over Picture: ( )",
                "V - Negative dirt: ( )",
                "V - Stain: ( )",
                "V - Emulsion stain: ( )",
                "V - Scratch: ( )",
                "A - Mis - time: ( )",
                "A - Capstan hit: ( )",
                "V - Noticeable jitter throughout opening sequence: ( )",
                "V - Capstan bump: ( )",
                "V - Film Bump: ( )",
                "V - Video Jitter: ( )",
                "V - Film Stain: ( )",
                "A - Audio Distortion: ( )",
                "V - Audio dip: ( )",
                "A - Audio dip: ( )",
                "V - Last Cut Of Program: ( )",
                "V - End Credits: ( )",
                "V - 20th Century Fox animated logo: ( )",
                "V - Main Title: ( )",
                "V - Start of program: ( )",
                "V - Text Forced Narritive: ( )",
                "V - Text Forced Narrative: ( )",
                "V - Text Forced Narrative: ( )",
                "V - Fox Searchlight Pictures Logo: ( )",
                "V - Camera Flare: ( )",
                "V - 20th Century Fox Logo Celebrating 75 Years: ( )",
                "V - Subtitle overlaps Casting Credit: ( )",
                "V - Subtitle overlaps credit: ( )",
                "V - Minor Aliasing during Paramount Logo: ( )",
                "V - Digital Hit: ( )",
                "V - Scene Missing. Could be Edited for Creative Choice: ( )",
                "A - Noticeable ADR: ( )",
                "V - Pixel above mouth is flickering: ( )",
                "A - Hit Across Face: ( )",
                "V - New Life Foundation Information: ( )",
                "V - End of program: ( )",
                "V - Horrizontal Streak: ( )",
                "V - Hit Across Face: ( )",
                "V - Slate: ( )",
                "A - Hiss: ( )",
                "V - First Cut Of Program: ( )",
                "A - Audio Crackle: ( )",
                "V - Moire: ( )",
                "A - Audio Distortion: ( )",
                "V - TBC Hit: ( )",
                "A - Audio Mutes during TBC Hit: ( )",
                "A - Slight Hiss: ( )",
                "V - Flash / off set: ( )",
                "A - MIC bump: ( )",
                "A - Audio levels dip / Very low: ( )",
                "A - Dip in Audio Levels: ( )",
                "A - Spelling Error on Slate: ( )",
                "V - Spelling Error on Slate: ( )",
                "V - Tracking: ( )",
                "A - Audio Sync Verification: ( )",
                "V - Picture Ringing: ( )",
                "V - Dubcard: ( )",
                "A - Dialogue clipping: ( )",
                "A - Audio Bump: ( )",
                "V - Video Jitter: ( )",
                "V - Dropped frame: ( )",
                "V - Chroma shift: ( )",
                "V - Fox Searchlight Pictures Logo: ( )",
                "V - Jitter: ( )"
            )
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
                    self.get_timecode_textbox('timecode-{0}'.format(iterator), 150, line.get_value('timecode'))
                )
                table.add_cell(
                    self.get_text_input_wdg('field-{0}'.format(iterator), 30, line.get_value('field'))
                )
                table.add_cell(
                    self.get_text_input_wdg('description-{0}'.format(iterator), 150, line.get_value('description'))
                )
                table.add_cell(
                    self.get_select_wdg('type-code-{0}'.format(iterator), type_code_options,
                                        line.get_value('type_code'))
                )
                table.add_cell(
                    self.get_select_wdg('scale-{0}'.format(iterator), scale_select_options, line.get_value('scale'))
                )
                table.add_cell(
                    self.get_text_input_wdg('sector-or-channel-{0}'.format(iterator), 150,
                                            line.get_value('sector_or_channel'))
                )
                table.add_cell(
                    self.get_select_wdg('in-source-{0}'.format(iterator), in_source_options,
                                        line.get_value('in_source'))
                )
                table.add_cell(
                    self.get_remove_row_button(line.get_code())
                )
        else:
            table.add_cell("No PreQual Evaluation lines exist yet. Add one?")

        table.add_cell(self.get_add_row_button())

        main_div = DivWdg()
        main_div.set_id('prequal_eval_lines_div')
        main_div.add_style('margin', '10px')
        main_div.add(table)

        return main_div
