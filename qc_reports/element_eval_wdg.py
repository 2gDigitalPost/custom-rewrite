from qc_reports.audio_configuration_lines_wdg import AudioLinesTableWdg
from qc_reports.element_eval_lines_wdg import ElementEvalLinesWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import CalendarInputWdg, ButtonNewWdg

from pyasm.search import Search
from pyasm.web import Table, DivWdg, SpanWdg
from pyasm.widget import SelectWdg, TextAreaWdg

from utils import get_attribute_or_none, get_text_input_wdg


class ElementEvalWdg(BaseRefreshWdg):

    def init(self):
        self.element_eval_sobject = self.get_sobject_from_kwargs()

        if self.element_eval_sobject:
            self.name_data = self.element_eval_sobject.get('name') # self.name is already used in the super class
            self.title_data = self.element_eval_sobject.get('title') # self.title is already used in the super class
            self.client_code = self.element_eval_sobject.get('client_code')
            self.status = self.element_eval_sobject.get('status')
            self.date = self.element_eval_sobject.get('date')
            self.operator = self.element_eval_sobject.get('operator')
            self.style_sel = self.element_eval_sobject.get('style') # self.style is already used in the super class
            self.bay = self.element_eval_sobject.get('bay')
            self.machine_code = self.element_eval_sobject.get('machine_code')
            self.format_data = self.element_eval_sobject.get('format') # 'format' is a reserved word in Python
            self.season = self.element_eval_sobject.get('season')
            self.standard = self.element_eval_sobject.get('standard')
            self.episode = self.element_eval_sobject.get('episode')
            self.frame_rate_code = self.element_eval_sobject.get('frame_rate_code')
            self.version = self.element_eval_sobject.get('version')
            self.po_number = self.element_eval_sobject.get('po_number')
            self.file_name = self.element_eval_sobject.get('file_name')
            self.roll_up_blank = self.element_eval_sobject.get('roll_up_blank')
            self.bars_tone = self.element_eval_sobject.get('bars_tone')
            self.black_silence_1 = self.element_eval_sobject.get('black_silence_1')
            self.slate_silence = self.element_eval_sobject.get('slate_silence')
            self.black_silence_2 = self.element_eval_sobject.get('black_silence_2')
            self.start_of_program = self.element_eval_sobject.get('start_of_program')
            self.end_of_program = self.element_eval_sobject.get('end_of_program')
            self.active_video_begins = self.element_eval_sobject.get('active_video_begins')
            self.active_video_ends = self.element_eval_sobject.get('active_video_ends')
            self.horizontal_blanking = self.element_eval_sobject.get('horizontal_blanking')
            self.luminance_peak = self.element_eval_sobject.get('luminance_peak')
            self.chroma_peak = self.element_eval_sobject.get('chroma_peak')
            self.head_logo = self.element_eval_sobject.get('head_logo')
            self.tail_logo = self.element_eval_sobject.get('tail_logo')
            self.total_runtime = self.element_eval_sobject.get('total_runtime')
            self.language_code = self.element_eval_sobject.get('language_code')
            self.tv_feature_trailer = self.element_eval_sobject.get('tv_feature_trailer')
            self.cc_subtitles = self.element_eval_sobject.get('cc_subtitles')
            self.video_aspect_ratio = self.element_eval_sobject.get('video_aspect_ratio')
            self.vitc = self.element_eval_sobject.get('vitc')
            self.textless_tail = self.element_eval_sobject.get('textless_tail')
            self.source_barcode = self.element_eval_sobject.get('source_barcode')
            self.notices = self.element_eval_sobject.get('notices')
            self.element_qc_barcode = self.element_eval_sobject.get('element_qc_barcode')
            self.label = self.element_eval_sobject.get('label')
            self.record_date = self.element_eval_sobject.get('record_date')
            self.general_comments = self.element_eval_sobject.get('general_comments')

    @staticmethod
    def get_save_behavior(sobject_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
function save_audio_eval_lines(element_evaluation_code) {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

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
}

function save_element_eval_lines(element_evaluation_code) {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

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

    server.update_multiple(lines);
}

function get_report_values() {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    // Name of the report
    var name = report_values.name_data;

    // Client row values
    var client_code = report_values.client_select;
    var status = report_values.status_select;

    // Operator row values
    var date = report_values.date;
    var operator = report_values.operator;
    var style = report_values.style_select;
    var bay = report_values.bay_select;
    var machine_code = report_values.machine_select;

    // Title section values
    var title_data = report_values.title_data;
    var format = report_values.format_select;
    var season = report_values.season;
    var standard = report_values.standard_select;
    var episode = report_values.episode;
    var frame_rate_code = report_values.frame_rate_select;
    var version = report_values.version;
    var po_number = report_values.po_number;
    var file_name = report_values.file_name;

    // Program Format values
    var roll_up_blank = report_values.roll_up_blank;
    var bars_tone = report_values.bars_tone;
    var black_silence_1 = report_values.black_silence_1;
    var slate_silence = report_values.slate_silence;
    var black_silence_2 = report_values.black_silence_2;
    var start_of_program = report_values.start_of_program;
    var end_of_program = report_values.end_of_program;

    // Video Measurements values
    var active_video_begins = report_values.active_video_begins;
    var active_video_ends = report_values.active_video_ends;
    var horizontal_blanking = report_values.horizontal_blanking;
    var luminance_peak = report_values.luminance_peak;
    var chroma_peak = report_values.chroma_peak;
    var head_logo = report_values.head_logo;
    var tail_logo = report_values.tail_logo;

    // Element Profile values
    var total_runtime = report_values.total_runtime;
    var language_code = report_values.language_select;
    var tv_feature_trailer = report_values.tv_feature_trailer;
    var cc_subtitles = report_values.cc_subtitles;
    var video_aspect_ratio = report_values.video_aspect_ratio_select;
    var vitc = report_values.vitc;
    var textless_tail = report_values.textless_tail;
    var source_barcode = report_values.source_barcode;
    var notices = report_values.notices;
    var element_qc_barcode = report_values.element_qc_barcode;
    var label = report_values.label;
    var record_date = report_values.record_date;

    // General comments
    var general_comments = report_values.general_comments;

    var qc_report_object = {
        'name': name,
        'client_code': client_code,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine_code': machine_code,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate_code': frame_rate_code,
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
        'language_code': language_code,
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
        'general_comments': general_comments
    };

    return qc_report_object;
}

try {
    var code = '%s';

    save_audio_eval_lines(code);
    save_element_eval_lines(code);

    var server = TacticServerStub.get();
    var search_key = server.build_search_key('twog/element_evaluation', code, 'twog');

    var qc_report_object = get_report_values();

    spt.app_busy.show("Saving...");
    server.update(search_key, qc_report_object);
    spt.api.load_panel(bvr.src_el.getParent('#element_eval_panel'), 'qc_reports.ElementEvalWdg', {'search_key': search_key});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            ''' % sobject_code
        }

        return behavior

    @staticmethod
    def get_save_as_new_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
function get_report_values() {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    // Name of the report
    var name = report_values.name_data;

    // Client row values
    var client_code = report_values.client_select;
    var status = report_values.status_select;

    // Operator row values
    var date = report_values.date;
    var style = report_values.style_select;
    var bay = report_values.bay_select;
    var machine_code = report_values.machine_select;

    // Title section values
    var title_data = report_values.title_data;
    var format = report_values.format_select;
    var season = report_values.season;
    var standard = report_values.standard_select;
    var episode = report_values.episode;
    var frame_rate_code = report_values.frame_rate_select;
    var version = report_values.version;
    var po_number = report_values.po_number;
    var file_name = report_values.file_name;

    // Program Format values
    var roll_up_blank = report_values.roll_up_blank;
    var bars_tone = report_values.bars_tone;
    var black_silence_1 = report_values.black_silence_1;
    var slate_silence = report_values.slate_silence;
    var black_silence_2 = report_values.black_silence_2;
    var start_of_program = report_values.start_of_program;
    var end_of_program = report_values.end_of_program;

    // Video Measurements values
    var active_video_begins = report_values.active_video_begins;
    var active_video_ends = report_values.active_video_ends;
    var horizontal_blanking = report_values.horizontal_blanking;
    var luminance_peak = report_values.luminance_peak;
    var chroma_peak = report_values.chroma_peak;
    var head_logo = report_values.head_logo;
    var tail_logo = report_values.tail_logo;

    // Element Profile values
    var total_runtime = report_values.total_runtime;
    var language_code = report_values.language_select;
    var tv_feature_trailer = report_values.tv_feature_trailer;
    var cc_subtitles = report_values.cc_subtitles;
    var video_aspect_ratio = report_values.video_aspect_ratio_select;
    var vitc = report_values.vitc;
    var textless_tail = report_values.textless_tail;
    var source_barcode = report_values.source_barcode;
    var notices = report_values.notices;
    var element_qc_barcode = report_values.element_qc_barcode;
    var label = report_values.label;
    var record_date = report_values.record_date;

    // General comments
    var general_comments = report_values.general_comments;

    var qc_report_object = {
        'name': name,
        'client_code': client_code,
        'status': status,
        'date': new Date().toUTCString(),
        'style': style,
        'bay': bay,
        'machine_code': machine_code,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate_code': frame_rate_code,
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
        'language_code': language_code,
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
        'general_comments': general_comments
    };

    return qc_report_object;
}

try {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    var server = TacticServerStub.get();

    spt.app_busy.show("Saving a new Report...");

    var qc_report_object = get_report_values();

    // Save the new Element Evaluation, and get the code that it saved as
    var inserted_element_evaluation = server.insert('twog/element_evaluation', qc_report_object);
    var code = inserted_element_evaluation['code'];

    // Using the code gained from the new report, save the audio and element eval lines
    var number_of_lines = 0;

    while (true) {
        if (report_values.hasOwnProperty("channel-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

    for (var i = 0; i < number_of_lines; i++) {
        var channel = report_values["channel-" + String(i)];
        var content = report_values["content-" + String(i)];
        var tone = report_values["tone-" + String(i)];
        var peak = report_values["peak-" + String(i)];

        // Insert the line
        // TODO: Insert all lines at once rather than one at a time
        server.insert('twog/audio_evaluation_line', {'element_evaluation_code': code,
                                                     'channel': channel,
                                                     'content': content,
                                                     'tone': tone,
                                                     'peak': peak});
    }

    number_of_lines = 0;

    while (true) {
        if (report_values.hasOwnProperty("timecode-in-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

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
        line_data['element_evaluation_code'] = code;

        // All copied lines are not checked by default, to force operators to check off the lines on new reports
        line_data['checked'] = false;

        server.insert('twog/element_evaluation_line', line_data);
    }

    // Finally, get the search key for the new report, and use it to reload the page
    var search_key = server.build_search_key('twog/element_evaluation', code, 'twog');

    spt.api.load_panel(bvr.src_el.getParent('#element_eval_panel'), 'qc_reports.ElementEvalWdg', {'search_key': search_key});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            '''
        }

        return behavior

    @staticmethod
    def get_save_as_new_version_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
function get_report_values() {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    // Regular expression to find if the name has _V{digit} at the end of the name. If so, increment the version by one,
    // if not, add _V2 to the name when saving the new report
    var regex = /_V\d$/gm;

    // Name of the report
    var name = report_values.name_data;

    var match = regex.exec(name);

    if (match) {
        var version_digit = Number(name[name.length - 1]) + 1;
        name = name.slice(0, -1) + String(version_digit);
    }
    else {
        name = name + "_V2";
    }

    // Client row values
    var client_code = report_values.client_select;
    var status = report_values.status_select;

    // Operator row values
    var style = report_values.style_select;
    var bay = report_values.bay_select;
    var machine_code = report_values.machine_select;

    // Title section values
    var title_data = report_values.title_data;
    var format = report_values.format_select;
    var season = report_values.season;
    var standard = report_values.standard_select;
    var episode = report_values.episode;
    var frame_rate_code = report_values.frame_rate_select;
    var version = report_values.version;
    var po_number = report_values.po_number;
    var file_name = report_values.file_name;

    // Program Format values
    var roll_up_blank = report_values.roll_up_blank;
    var bars_tone = report_values.bars_tone;
    var black_silence_1 = report_values.black_silence_1;
    var slate_silence = report_values.slate_silence;
    var black_silence_2 = report_values.black_silence_2;
    var start_of_program = report_values.start_of_program;
    var end_of_program = report_values.end_of_program;

    // Video Measurements values
    var active_video_begins = report_values.active_video_begins;
    var active_video_ends = report_values.active_video_ends;
    var horizontal_blanking = report_values.horizontal_blanking;
    var luminance_peak = report_values.luminance_peak;
    var chroma_peak = report_values.chroma_peak;
    var head_logo = report_values.head_logo;
    var tail_logo = report_values.tail_logo;

    // Element Profile values
    var total_runtime = report_values.total_runtime;
    var language_code = report_values.language_select;
    var tv_feature_trailer = report_values.tv_feature_trailer;
    var cc_subtitles = report_values.cc_subtitles;
    var video_aspect_ratio = report_values.video_aspect_ratio_select;
    var vitc = report_values.vitc;
    var textless_tail = report_values.textless_tail;
    var source_barcode = report_values.source_barcode;
    var notices = report_values.notices;
    var element_qc_barcode = report_values.element_qc_barcode;
    var label = report_values.label;
    var record_date = report_values.record_date;

    // General comments
    var general_comments = report_values.general_comments;

    var qc_report_object = {
        'name': name,
        'client_code': client_code,
        'status': status,
        'date': new Date().toUTCString(),
        'style': style,
        'bay': bay,
        'machine_code': machine_code,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate_code': frame_rate_code,
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
        'language_code': language_code,
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
        'general_comments': general_comments
    };

    return qc_report_object;
}

try {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#element_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    var server = TacticServerStub.get();

    spt.app_busy.show("Saving a new Report...");

    var qc_report_object = get_report_values();

    // Save the new Element Evaluation, and get the code that it saved as
    var inserted_element_evaluation = server.insert('twog/element_evaluation', qc_report_object);
    var code = inserted_element_evaluation['code'];

    // Using the code gained from the new report, save the audio and element eval lines
    var number_of_lines = 0;

    while (true) {
        if (report_values.hasOwnProperty("channel-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

    for (var i = 0; i < number_of_lines; i++) {
        var channel = report_values["channel-" + String(i)];
        var content = report_values["content-" + String(i)];
        var tone = report_values["tone-" + String(i)];
        var peak = report_values["peak-" + String(i)];

        // Insert the line
        // TODO: Insert all lines at once rather than one at a time
        server.insert('twog/audio_evaluation_line', {'element_evaluation_code': code,
                                                     'channel': channel,
                                                     'content': content,
                                                     'tone': tone,
                                                     'peak': peak});
    }

    number_of_lines = 0;

    while (true) {
        if (report_values.hasOwnProperty("timecode-in-" + String(number_of_lines))) {
            number_of_lines++;
        }
        else {
            break;
        }
    }

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
        line_data['element_evaluation_code'] = code;

        // All copied lines are checked by default, as opposed to the regular 'save as'
        line_data['checked'] = report_values["checked-" + String(i)];

        server.insert('twog/element_evaluation_line', line_data);
    }

    // Finally, get the search key for the new report, and use it to reload the page
    var search_key = server.build_search_key('twog/element_evaluation', code, 'twog');

    spt.api.load_panel(bvr.src_el.getParent('#element_eval_panel'), 'qc_reports.ElementEvalWdg', {'search_key': search_key});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            '''
        }

        return behavior

    @staticmethod
    def get_export_to_pdf_behavior(sobject_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Return an object containing the element evaluation's values
var top = bvr.src_el.getParent("#element_eval_panel");
var report_values = spt.api.get_input_values(top, null, false);

var server = TacticServerStub.get();

var code = '%s';
var search_key = server.build_search_key('twog/element_evaluation', code, 'twog');

server.execute_cmd('qc_reports.ExportElementEvalCommand', {'report_search_key': search_key});

var report_name = report_values.name_data;
var file_path = "/assets/element_evaluations/" + report_name + ".pdf";

window.open(file_path);
            ''' % sobject_code
        }

        return behavior

    def get_name_section(self):
        section_div = DivWdg()

        name_wdg = get_text_input_wdg('name_data', get_attribute_or_none(self, 'name_data'), 500)

        section_div.add('Name: ')
        section_div.add(name_wdg)

        return section_div

    def get_client_section(self):
        section_div = DivWdg()

        client_span = SpanWdg()
        client_span.add_style('display', 'inline-block')
        client_span.add('Client: ')
        client_span.add(self.get_client_select())

        status_span = SpanWdg()
        status_span.add_style('display', 'inline-block')
        status_span.add('Status: ')
        status_span.add(self.get_status_select())

        section_div.add(client_span)
        section_div.add(status_span)

        return section_div

    def get_client_select(self):
        client_sel = SelectWdg('client_select')
        client_sel.set_id('client_code')
        client_sel.add_style('width', '135px')
        client_sel.add_empty_option()

        client_search = Search('twog/client')
        clients = client_search.get_sobjects()

        for client in clients:
            client_sel.append_option(client.get_value('name'), client.get_code())

        if hasattr(self, 'client_code'):
            client_sel.set_value(self.client_code)

        return client_sel

    def get_status_select(self):
        status_sel = SelectWdg('status_select')
        status_sel.set_id('status')
        status_sel.add_style('width', '135px')
        status_sel.add_empty_option()

        statuses = ('Approved', 'In Progress', 'Rejected')

        for status in statuses:
            status_sel.append_option(status, status)

        if hasattr(self, 'status'):
            status_sel.set_value(self.status)

        return status_sel

    def get_operator_section(self):
        operator_table = Table()
        operator_table.add_attr('class', 'operator_table')
        operator_table.add_row()
        operator_table.add_header('DATE')
        operator_table.add_header('OPERATOR')
        operator_table.add_header('STYLE')
        operator_table.add_header('BAY')
        operator_table.add_header('MACHINE')
        operator_table.add_row()

        operator_table.add_cell(self.get_date_calendar_wdg())

        operator_table.add_cell(get_text_input_wdg('operator', get_attribute_or_none(self, 'operator')))

        operator_table.add_cell(self.get_style_select())
        operator_table.add_cell(self.get_bay_select())
        operator_table.add_cell(self.get_machine_select())

        return operator_table

    def get_date_calendar_wdg(self):
        date_calendar_wdg = CalendarInputWdg("date")
        date_calendar_wdg.set_option('show_activator', 'true')
        date_calendar_wdg.set_option('show_time', 'false')
        date_calendar_wdg.set_option('width', '300px')
        date_calendar_wdg.set_option('id', 'date')
        date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

        try:
            date_calendar_wdg.set_value(self.date)
        except AttributeError:
            pass

        return date_calendar_wdg

    def get_style_select(self):
        style_sel = SelectWdg('style_select')
        style_sel.set_id('style')
        style_sel.add_style('width: 135px;')
        style_sel.add_empty_option()

        for style in ('Technical', 'Spot QC', 'Mastering'):
            style_sel.append_option(style, style)

        try:
            style_sel.set_value(self.style_sel)
        except AttributeError:
            pass

        return style_sel

    def get_bay_select(self):
        bay_sel = SelectWdg('bay_select')
        bay_sel.set_id('bay')
        bay_sel.add_style('width', '135px')
        bay_sel.add_empty_option()

        for i in range(1, 13):
            bay_sel.append_option('Bay %s' % i, 'Bay %s' % i)

        try:
            bay_sel.set_value(self.bay)
        except AttributeError:
            pass

        return bay_sel

    def get_machine_select(self):
        machine_sel = SelectWdg('machine_select')
        machine_sel.set_id('machine_code')
        machine_sel.add_style('width', '135px')
        machine_sel.add_empty_option()

        machine_search = Search('twog/machine')
        machines = machine_search.get_sobjects()

        for machine in machines:
            machine_sel.append_option(machine.get_value('name'), machine.get_code())

        try:
            machine_sel.set_value(self.machine_code)
        except AttributeError:
            pass

        return machine_sel

    def get_title_section(self):
        section_div = DivWdg()

        section_div.add(self.get_input_widget_with_label('Title: ', 'title_data', 400))
        section_div.add(self.get_format_section())

        return section_div

    def get_input_widget_with_label(self, label, id, width):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add(label)

        section_span.add(get_text_input_wdg(id, get_attribute_or_none(self, id), width))

        return section_span

    def get_format_section(self):
        section_span = SpanWdg()

        section_span.add('Format: ')
        section_span.add(self.get_format_select_wdg())

        return section_span

    def get_format_select_wdg(self):
        format_sel = SelectWdg('format_select')
        format_sel.set_id('format')
        format_sel.add_style('width', '153px')
        format_sel.add_style('display', 'inline-block')
        format_sel.add_empty_option()

        for file_format in ('Electronic/File', 'File - ProRes', 'File - MXF', 'File - MPEG', 'File - WAV', 'DBC', 'D5',
                            'HDCAM SR', 'NTSC', 'PAL'):
            format_sel.append_option(file_format, file_format)

        try:
            format_sel.set_value(self.format_data)
        except AttributeError:
            pass

        return format_sel

    def get_season_section(self):
        section_div = DivWdg()

        section_div.add(self.get_input_widget_with_label('Season: ', 'season', 400))
        section_div.add(self.get_standard_section())

        return section_div

    def get_standard_section(self):
        section_span = SpanWdg()

        section_span.add('Standard: ')

        standard_select = SelectWdg('standard_select')
        standard_select.set_id('standard')
        standard_select.add_style('width', '153px')
        standard_select.add_style('display', 'inline-block')
        standard_select.add_empty_option()

        for standard in ('625', '525', '720', '1080 (4:4:4)', '1080', 'PAL', 'NTSC', '3840', '4160'):
            standard_select.append_option(standard, standard)

        try:
            standard_select.set_value(self.standard)
        except AttributeError:
            pass

        section_span.add(standard_select)

        return section_span

    def get_episode_section(self):
        section_div = DivWdg()

        section_div.add(self.get_input_widget_with_label('Episode: ', 'episode', 400))
        section_div.add(self.get_frame_rate_section())

        return section_div

    def get_frame_rate_section(self):
        section_span = SpanWdg()

        section_span.add('Frame Rate: ')

        frame_rate_select = SelectWdg('frame_rate_select')
        frame_rate_select.set_id('frame_rate_code')
        frame_rate_select.add_style('width', '153px')
        frame_rate_select.add_style('display', 'inline-block')
        frame_rate_select.add_empty_option()

        frame_rate_search = Search('twog/frame_rate')
        frame_rates = frame_rate_search.get_sobjects()

        for frame_rate in frame_rates:
            frame_rate_select.append_option(frame_rate.get_value('name'), frame_rate.get_code())

        try:
            frame_rate_select.set_value(self.frame_rate_code)
        except AttributeError:
            pass

        section_span.add(frame_rate_select)

        return section_span

    def get_language_select(self):
        language_select = SelectWdg('language_select')
        language_select.set_id('language_code')
        language_select.add_style('width', '300px')
        language_select.add_style('display', 'inline-block')
        language_select.add_empty_option()

        language_search = Search('twog/language')
        languages = language_search.get_sobjects()

        languages = sorted(languages, key=lambda x: x.get_value('name'))

        for language in languages:
            language_select.append_option(language.get_value('name'), language.get_code())

        if hasattr(self, 'language_code'):
            language_select.set_value(self.language_code)

        return language_select

    def get_version_section(self):
        section_div = DivWdg()

        section_div.add(self.get_input_widget_with_label('Version: ', 'version', 400))
        section_div.add(self.get_input_widget_with_label('PO #: ', 'po_number', 100))

        return section_div

    def get_file_name_section(self):
        section_div = DivWdg()

        section_div.add(self.get_input_widget_with_label('File Name: ', 'file_name', 600))

        return section_div

    def get_program_format_table(self):
        program_format_table = Table()
        program_format_table.add_style('float', 'left')

        program_format_table.add_row()
        program_format_table.add_header('Program Format')
        program_format_table.add_header()

        text_input_name_id_pairs = [
            ('Roll-up (blank)', 'roll_up_blank'),
            ('Bars/Tone', 'bars_tone'),
            ('Black/Silence', 'black_silence_1'),
            ('Slate/Silence', 'slate_silence'),
            ('Black/Silence', 'black_silence_2'),
            ('Start of Program', 'start_of_program'),
            ('End of Program', 'end_of_program')
        ]

        self.setup_table_rows_with_input_boxes(program_format_table, text_input_name_id_pairs, timecode=True)

        return program_format_table

    def setup_table_rows_with_input_boxes(self, table, text_input_name_id_pairs, timecode=False):
        for text_input_name_id_pair in text_input_name_id_pairs:
            table.add_row()

            text_input_name = str(text_input_name_id_pair[0])
            text_input_id = str(text_input_name_id_pair[1])

            table.add_cell(text_input_name)

            table.add_cell(get_text_input_wdg(text_input_id, get_attribute_or_none(self, text_input_id), 300,
                                              timecode=timecode))

    def get_video_measurements_table(self):
        video_measurements_table = Table()

        video_measurements_table.add_row()
        video_measurements_table.add_header('Video Measurements')

        text_input_name_id_pairs = [
            ('Active Video Begins', 'active_video_begins'),
            ('Active Video Ends', 'active_video_ends'),
            ('Horizontal Blanking', 'horizontal_blanking'),
            ('Luminance Peak', 'luminance_peak'),
            ('Chroma Peak', 'chroma_peak'),
            ('Head Logo', 'head_logo'),
            ('Tail Logo', 'tail_logo')
        ]

        self.setup_table_rows_with_input_boxes(video_measurements_table, text_input_name_id_pairs)

        return video_measurements_table

    def get_element_profile_table(self):
        element_profile_table = Table()

        element_profile_table.add_row()
        element_profile_table.add_header('Element Profile')

        element_profile_table.add_row()
        element_profile_table.add_cell('Total Runtime')
        element_profile_table.add_cell(get_text_input_wdg('total_runtime',
                                                          get_attribute_or_none(self, 'total_runtime'), 300))
        element_profile_table.add_cell('Language')
        element_profile_table.add_cell(self.get_language_select())

        element_profile_table.add_row()
        element_profile_table.add_cell('TV/Feature/Trailer')
        element_profile_table.add_cell(get_text_input_wdg('tv_feature_trailer',
                                                          get_attribute_or_none(self, 'tv_feature_trailer'), 300))
        element_profile_table.add_cell('(CC)/Subtitles')
        element_profile_table.add_cell(get_text_input_wdg('cc_subtitles',
                                                          get_attribute_or_none(self, 'cc_subtitles'), 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Video Aspect Ratio')
        element_profile_table.add_cell(self.get_video_aspect_ratio_select_wdg())
        element_profile_table.add_cell('VITC')
        element_profile_table.add_cell(get_text_input_wdg('vitc', get_attribute_or_none(self, 'vitc'), 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Textless @ Tail')
        element_profile_table.add_cell(get_text_input_wdg('textless_tail',
                                                          get_attribute_or_none(self, 'textless_tail'), 300))
        element_profile_table.add_cell('Source Barcode')
        element_profile_table.add_cell(get_text_input_wdg('source_barcode',
                                                          get_attribute_or_none(self, 'source_barcode'), 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Notices')
        element_profile_table.add_cell(get_text_input_wdg('notices',
                                                          get_attribute_or_none(self, 'notices'), 300))
        element_profile_table.add_cell('Element QC Barcode')
        element_profile_table.add_cell(get_text_input_wdg('element_qc_barcode',
                                                          get_attribute_or_none(self, 'element_qc_barcode'), 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Label')
        element_profile_table.add_cell(self.get_label_select_wdg())
        element_profile_table.add_cell('Record Date')
        element_profile_table.add_cell(self.get_record_date_calendar_wdg())

        return element_profile_table

    def get_video_aspect_ratio_select_wdg(self):
        video_aspect_ratio_sel = SelectWdg('video_aspect_ratio_select')
        video_aspect_ratio_sel.set_id('video_aspect_ratio')
        video_aspect_ratio_sel.add_style('width', '300px')
        video_aspect_ratio_sel.add_style('display', 'inline-block')
        video_aspect_ratio_sel.add_empty_option()

        video_aspect_ratios_search = Search('twog/aspect_ratio')
        video_aspect_ratios = video_aspect_ratios_search.get_sobjects()

        for video_aspect_ratio in video_aspect_ratios:
            video_aspect_ratio_sel.append_option(video_aspect_ratio.get('name'), video_aspect_ratio.get('name'))

        if hasattr(self, 'video_aspect_ratio'):
            video_aspect_ratio_sel.set_value(self.video_aspect_ratio)

        return video_aspect_ratio_sel

    def get_label_select_wdg(self):
        label_select_wdg = SelectWdg('label')
        label_select_wdg.set_id('label')
        label_select_wdg.add_style('width', '300px')
        label_select_wdg.add_style('display', 'inline-block')
        label_select_wdg.add_empty_option()

        label_options = ('Good', 'Fair', 'Poor')

        for label in label_options:
            label_select_wdg.append_option(label, label)

        if hasattr(self, 'label'):
            # Double check that 'label' is within the given options (sometimes it isn't for some reason which causes
            # an error)
            if self.label in label_options:
                label_select_wdg.set_value(self.label)

        return label_select_wdg

    def get_record_date_calendar_wdg(self):
        record_date_calendar_wdg = CalendarInputWdg("record_date")
        record_date_calendar_wdg.set_option('show_activator', 'true')
        record_date_calendar_wdg.set_option('show_time', 'false')
        record_date_calendar_wdg.set_option('width', '300px')
        record_date_calendar_wdg.set_option('id', 'record_date')
        record_date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

        if hasattr(self, 'record_date'):
            record_date_calendar_wdg.set_value(self.record_date)

        return record_date_calendar_wdg

    def get_general_comments_section(self):
        general_comments_div = DivWdg()
        general_comments_div.add_style('margin', '10px')
        general_comments_wdg = TextAreaWdg()
        general_comments_wdg.set_id('general_comments')
        general_comments_wdg.set_name('general_comments')

        if hasattr(self, 'general_comments'):
            general_comments_wdg.set_value(self.general_comments)

        general_comments_text_div = DivWdg('General Comments')
        general_comments_text_div.add_style('font-weight', 'bold')
        general_comments_div.add(general_comments_text_div)
        general_comments_div.add(general_comments_wdg)

        return general_comments_div

    def get_save_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_button = ButtonNewWdg(title='Save', icon='SAVE')
        save_button.add_class('save_button')
        save_button.add_behavior(self.get_save_behavior(self.element_eval_sobject.get_code()))

        section_span.add(save_button)

        return section_span

    def get_save_as_new_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_as_new_button = ButtonNewWdg(title='Save As', icon='NEW')
        save_as_new_button.add_class('save_as_new_button')
        save_as_new_button.add_behavior(self.get_save_as_new_behavior())

        section_span.add(save_as_new_button)

        return section_span

    def get_save_as_new_version_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_as_new_version_button = ButtonNewWdg(title='Save As New Version', icon='INSERT')
        save_as_new_version_button.add_class('save_as_new_version_button')
        save_as_new_version_button.add_behavior(self.get_save_as_new_version_behavior())

        section_span.add(save_as_new_version_button)

        return section_span

    def get_export_to_pdf_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        export_to_pdf_button = ButtonNewWdg(title='Export to PDF', icon='ARROW_DOWN')
        export_to_pdf_button.add_class('export_to_pdf_button')
        export_to_pdf_button.add_behavior(self.get_export_to_pdf_behavior(self.element_eval_sobject.get_code()))

        section_span.add(export_to_pdf_button)

        return section_span

    def add_button_row_to_main_wdg(self, main_wdg):
        main_wdg.add(self.get_save_button())
        main_wdg.add(self.get_export_to_pdf_button())
        main_wdg.add(self.get_save_as_new_button())
        main_wdg.add(self.get_save_as_new_version_button())

    def get_display(self):
        # This will be the main <div> that everything else goes into
        main_wdg = DivWdg()
        main_wdg.set_id('element_eval_panel')

        self.add_button_row_to_main_wdg(main_wdg)

        main_wdg.add(self.get_name_section())

        main_wdg.add(self.get_client_section())

        main_wdg.add(self.get_operator_section())
        main_wdg.add(self.get_title_section())
        main_wdg.add(self.get_season_section())
        main_wdg.add(self.get_episode_section())
        main_wdg.add(self.get_version_section())
        main_wdg.add(self.get_file_name_section())

        main_wdg.add(self.get_program_format_table())
        main_wdg.add(self.get_video_measurements_table())
        main_wdg.add(self.get_element_profile_table())

        if hasattr(self, 'element_eval_sobject') and self.element_eval_sobject:
            main_wdg.add(AudioLinesTableWdg(element_evaluation_code=self.element_eval_sobject.get_code()))

        main_wdg.add(self.get_general_comments_section())

        main_wdg.add(ElementEvalLinesWdg(element_evaluation_code=self.element_eval_sobject.get_code()))

        self.add_button_row_to_main_wdg(main_wdg)

        return main_wdg
