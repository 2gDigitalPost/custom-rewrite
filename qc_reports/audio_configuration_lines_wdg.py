from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseTableElementWdg

from pyasm.prod.biz import ProdSetting
from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import SelectWdg


def get_add_audio_configuration_line_behavior(number_of_lines=1):
    """
    :param number_of_lines: Number of lines to add (or subtract if negative)
    :return: Javascript behavior
    """
    # TODO: Better docstring here

    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    // Client row values
    var client = document.getElementById("client").value;
    var status = document.getElementById("status").value;

    // Operator row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine = document.getElementById("machine").value;

    // Title section values
    var title_data = document.getElementsByName("title_data")[0].value;
    var format = document.getElementById("format").value;
    var season = document.getElementsByName("season")[0].value;
    var standard = document.getElementById("standard").value;
    var episode = document.getElementsByName("episode")[0].value;
    var frame_rate = document.getElementById("frame_rate").value;
    var version = document.getElementsByName("version")[0].value;
    var po_number = document.getElementsByName("po_number")[0].value;
    var file_name = document.getElementsByName("file_name")[0].value;

    // Program Format values
    var roll_up_blank = document.getElementsByName("roll_up_blank")[0].value;
    var bars_tone = document.getElementsByName("bars_tone")[0].value;
    var black_silence_1 = document.getElementsByName("black_silence_1")[0].value;
    var slate_silence = document.getElementsByName("slate_silence")[0].value;
    var black_silence_2 = document.getElementsByName("black_silence_2")[0].value;
    var start_of_program = document.getElementsByName("start_of_program")[0].value;
    var end_of_program = document.getElementsByName("end_of_program")[0].value;

    // Video Measurements values
    var active_video_begins = document.getElementsByName("active_video_begins")[0].value;
    var active_video_ends = document.getElementsByName("active_video_ends")[0].value;
    var horizontal_blanking = document.getElementsByName("horizontal_blanking")[0].value;
    var luminance_peak = document.getElementsByName("luminance_peak")[0].value;
    var chroma_peak = document.getElementsByName("chroma_peak")[0].value;
    var head_logo = document.getElementsByName("head_logo")[0].value;
    var tail_logo = document.getElementsByName("tail_logo")[0].value;

    // Element Profile values
    var total_runtime = document.getElementsByName("total_runtime")[0].value;
    var language = document.getElementsByName("language")[0].value;
    var tv_feature_trailer = document.getElementsByName("tv_feature_trailer")[0].value;
    var cc_subtitles = document.getElementsByName("cc_subtitles")[0].value;
    var video_aspect_ratio = document.getElementById("video_aspect_ratio").value;
    var vitc = document.getElementsByName("vitc")[0].value;
    var textless_tail = document.getElementsByName("textless_tail")[0].value;
    var source_barcode = document.getElementsByName("source_barcode")[0].value;
    var notices = document.getElementsByName("notices")[0].value;
    var element_qc_barcode = document.getElementsByName("element_qc_barcode")[0].value;
    var label = document.getElementById("label").value;
    var record_date = document.getElementsByName("record_date")[0].value;

    // General comments
    var general_comments = document.getElementById("general_comments").value;

    // Get the number of lines in the audio configuration table
    var audio_configuration_table = document.getElementById('audio_configuration_table');
    var audio_configuration_table_rows = audio_configuration_table.getElementsByTagName("tr");

    // Two rows always exist for the table headers, so subtract that
    var number_of_audio_configuration_lines = audio_configuration_table_rows.length - 2;

    // Get the number of lines to add (or subtract)
    var number_of_lines_to_add = Number('%s');

    // Finally, get the new number to pass into the kwargs. If the number is less than or equal to 1, set it to 1
    // (don't want to allow less than one row to be displayed)
    var audio_configuration_lines = number_of_audio_configuration_lines + number_of_lines_to_add;

    if (audio_configuration_lines < 1) {
        audio_configuration_lines = 1;
    }

    var audio_configuration_lines_values = {};

    for (var i = 0; i < number_of_audio_configuration_lines; i++) {
        audio_configuration_lines_values['channel-' + String(i)] = document.getElementsByName("channel-" + String(i))[0].value;
        audio_configuration_lines_values['content-' + String(i)] = document.getElementsByName("content-" + String(i))[0].value;
        audio_configuration_lines_values['tone-' + String(i)] = document.getElementsByName("tone-" + String(i))[0].value;
        audio_configuration_lines_values['peak-' + String(i)] = document.getElementsByName("peak-" + String(i))[0].value;
    }

    var qc_report_object = {
        'client': client,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine': machine,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate': frame_rate,
        'version': version,
        'po_number': po_number,
        'file_name': file_name,
        'roll_up_blank': roll_up_blank,
        'bars_tone': bars_tone,
        'black_silence_1': black_silence_1,
        'slate_silence': slate_silence,
        'black_silence_2': black_silence_2,
        'start_of_program': start_of_program,
        'end_of_program': end_of_program,
        'active_video_begins': active_video_begins,
        'active_video_ends': active_video_ends,
        'horizontal_blanking': horizontal_blanking,
        'luminance_peak': luminance_peak,
        'chroma_peak': chroma_peak,
        'head_logo': head_logo,
        'tail_logo': tail_logo,
        'total_runtime': total_runtime,
        'language': language,
        'tv_feature_trailer': tv_feature_trailer,
        'cc_subtitles': cc_subtitles,
        'video_aspect_ratio': video_aspect_ratio,
        'vitc': vitc,
        'textless_tail': textless_tail,
        'source_barcode': source_barcode,
        'notices': notices,
        'element_qc_barcode': element_qc_barcode,
        'label': label,
        'record_date': record_date,
        'audio_configuration_lines': audio_configuration_lines,
        'audio_configuration_lines_values': audio_configuration_lines_values,
        'general_comments': general_comments
    };

    var board_table = document.getElementById('element_eval_panel');

    spt.app_busy.show("Refreshing...");
    spt.api.load_panel(board_table, 'qc_reports.ElementEvalWdg', {'report_data': qc_report_object});
    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
        ''' % number_of_lines
    }

    return behavior


class AudioLinesTableWdg(BaseTableElementWdg):
    def init(self):
        self.element_evaluation_code = self.kwargs.get('element_evaluation_code')

        if self.element_evaluation_code:
            lines_search = Search('twog/element_evaluation_line')
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

    def get_add_subtract_row_buttons(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        add_row_button = ButtonNewWdg(title='Add Row', icon='ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_behavior(self.get_add_audio_configuration_line_behavior())

        section_span.add(add_row_button)

        # Check if we're down to one line on the table. If so, don't show the subtract button
        if hasattr(self, 'audio_configuration_lines') and self.audio_configuration_lines > 1:
            # TODO: Find a proper icon for subtract (not sure if one exists by default)
            subtract_row_button = ButtonNewWdg(title='Remove Row', icon='REMOVE')
            subtract_row_button.add_class('subtract_row_button')
            subtract_row_button.add_behavior(self.get_add_audio_configuration_line_behavior(-1))

            section_span.add(subtract_row_button)

        return section_span

    def get_display(self):
        audio_configuration_table = Table()
        audio_configuration_table.set_id('audio_configuration_table')

        audio_configuration_table.add_row()
        audio_configuration_table.add_header('Audio Configuration')

        audio_configuration_table.add_row()
        audio_configuration_table.add_header('Channel')
        audio_configuration_table.add_header('Content')
        audio_configuration_table.add_header('Tone')
        audio_configuration_table.add_header('Peak')

        for iterator, line in enumerate(self.lines):
            current_row = audio_configuration_table.add_row()

            current_row.add_attr('code', line.get_code())

            audio_configuration_table.add_cell(
                self.get_text_input_wdg_for_audio_config('channel-{0}'.format(iterator), 150, line.get_value('channel')))
            audio_configuration_table.add_cell(
                self.get_text_input_wdg_for_audio_config('content-{0}'.format(iterator), 150, line.get_value('content')))
            audio_configuration_table.add_cell(
                self.get_text_input_wdg_for_audio_config('tone-{0}'.format(iterator), 150, line.get_value('tone')))
            audio_configuration_table.add_cell(
                self.get_text_input_wdg_for_audio_config('peak-{0}'.format(iterator), 150, line.get_value('peak')))

        return audio_configuration_table
