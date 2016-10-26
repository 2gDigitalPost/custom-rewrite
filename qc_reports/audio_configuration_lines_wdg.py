from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseTableElementWdg

from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import HiddenWdg


def get_add_audio_configuration_line_behavior(element_eval_code):
    """
    :return: Javascript behavior
    """
    # TODO: Better docstring here

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
        if (report_values.hasOwnProperty("channel-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

    var lines = {};

    for (var i = 0; i < number_of_lines; i++) {
        var audio_line = {};

        audio_line['channel'] = report_values["channel-" + String(i)];
        audio_line['content'] = report_values["content-" + String(i)];
        audio_line['tone'] = report_values["tone-" + String(i)];
        audio_line['peak'] = report_values["peak-" + String(i)];

        audio_line_code = report_values["audio-line-code-" + String(i)];

        var search_key = server.build_search_key('twog/audio_evaluation_line', audio_line_code, 'twog');

        lines[search_key] = audio_line;
    }

    server.update_multiple(lines);

    // Insert a blank line
    server.insert('twog/audio_evaluation_line', {'element_evaluation_code': element_evaluation_code});

    // Refresh the widget
    spt.app_busy.show("Refreshing...");
    spt.api.load_panel(bvr.src_el.getParent('#audio_config_lines_div'), 'qc_reports.AudioLinesTableWdg', {'element_evaluation_code': element_evaluation_code});
    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
        ''' % element_eval_code
    }

    return behavior


def get_remove_audio_configuration_line_behavior(element_eval_code, line_code):
    """
    :return: Javascript behavior
    """
    # TODO: Better docstring here

    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var server = TacticServerStub.get();
    var element_evaluation_code = '%s';
    var line_code = '%s';

    server.retire_sobject(server.build_search_key('twog/audio_evaluation_line', line_code, 'twog'));

    // Refresh the widget
    spt.api.load_panel(bvr.src_el.getParent('#audio_config_lines_div'), 'qc_reports.AudioLinesTableWdg',
                                            {'element_evaluation_code': element_evaluation_code});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % (element_eval_code, line_code)
    }

    return behavior


class AudioLinesTableWdg(BaseTableElementWdg):
    def init(self):
        self.element_evaluation_code = self.kwargs.get('element_evaluation_code')

        if self.element_evaluation_code:
            lines_search = Search('twog/audio_evaluation_line')
            lines_search.add_filter('element_evaluation_code', self.element_evaluation_code)
            self.lines = lines_search.get_sobjects()
        else:
            self.lines = []

    def get_text_input_wdg_for_audio_config(self, name, width=200, line_data=None):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if line_data:
            textbox_wdg.set_value(line_data)

        return textbox_wdg

    def get_add_row_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        add_row_button = ButtonNewWdg(title='Add Row', icon='ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_behavior(get_add_audio_configuration_line_behavior(self.element_evaluation_code))

        section_span.add(add_row_button)

        return section_span

    def get_remove_row_button(self, line_code):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        remove_row_button = ButtonNewWdg(title='Remove Row', icon='DELETE')
        remove_row_button.add_class('remove_row_button')
        remove_row_button.add_behavior(get_remove_audio_configuration_line_behavior(self.element_evaluation_code,
                                                                                    line_code))

        section_span.add(remove_row_button)

        return section_span

    def get_display(self):
        audio_configuration_table = Table()
        audio_configuration_table.set_id('audio_configuration_table')
        audio_configuration_table.add_style('margin', '10px')

        if self.lines:
            audio_configuration_table.add_row()
            audio_configuration_table.add_header('Audio Configuration')

            audio_configuration_table.add_row()
            audio_configuration_table.add_header('Channel')
            audio_configuration_table.add_header('Content')
            audio_configuration_table.add_header('Tone')
            audio_configuration_table.add_header('Peak')

            for iterator, line in enumerate(self.lines):
                current_row = audio_configuration_table.add_row()

                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('channel-{0}'.format(iterator), 150, line.get_value('channel'))
                )
                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('content-{0}'.format(iterator), 150, line.get_value('content'))
                )
                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('tone-{0}'.format(iterator), 150, line.get_value('tone'))
                )
                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('peak-{0}'.format(iterator), 150, line.get_value('peak'))
                )
                audio_configuration_table.add_cell(
                    HiddenWdg('audio-line-code-{0}'.format(iterator), line.get_code())
                )
                audio_configuration_table.add_cell(
                    self.get_remove_row_button(line.get_code())
                )
        else:
            audio_configuration_table.add("No Audio Configuration lines exist yet. Add one?")

        audio_configuration_table.add(self.get_add_row_button())

        main_div = DivWdg()
        main_div.set_id('audio_config_lines_div')
        main_div.add_style('margin', '10px')
        main_div.add(audio_configuration_table)

        return main_div
