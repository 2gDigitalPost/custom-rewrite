from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg, CalendarInputWdg

from pyasm.search import Search
from pyasm.web import Table, DivWdg, SpanWdg
from pyasm.widget import SelectWdg, TextAreaWdg

import json


class MetaDataReportWdg(BaseRefreshWdg):
    def init(self):
        self.metadata_report_sobject = self.get_sobject_from_kwargs()

        if self.metadata_report_sobject:
            self.report_data = self.parse_report_data_json(self.metadata_report_sobject.get_value('report_data'))

    def parse_report_data_json(self, report_data):
        report_data_dictionary = json.loads(report_data)

        video_configuration = report_data_dictionary.get('video_configuration')
        audio_configuration = report_data_dictionary.get('audio_configuration')
        assets = report_data_dictionary.get('assets')
        chapter_thumbnails = report_data_dictionary.get('chapter_thumbnails')

        if video_configuration:
            data_points = ('encoding_log_shows_no_errors', 'correct_video_codec_used',
                           'frame_rate_same_as_native_source', 'hd_resolution', 'field_dominance_set_to_none',
                           'tagged_as_progressive', 'clap_tag_removed', 'pasp_correct', 'gamma_tag_removed',
                           'video_asset_does_not_contain', 'video_proper_aspect_ratio', 'websites_not_listed',
                           'cropping_values_correct')

            for data_point in data_points:
                data = video_configuration.get(data_point)

                if data:
                    feature_data = data.get('feature')
                    preview_data = data.get('preview')

                    setattr(self, data_point + '_feature', feature_data)
                    setattr(self, data_point + '_preview', preview_data)

            data_points = ('trailer_no_promotional_bumpers', 'trailer_same_aspect_ratio', 'trailer_general_audience',
                           'file_starts_with_black', 'program_starts', 'program_ends_black_frame_feature',
                           'file_starts_fade_up_down', 'program_ends_black_frame_preview', 'program_ends_fade_down')

            for data_point in data_points:
                data = video_configuration.get(data_point)

                if data:
                    setattr(self, data_point, data)

        if audio_configuration:
            data_points = (
                'feature_audio_config_language_1',
                'feature_audio_config_language_2',
                'feature_audio_config_language_3',
                'feature_audio_config_language_4',
                'feature_audio_config_language_5',
                'feature_audio_config_language_6',
                'feature_audio_config_language_7',
                'feature_audio_config_language_8',
                'feature_audio_config_type_1',
                'feature_audio_config_type_2',
                'feature_audio_config_type_3',
                'feature_audio_config_type_4',
                'feature_audio_config_type_5',
                'feature_audio_config_type_6',
                'feature_audio_config_type_7',
                'feature_audio_config_type_8',
                'audio_bundle_language_1',
                'audio_bundle_language_2',
                'audio_bundle_language_3',
                'audio_bundle_language_4',
                'audio_bundle_language_5',
                'audio_bundle_language_6',
                'audio_bundle_language_7',
                'audio_bundle_language_8',
                'audio_bundle_type_1',
                'audio_bundle_type_2',
                'audio_bundle_type_3',
                'audio_bundle_type_4',
                'audio_bundle_type_5',
                'audio_bundle_type_6',
                'audio_bundle_type_7',
                'audio_bundle_type_8',
                'preview_trailer_audio_config_language_1',
                'preview_trailer_audio_config_language_2',
                'preview_trailer_audio_config_language_3',
                'preview_trailer_audio_config_language_4',
                'preview_trailer_audio_config_language_5',
                'preview_trailer_audio_config_language_6',
                'preview_trailer_audio_config_language_7',
                'preview_trailer_audio_config_language_8',
                'preview_trailer_audio_config_type_1',
                'preview_trailer_audio_config_type_2',
                'preview_trailer_audio_config_type_3',
                'preview_trailer_audio_config_type_4',
                'preview_trailer_audio_config_type_5',
                'preview_trailer_audio_config_type_6',
                'preview_trailer_audio_config_type_7',
                'preview_trailer_audio_config_type_8'
            )

            for data_point in data_points:
                data = audio_configuration.get(data_point)

                if data:
                    setattr(self, data_point, data)

            data_points = ('audio_configuration_verified', 'audio_in_sync_with_video', 'audio_tagged_correctly',
                           'no_audio_cut_off', 'trt_audio_equals_trt_video', 'correct_language_present')

            for data_point in data_points:
                data = audio_configuration.get(data_point)

                if data:
                    feature_data = data.get('feature')
                    audio_data = data.get('audio')
                    preview_data = data.get('preview')

                    setattr(self, data_point + '_feature', feature_data)
                    setattr(self, data_point + '_audio', audio_data)
                    setattr(self, data_point + '_preview', preview_data)

        return report_data_dictionary

    @staticmethod
    def get_save_behavior(code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
function get_feature_preview_values(report_values, key) {
    var values = {};

    var feature_key = key + "_feature";
    var preview_key = key + "_preview";

    if (feature_key in report_values) {
        values["feature"] = report_values[feature_key];
    }

    if (preview_key in report_values) {
        values["preview"] = report_values[preview_key];
    }

    return values;
}

function get_feature_audio_preview_values(report_values, key) {
    var values = {};

    var feature_key = key + "_feature";
    var audio_key = key + "_audio";
    var preview_key = key + "_preview";

    if (feature_key in report_values) {
        values["feature"] = report_values[feature_key];
    }

    if (audio_key in report_values) {
        values["audio"] = report_values[audio_key];
    }

    if (preview_key in report_values) {
        values["preview"] = report_values[preview_key];
    }

    return values;
}

function get_video_configuration_values(report_values) {
    var video_configuration = {};

    var video_configuration_data_points_1 = [
        'encoding_log_shows_no_errors',
        'correct_video_codec_used',
        'frame_rate_same_as_native_source',
        'hd_resolution',
        'field_dominance_set_to_none',
        'tagged_as_progressive',
        'clap_tag_removed',
        'pasp_correct',
        'gamma_tag_removed',
        'video_asset_does_not_contain',
        'video_proper_aspect_ratio',
        'websites_not_listed',
        'cropping_values_correct'
    ]

    var video_configuration_data_points_2 = [
        'trailer_no_promotional_bumpers',
        'trailer_same_aspect_ratio',
        'trailer_general_audience',
        'file_starts_with_black',
        'program_starts',
        'program_ends_black_frame_feature',
        'file_starts_fade_up_down',
        'program_ends_black_frame_preview',
        'program_ends_fade_down'
    ]

    for (var i = 0; i < video_configuration_data_points_1.length; i++) {
        var data_point = video_configuration_data_points_1[i];
        video_configuration[data_point] = get_feature_preview_values(report_values, data_point);
    }

    for (var i = 0; i < video_configuration_data_points_2.length; i++) {
        var data_point = video_configuration_data_points_2[i];
        video_configuration[data_point] = report_values[data_point];
    }

    return video_configuration;
}

function get_audio_configuration_values(report_values) {
    var audio_configuration = {};

    var audio_configuration_data_points = [
        'audio_configuration_verified',
        'audio_in_sync_with_video',
        'audio_tagged_correctly',
        'no_audio_cut_off',
        'trt_audio_equals_trt_video',
        'correct_language_present'
    ]

    for (var i = 0; i < audio_configuration_data_points.length; i++) {
        var data_point = audio_configuration_data_points[i];
        audio_configuration[data_point] = get_feature_audio_preview_values(report_values, data_point);
    }

    var audio_configuration_data_points_2 = [
        'feature_audio_config_language_1',
        'feature_audio_config_language_2',
        'feature_audio_config_language_3',
        'feature_audio_config_language_4',
        'feature_audio_config_language_5',
        'feature_audio_config_language_6',
        'feature_audio_config_language_7',
        'feature_audio_config_language_8',
        'feature_audio_config_type_1',
        'feature_audio_config_type_2',
        'feature_audio_config_type_3',
        'feature_audio_config_type_4',
        'feature_audio_config_type_5',
        'feature_audio_config_type_6',
        'feature_audio_config_type_7',
        'feature_audio_config_type_8',
        'audio_bundle_language_1',
        'audio_bundle_language_2',
        'audio_bundle_language_3',
        'audio_bundle_language_4',
        'audio_bundle_language_5',
        'audio_bundle_language_6',
        'audio_bundle_language_7',
        'audio_bundle_language_8',
        'audio_bundle_type_1',
        'audio_bundle_type_2',
        'audio_bundle_type_3',
        'audio_bundle_type_4',
        'audio_bundle_type_5',
        'audio_bundle_type_6',
        'audio_bundle_type_7',
        'audio_bundle_type_8',
        'preview_trailer_audio_config_language_1',
        'preview_trailer_audio_config_language_2',
        'preview_trailer_audio_config_language_3',
        'preview_trailer_audio_config_language_4',
        'preview_trailer_audio_config_language_5',
        'preview_trailer_audio_config_language_6',
        'preview_trailer_audio_config_language_7',
        'preview_trailer_audio_config_language_8',
        'preview_trailer_audio_config_type_1',
        'preview_trailer_audio_config_type_2',
        'preview_trailer_audio_config_type_3',
        'preview_trailer_audio_config_type_4',
        'preview_trailer_audio_config_type_5',
        'preview_trailer_audio_config_type_6',
        'preview_trailer_audio_config_type_7',
        'preview_trailer_audio_config_type_8'
    ]

    for (var x = 0; x < audio_configuration_data_points_2.length; x++) {
        var data_point = audio_configuration_data_points_2[x];
        audio_configuration[data_point] = report_values[data_point];
    }

    return audio_configuration;
}

function get_assets_values(report_values) {
    var assets = {};

    return assets;
}

function get_chapter_thumbnails_values(report_values) {
    var chapter_thumbnails = {};

    return chapter_thumbnails;
}

function get_report_values() {
    // Return an object containing the element evaluation's values
    var top = bvr.src_el.getParent("#metadata_eval_panel");
    var report_values = spt.api.get_input_values(top, null, false);

    console.log(report_values);

    // Name of the report
    var name = report_values.name_data;

    // Title section values
    var title_data = report_values.title_data;
    var episode = report_values.episode;
    var cont = report_values.cont;
    var source_type = report_values.source_type;
    var operator = report_values.operator;
    var date = report_values.date;
    var trt_feature = report_values.trt_feature;
    var trt_trailer = report_values.trt_trailer;

    var qc_notes = report_values.qc_notes;

    var report_data = {};

    report_data["video_configuration"] = get_video_configuration_values(report_values);
    report_data["audio_configuration"] = get_audio_configuration_values(report_values);
    report_data["assets"] = get_assets_values(report_values);
    report_data["chapter_thumbnails"] = get_chapter_thumbnails_values(report_values);

    var qc_report_object = {
        'name': name,
        'title': title_data,
        'episode': episode,
        'cont': cont,
        'source_type': source_type,
        'operator': operator,
        'date': date,
        'trt_feature': trt_feature,
        'trt_trailer': trt_trailer,
        'qc_notes': qc_notes,
        'report_data': JSON.stringify(report_data)
    };

    return qc_report_object;
}

var code = '%s';

var server = TacticServerStub.get();
var search_key = server.build_search_key('twog/metadata_report', code, 'twog');

var qc_report_object = get_report_values();

var metadata_eval_panel = document.getElementById('metadata_eval_panel');

spt.app_busy.show("Saving...");
server.update(search_key, qc_report_object);
spt.api.load_panel(metadata_eval_panel, 'qc_reports.MetaDataReportWdg', {'search_key': search_key});

spt.app_busy.hide();
''' % code
        }

        return behavior

    # TODO: This function is the same as the one in ElementEvalWdg, merge the two into one
    def get_text_input_wdg(self, field_name, width=200):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(field_name)
        textbox_wdg.set_name(field_name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if hasattr(self, field_name):
            textbox_wdg.set_value(getattr(self, field_name))

        return textbox_wdg

    # TODO: This function is the same as the one in ElementEvalWdg, merge the two into one
    def get_date_calendar_wdg(self):
        date_calendar_wdg = CalendarInputWdg("date")
        date_calendar_wdg.set_option('show_activator', 'true')
        date_calendar_wdg.set_option('show_time', 'false')
        date_calendar_wdg.set_option('width', '300px')
        date_calendar_wdg.set_option('id', 'date')
        date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

        try:
            date = self.date
            date_calendar_wdg.set_value(date)
        except AttributeError:
            pass

        return date_calendar_wdg

    def get_text_area_input_wdg(self, name, id):
        text_area_wdg = TextAreaWdg()
        text_area_wdg.set_id(id)

        if hasattr(self, id):
            text_area_wdg.set_value(self.general_comments)

        text_area_div = DivWdg(name)
        text_area_div.add_style('font-weight', 'bold')

        section_div = DivWdg()
        section_div.add_style('margin', '10px')
        section_div.add(text_area_div)
        section_div.add(text_area_wdg)

        return section_div

    def get_true_false_select_wdg(self, name, width=80):
        """
        Set up a select widget with True and False values, with the labels being Yes and No. Most of the MetaData report
        is made up of such select widgets.

        :name: String, set as the name and ID for the select widget. Should correspond to a column on the MetaData
               sobject
        :width: int, the desired width of the widget in pixels
        :return: SelectWdg
        """

        select_wdg = SelectWdg(name)
        select_wdg.set_id(name)
        select_wdg.add_style('width', '{0}px'.format(width))
        select_wdg.add_empty_option()

        select_wdg.append_option('Yes', True)
        select_wdg.append_option('No', False)

        # If the report was loaded from a save, and if the value is set, load it in the widget
        if hasattr(self, name):
            select_wdg.set_value(getattr(self, name))

        return select_wdg

    def get_language_select_wdg(self, name, width=100):
        """
        Get a select widget that chooses from the languages saved in the database.

        :param name: String, set as the name and ID for the select widget. Should correspond to a column on the MetaData
                     sobject
        :param width: int, the desired width of the widget in pixels
        :return: SelectWdg
        """
        select_wdg = SelectWdg(name)
        select_wdg.set_id(name)
        select_wdg.add_style('width', '{0}px'.format(width))
        select_wdg.add_empty_option()

        language_search = Search('twog/language')
        languages = language_search.get_sobjects()

        for language in languages:
            select_wdg.append_option(language.get_value('name'), language.get_code())

        if hasattr(self, name):
            select_wdg.set_value(getattr(self, name))

        return select_wdg

    def get_type_select_wdg(self, name, width=80):
        """
        :name: String, set as the name and ID for the select widget. Should correspond to a column on the MetaData
               sobject
        :width: int, the desired width of the widget in pixels
        :return: SelectWdg
        """

        select_wdg = SelectWdg(name)
        select_wdg.set_id(name)
        select_wdg.add_style('width', '{0}px'.format(width))
        select_wdg.add_empty_option()

        types = (
            ('(5.1) L', '5_1_l'),
            ('(5.1) R', '5_1_r'),
            ('(5.1) C', '5_1_c'),
            ('(5.1) Lfe', '5_1_lfe'),
            ('(5.1) Ls', '5_1_ls'),
            ('(5.1) Rs', '5_1_rs'),
            ('(7.1) L', '7_1_l'),
            ('(7.1) R', '7_1_r'),
            ('(7.1) C', '7_1_c'),
            ('(7.1) Lfe', '7_1_lfe'),
            ('(7.1) Ls', '7_1_ls'),
            ('(7.1) Rs', '7_1_rs'),
            ('(7.1) SBL', '7_1_sbl'),
            ('(7.1) SBR', '7_1_sbr'),
            ('(Stereo) Lt', 'stereo_lt'),
            ('(Stereo) Rt', 'stereo_rt'),
            ('(Stereo) Lt, Rt', 'stereo_lt_rt'),
            ('(Stereo) L', 'stereo_l'),
            ('(Stereo) R', 'stereo_r'),
            ('(Stereo) L, R', 'stereo_l_r'),
            ('Mono', 'mono')
        )

        for audio_type in types:
            type_label = audio_type[0]
            type_value = audio_type[1]

            select_wdg.append_option(type_label, type_value)

        # If the report was loaded from a save, and if the value is set, load it in the widget
        if hasattr(self, name):
            select_wdg.set_value(getattr(self, name))

        return select_wdg

    def get_top_section(self):
        title_span = SpanWdg()
        title_span.add_style('display', 'inline-block')
        title_span.add("Title")
        title_span.add(self.get_text_input_wdg('title_data', 400))

        episode_span = SpanWdg()
        episode_span.add_style('display', 'inline-block')
        episode_span.add("Episode")
        episode_span.add(self.get_text_input_wdg('episode', 400))

        cont_span = SpanWdg()
        cont_span.add_style('display', 'inline-block')
        cont_span.add("Cont")
        cont_span.add(self.get_text_input_wdg('cont', 400))

        source_type_span = SpanWdg()
        source_type_span.add_style('display', 'inline-block')
        source_type_span.add("Source Type")
        source_type_span.add(self.get_text_input_wdg('source_type', 400))

        left_div = DivWdg()
        left_div.add_style('float', 'left')
        left_div.add_style('margin-right', '20px')
        left_div.add(title_span)
        left_div.add(episode_span)
        left_div.add(cont_span)
        left_div.add(source_type_span)

        qc_operator_span = SpanWdg()
        qc_operator_span.add_style('display', 'inline-block')
        qc_operator_span.add('QC Operator')
        qc_operator_span.add(self.get_text_input_wdg('qc_operator', 400))

        qc_date_span = SpanWdg()
        qc_date_span.add_style('display', 'inline-block')
        qc_date_span.add('QC Date')
        qc_date_span.add(self.get_date_calendar_wdg())

        trt_feature_span = SpanWdg()
        trt_feature_span.add_style('display', 'inline-block')
        trt_feature_span.add('TRT Feature')
        trt_feature_span.add(self.get_text_input_wdg('trt_feature', 400))

        trt_trailer_preview_span = SpanWdg()
        trt_trailer_preview_span.add_style('display', 'inline-block')
        trt_trailer_preview_span.add('TRT Trailer/Preview')
        trt_trailer_preview_span.add(self.get_text_input_wdg('trt_trailer_preview', 400))

        right_div = DivWdg()
        right_div.add(qc_operator_span)
        right_div.add(qc_date_span)
        right_div.add(trt_feature_span)
        right_div.add(trt_trailer_preview_span)

        section_div = DivWdg()
        section_div.add(left_div)
        section_div.add(right_div)
        section_div.add(self.get_text_area_input_wdg('QC Notes', 'qc_notes'))

        return section_div

    def get_section_one(self):
        section_div = DivWdg()

        label_value_pairs_1 = (
            ('Encoding Log Shows No Errors?', 'encoding_log_shows_no_errors'),
            ('Correct Video Codec Used (Apple ProRes (HQ)422)?', 'correct_video_codec_used'),
            ('Frame Rate Same as the Native Source (23.976, 24, 25, 29.97)?', 'frame_rate_same_as_native_source'),
            ('HD Resolution is 1920x1080 (Square Pixel Aspect Ratio)?', 'hd_resolution'),
            ('Field Dominance Set to None?', 'field_dominance_set_to_none'),
            ('Tagged as Progressive?', 'tagged_as_progressive'),
            ('Clap Tag has been Removed?', 'clap_tag_removed'),
            ('PASP is Correct? (1:1)', 'pasp_correct'),
            ('Gamma Tag has been Removed?', 'gamma_tag_removed'),
            ('Video Asset does not Contain FBI, MPAA, or Release Data Tagging?', 'video_asset_does_not_contain'),
            ('Video is Proper Aspect Ratio (Pic is not Squeezed, Cut Off, Distorted)?', 'video_proper_aspect_ratio'),
            ('Websites are not Listed in Program and Credits?', 'websites_not_listed'),
            ('*Cropping Values are Correct (No Inactive Pixels)?', 'cropping_values_correct')
        )

        label_value_pairs_2 = (
            ('Trailer does not Contain any Promotional Bumpers?', 'trailer_no_promotional_bumpers'),
            ('Trailer is Same Aspect Ratio as Feature?', 'trailer_same_aspect_ratio'),
            ('*Trailer Contains Content Suitable for a General Audience?', 'trailer_general_audience')
        )

        label_value_pairs_3 = (
            ('File Starts @ 00:59:59:00 With Black?', 'file_starts_with_black'),
            ('Program Starts @ 1:00:00:00?', 'program_starts'),
            ('Program ends with at least one black frame?', 'program_ends_black_frame_feature')
        )

        label_value_pairs_4 = (
            ('File starts @ 1:00:00:00 with fade up/down?', 'file_starts_fade_up_down'),
            ('Program begins with at least one black frame?', 'program_ends_black_frame_preview'),
            ('Program ends with fade down (with at least once black frame)?', 'program_ends_fade_down')
        )

        section_div.add(self.get_section_one_table_one(label_value_pairs_1, label_value_pairs_2))
        section_div.add(self.get_section_one_table_two(label_value_pairs_3))
        section_div.add(self.get_section_one_table_three(label_value_pairs_4))
        section_div.add(self.get_text_area_input_wdg('Video Notes', 'video_notes'))

        return section_div

    def get_section_one_table_one(self, label_value_pairs_1, label_value_pairs_2):
        table = Table()
        table.add_row()

        table.add_header('')
        table.add_header('Feature')
        table.add_header('Trailer/Preview')

        for label_value_pair in label_value_pairs_1:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)

            for column in ('feature', 'preview'):
                select_wdg_id = value + '_' + column
                table.add_cell(self.get_true_false_select_wdg(select_wdg_id))

        for label_value_pair in label_value_pairs_2:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)
            table.add_cell()
            table.add_cell(self.get_true_false_select_wdg(value))

        return table

    def get_section_one_table_two(self, label_value_pairs):
        table = Table()
        table.add_style('float', 'left')

        table.add_row()
        table.add_header('Confirm the build of the feature')

        for label_value_pair in label_value_pairs:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)
            table.add_cell(self.get_true_false_select_wdg(value))

        return table

    def get_section_one_table_three(self, label_value_pairs):
        table = Table()

        table.add_row()
        table.add_header('Confirm the build of trailer/preview')

        for label_value_pair in label_value_pairs:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)
            table.add_cell(self.get_true_false_select_wdg(value))

        return table

    def get_section_two(self):
        section_div = DivWdg()

        feature_audio_config_table = self.get_audio_configuration_section_table('Feature: Audio Config',
                                                                                'feature_audio_config')

        audio_bundle_table = self.get_audio_configuration_section_table('Audio Bundle', 'audio_bundle')

        preview_trailer_audio_config = self.get_audio_configuration_section_table('Preview/Trailer: Audio Config',
                                                                                  'preview_trailer_audio_config',
                                                                                  float_left=False)

        section_div.add(feature_audio_config_table)
        section_div.add(audio_bundle_table)
        section_div.add(preview_trailer_audio_config)

        section_div.add(self.get_section_two_bottom_table())
        section_div.add(self.get_text_area_input_wdg('Audio Notes', 'audio_notes'))

        return section_div

    def get_audio_configuration_section_table(self, name, id, float_left=True):
        table = Table()

        if float_left:
            table.add_style('float: left')

        table.add_style('margin', '10px')
        table.add_row()
        table.add_header(name)

        for i in range(1, 9):
            table.add_row()

            label_cell = table.add_cell('TRK. {0}'.format(i))
            label_cell.add_style('padding', '10px 10px 10px 0px')

            table.add_cell(self.get_language_select_wdg(id + '_language_' + str(i)))
            table.add_cell(self.get_type_select_wdg(id + '_type_' + str(i)))

        return table

    def get_section_two_bottom_table(self):
        table = Table()
        table.add_style('margin', '10px')
        table.add_row()

        table.add_header('')
        table.add_header('Feature')
        table.add_header('Audio Bundle')
        table.add_header('Trailer/Preview')

        label_value_pairs = (
            ('Audio configuration verified (stereo or mono/mapping is correct)?', 'audio_configuration_verified'),
            ('Audio is in sync with video (checked in 3 random spots and head/tail)?', 'audio_in_sync_with_video'),
            ('Audio is tagged correctly?', 'audio_tagged_correctly'),
            ('No audio is cut off (at beginning or end)?', 'no_audio_cut_off'),
            ('TRT of audio equals TRT of the video?', 'trt_audio_equals_trt_video'),
            ('Correct language is present (on applicable channels)?', 'correct_language_present')
        )

        for label_value_pair in label_value_pairs:
            table.add_row()
            table.add_cell(label_value_pair[0])

            for section in ('feature', 'audio', 'preview'):
                table.add_cell(self.get_true_false_select_wdg(label_value_pair[1] + '_' + section))

        return table

    def get_section_three(self):
        section_div = DivWdg()

        section_div.add(self.get_delivery_snapshot_section())
        section_div.add(self.get_section_three_subsection_one())
        section_div.add(self.get_section_three_subsection_two())

        return section_div

    def get_delivery_snapshot_section(self):
        label_value_pairs = (
            ('Feature', 'feature_delivery_snapshot'),
            ('Trailer', 'trailer_delivery_snapshot'),
            ('Alt Audio', 'alt_audio_delivery_snapshot'),
            ('Subtitle', 'subtitle_delivery_snapshot'),
            ('CC', 'cc_delivery_snapshot'),
            ('Vendor Notes', 'vendor_notes_delivery_snapshot'),
            ('Poster Art', 'poster_art_delivery_snapshot'),
            ('Dub Card', 'dub_card_delivery_snapshot')
        )

        table = Table()
        table.add_style('float', 'left')

        table.add_row()
        table.add_header('Delivery Snapshot')

        for label_value_pair in label_value_pairs:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)
            table.add_cell(self.get_true_false_select_wdg(value))

        section_div = DivWdg()
        section_div.add(table)

        return section_div

    def get_section_three_subsection_one(self):
        label_value_pairs = (
            ('Forced narrative on feature?', 'forced_narrative_feature',
             'Does not overlap any credits or other text?', 'overlap_credits_text_1'),
            ('Forced narrative on trailer?', 'forced_narrative_trailer',
             'Does not overlap any credits or other text?', 'overlap_credits_text_2'),
            ('Subtitles on feature?', 'subtitles_on_feature',
             'Does not overlap any credits or other text?', 'overlap_credits_text_3'),
            ('Subtitles on trailer?', 'subtitles_on_trailer',
             'Does not overlap any credits or other text?', 'overlap_credits_text_4'),
        )

        table = Table()

        for label_value_pair in label_value_pairs:
            label_1, value_1, label_2, value_2 = label_value_pair

            table.add_row()
            table.add_cell(label_1)
            table.add_cell(self.get_true_false_select_wdg(value_1))
            table.add_cell(label_2)
            table.add_cell(self.get_true_false_select_wdg(value_2))

        section_div = DivWdg()
        section_div.add(table)

        return section_div

    def get_section_three_subsection_two(self):

        label_value_pairs = (
            ('Dub card dimensions match feature?', 'dub_card_dimensions',
             'CC is in sync with video?', 'cc_in_sync'),
            ('Dub card FPS matches feature?', 'dub_card_fps',
             'Subtitles are in sync with video?', 'subtitles_in_sync'),
            ('Dub card language matches locale?', 'dub_card_language',
             'Subtitles have correct language?', 'subtitles_correct_language'),
            ('Dub card duration is 4 to 5 seconds?', 'dub_card_duration', '', ''),
            ('Dub card contains no audio tracks?', 'dub_card_contains', '', '')
        )

        label_value_pairs_3 = (
            ('Dub card text is not cut off when feature cropping values are applied?', 'dub_card_text_not_cut_off')
        )

        table = Table()

        for label_value_pair in label_value_pairs:
            label_1, value_1, label_2, value_2 = label_value_pair

            table.add_row()
            table.add_cell(label_1)
            table.add_cell(self.get_true_false_select_wdg(value_1))

            table.add_cell(label_2)

            if (value_2):
                table.add_cell(self.get_true_false_select_wdg(value_2))
            else:
                table.add_cell(value_2)

        section_div = DivWdg()
        section_div.add(table)

        return section_div

    def get_section_four(self):
        label_value_pairs_1 = (
            ('Image is a JPEG (.jpg extension)?', 'image_is_jpeg_chapter'),
            ('DPI is 72 or greater?', 'dpi_is_72_chapter'),
            ('Color profile is RGB?', 'color_profile_rgb_chapter'),
            ('Same aspect ratio as video?', 'same_aspect_ratio_as_video_chapter'),
            ('Only active pixels are included (no dirty edges)?', 'only_active_pixels_chapter'),
            ('Horizontal dimension is at least 640?', 'horizontal_dimension_640_chapter'),
            ('Each chapter has a thumbnail?', 'each_chapter_thumbnail_chapter')
        )

        label_value_pairs_2 = (
            ('Image is a JPEG (.jpg extension)?', 'image_is_jpeg_poster'),
            ('DPI is 72 or greater?', 'dpi_is_72_poster'),
            ('Color profile is RGB?', 'color_profile_rgb_poster'),
            ('Resolution is at least 1400x2100?', 'resolution_poster'),
            ('Aspect ratio is 2:3?', 'aspect_ratio_poster'),
            ('Contains key art and title only (no film rating on image)?', 'contains_key_art_poster'),
            ('No DVD cover, date stamp, URL or promo tagging included?', 'no_promo_poster')
        )

        section_div = DivWdg()

        section_div.add(self.get_section_four_table_one(label_value_pairs_1))
        section_div.add(self.get_section_four_table_two(label_value_pairs_2))

        return section_div

    def get_section_four_table_one(self, label_value_pairs):
        table = Table()
        table.add_style('float', 'left')

        table.add_row()
        table.add_header('Chapter Thumbnails')

        for label_value_pair in label_value_pairs:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)
            table.add_cell(self.get_true_false_select_wdg(value + '_chapter'))

        return table

    def get_section_four_table_two(self, label_value_pairs):
        table = Table()

        table.add_row()
        table.add_header('Poster Art (One Sheet)')

        for label_value_pair in label_value_pairs:
            label, value = label_value_pair

            table.add_row()
            table.add_cell(label)
            table.add_cell(self.get_true_false_select_wdg(value + '_poster'))

        return table

    def get_save_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_button = ButtonNewWdg(title='Save', icon='SAVE')
        save_button.add_class('save_button')
        save_button.add_behavior(self.get_save_behavior(self.metadata_report_sobject.get_code()))

        section_span.add(save_button)

        return section_span

    def get_display(self):
        main_wdg = DivWdg()
        main_wdg.set_id('metadata_eval_panel')

        main_wdg.add(self.get_top_section())

        main_wdg.add(self.get_section_one())
        main_wdg.add(self.get_section_two())
        main_wdg.add(self.get_section_three())
        main_wdg.add(self.get_section_four())

        if hasattr(self, 'metadata_report_sobject') and self.metadata_report_sobject:
            main_wdg.add(self.get_save_button())

        return main_wdg
