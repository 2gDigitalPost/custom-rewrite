from pyasm.widget import CheckboxWdg, SelectWdg
from tactic.ui.common import BaseRefreshWdg

from pyasm.prod.biz import ProdSetting
from pyasm.web import DivWdg, HtmlElement, Table
from tactic.ui.input import TextInputWdg


class ExternalRejectionOnTitleOrderWdg(BaseRefreshWdg):
    def init(self):
        self.title_order_code = self.get_kwargs().get('code')

    @staticmethod
    def setup_checkboxes_div(header_text, reasons_list):
        checkbox_table = Table()

        header_row = checkbox_table.add_row()
        header = checkbox_table.add_header(data=header_text, row=header_row)
        header.add_style('text-align', 'center')
        header.add_style('text-decoration', 'underline')

        for reason_id, reason_name in reasons_list:
            checkbox = CheckboxWdg(name=reason_id)

            checkbox_row = checkbox_table.add_row()

            checkbox_table.add_cell(data=checkbox, row=checkbox_row)
            checkbox_table.add_cell(data=reason_name, row=checkbox_row)

        return checkbox_table

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('new-external-rejection-form')

        # Set up the <input> widget for 'name'
        outer_div.add(HtmlElement.label('Name'))
        name_input = TextInputWdg(name='name')
        outer_div.add(name_input)

        root_cause_type_wdg = SelectWdg(name='root_cause_types',
                                        values=ProdSetting.get_seq_by_key('external_rejection_root_cause_types'))
        outer_div.add(root_cause_type_wdg)

        # TODO: Get this list from the schema, not hard coded
        video_rejection_reasons = [
            ('video_cropping', 'Cropping'),
            ('video_digital_hits_macroblocking', 'Digital Hits / Macroblocking'),
            ('video_dropped_frames', 'Dropped Frames'),
            ('video_dropout', 'Dropout'),
            ('video_duplicate_frames', 'Duplicate Frames'),
            ('video_interlacing_on_a_progressive_file', 'Interlacing on a Progressive File'),
            ('video_motion_image_lag', 'Motion / Image Lag'),
            ('video_missing_elements', 'Missing Elements'),
            ('video_corrupt_file', 'Corrupt File'),
            ('video_incorrect_aspect_ratio', 'Incorrect Aspect Ratio'),
            ('video_incorrect_resolution', 'Incorrect Resolution'),
            ('video_incorrect_pixel_aspect_ratio', 'Incorrect Pixel Aspect Ratio'),
            ('video_incorrect_specifications', 'Incorrect Specifications'),
            ('video_incorrect_head_tail_format', 'Incorrect Head / Tail Format'),
            ('video_other', 'Other')
        ]

        audio_rejection_reasons = [
            ('video_incorrect_audio_mapping', 'Incorrect Audio Mapping'),
            ('video_missing_audio_channel', 'Missing Audio Channel'),
            ('video_crackle_hiss_pop_static_ticks', 'Crackle / Hiss / Pop / Static / Ticks'),
            ('video_distortion', 'Distortion'),
            ('video_dropouts', 'Dropouts'),
            ('video_sync_issue', 'Sync Issue'),
            ('video_missing_elements', 'Missing Elements'),
            ('video_corrupt_missing_file', 'Corrupt / Missing File'),
            ('video_incorrect_specifications', 'Incorrect Specifications'),
            ('video_other', 'Other')
        ]

        metadata_rejection_reasons = [
            ('metadata_missing_information', 'Missing Information'),
            ('metadata_incorrect_information', 'Incorrect Information'),
            ('metadata_incorrect_formatting', 'Incorrect Formatting'),
            ('metadata_other', 'Other')
        ]

        subtitle_rejection_reasons = [
            ('subtitle_interlacing_on_subtitles', 'Interlacing on Subtitles'),
            ('subtitle_incorrect_subtitles', 'Incorrect Subtitles'),
            ('subtitle_sync_issue', 'Sync Issue'),
            ('subtitle_overlapping_other_text', 'Overlapping Other Text'),
            ('subtitle_other', 'Other')
        ]

        closed_captions_rejection_reasons = [
            ('closed_captions_sync_issue', 'Sync Issue'),
            ('closed_captions_incorrect_cc', 'Incorrect CC'),
            ('closed_captions_overlapping_other_text', 'Overlapping Other Text'),
            ('closed_captions_other', 'Other')
        ]

        video_checkbox_table = self.setup_checkboxes_div('Video', video_rejection_reasons)
        audio_checkbox_table = self.setup_checkboxes_div('Audio', audio_rejection_reasons)
        metadata_checkbox_table = self.setup_checkboxes_div('MetaData', metadata_rejection_reasons)
        subtitle_checkbox_table = self.setup_checkboxes_div('Subtitles', subtitle_rejection_reasons)
        closed_captions_checkbox_table = self.setup_checkboxes_div('Closed Captions', closed_captions_rejection_reasons)

        outer_div.add(video_checkbox_table)
        outer_div.add(audio_checkbox_table)
        outer_div.add(metadata_checkbox_table)
        outer_div.add(subtitle_checkbox_table)
        outer_div.add(closed_captions_checkbox_table)

        return outer_div
