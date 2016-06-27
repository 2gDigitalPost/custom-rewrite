from qc_reports.audio_configuration_lines_wdg import AudioLinesTableWdg
from qc_reports.element_eval_lines_wdg import ElementEvalLinesWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextInputWdg
from tactic.ui.widget import CalendarInputWdg, ButtonNewWdg

from pyasm.search import Search
from pyasm.web import Table, DivWdg, SpanWdg
from pyasm.widget import SelectWdg, CheckboxWdg, TextAreaWdg


class MetaDataReportWdg(BaseRefreshWdg):
    def init(self):
        self.metadata_report_sobject = self.get_sobject_from_kwargs()

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
            select_wdg.append_option(language.get_value('name'), language.get_value('name'))

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

    def get_section_one(self):
        section_div = DivWdg()

        table1 = Table()
        table1.add_row()

        table1.add_header('')
        table1.add_header('Feature')
        table1.add_header('Trailer/Preview')

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

        self.get_section_one_table_one(table1, label_value_pairs_1)

        label_value_pairs_2 = (
            ('Trailer does not Contain any Promotional Bumpers?', 'trailer_no_promotional_bumpers'),
            ('Trailer is Same Aspect Ratio as Feature?', 'trailer_same_aspect_ratio'),
            ('*Trailer Contains Content Suitable for a General Audience?', 'trailer_general_audience')
        )

        label_value_pairs_3 = (
            'File Starts @ 00:59:59:00 With Black?', 'file_starts_with_black',
            'Program Starts @ 1:00:00:00?', 'program_starts',
            'Program ends with at least one black frame?', 'program_ends_black_frame_feature'
        )

        label_value_pairs_4 = (
            'File starts @ 1:00:00:00 with fade up/down?', 'file_starts_fade_up_down',
            'Program begins with at least one black frame?', 'program_ends_black_frame_preview',
            'Program ends with fade down (with at least once black frame)?', 'program_ends_fade_down'
        )



        section_div.add(table1)

        return section_div

    def get_section_one_table_one(self, table, label_value_pairs):
        for label_value_pair in label_value_pairs:
            label = label_value_pair[0]
            value = label_value_pair[1]

            table.add_row()
            table.add_cell(label)

            for column in ('feature', 'preview'):
                select_wdg_id = value + '_' + column
                table.add_cell(self.get_true_false_select_wdg(select_wdg_id))

        return table

    def get_section_two(self):
        section_div = DivWdg()

        feature_audio_config_table = self.get_audio_configuration_section_table('Feature: Audio Config',
                                                                                'feature_audio_config')

        audio_bundle_table = self.get_audio_configuration_section_table('Audio Bundle', 'audio_bundle')

        preview_trailer_audio_config = self.get_audio_configuration_section_table('Preview/Trailer: Audio Config',
                                                                                  'preview_trailer_audio_config')

        section_div.add(feature_audio_config_table)
        section_div.add(audio_bundle_table)
        section_div.add(preview_trailer_audio_config)

        section_div.add(self.get_section_two_bottom_table())

        return section_div

    def get_section_three(self):
        section_div = DivWdg()



    def get_audio_configuration_section_table(self, name, id):
        table = Table()
        table.add_style('float: left')
        table.add_style('margin', '10px')
        table.add_row()
        table.add_header(name)

        for i in range(1, 9):
            table.add_row()

            label_cell = table.add_cell('TRK. {0}'.format(i))
            label_cell.add_style('padding', '10px 10px 10px 0px')

            table.add_cell(self.get_language_select_wdg(id))
            table.add_cell(self.get_type_select_wdg(id))

        return table

    def get_section_two_bottom_table(self):
        table = Table()
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

            for section in ('feature, audio, preview'):
                table.add_cell(self.get_true_false_select_wdg(label_value_pair[1] + '_' + section))

        return table

    def get_delivery_snapshot_section(self):
        section_div = DivWdg()

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

    def get_section_three_subsection_one(self):
        section_div = DivWdg()

        label_value_pairs_1 = (
            ('Forced narrative on feature?', 'forced_narrative_feature'),
            ('Forced narrative on trailer?', 'forced_narrative_trailer'),
            ('Subtitles on feature?', 'subtitles_on_feature'),
            ('Subtitles on trailer?', 'subtitles_on_trailer')
        )

        label_value_pairs_2 = (
            ('Does not overlap any credits or other text?', 'overlap_credits_text_1'),
            ('Does not overlap any credits or other text?', 'overlap_credits_text_2'),
            ('Does not overlap any credits or other text?', 'overlap_credits_text_3'),
            ('Does not overlap any credits or other text?', 'overlap_credits_text_4')
        )

    def get_display(self):
        main_wdg = DivWdg()
        main_wdg.set_id('metadata_report_wdg')

        main_wdg.add(self.get_section_one())
        main_wdg.add(self.get_section_two())

        return main_wdg
