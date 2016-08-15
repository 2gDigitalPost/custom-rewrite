import os
import json
from ConfigParser import SafeConfigParser

from pyasm.command import Command
from pyasm.search import Search

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus.flowables import HRFlowable

from pdf_export_utils import get_name_from_code, get_top_table, NumberedCanvas


def get_title_table(metadata_report_sobject):
    title_table_data = [
        ['Title:', metadata_report_sobject.get('title'), 'QC Operator:', metadata_report_sobject.get('operator')],
        ['Episode:', metadata_report_sobject.get('episode'), 'QC Date:', metadata_report_sobject.get('date')],
        ['Cont:', metadata_report_sobject.get('cont'), 'TRT Feature:', metadata_report_sobject.get('trt_feature')],
        ['Source Type:', metadata_report_sobject.get('source_type'),
         'TRT Trailer/Preview:', metadata_report_sobject.get('trt_trailer')],
        ['QC Notes:', metadata_report_sobject.get('qc_notes')]
    ]

    title_table = Table(title_table_data, hAlign='LEFT', colWidths=[(1 * inch), (2 * inch), (1 * inch), (2 * inch)])

    return title_table


def get_video_configuration_table_one(report_data):
    styleSheet = getSampleStyleSheet()

    video_configuration_data = report_data.get('video_configuration')

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

    table_data = [
        ['', Paragraph('<strong>Feature</strong>', styleSheet['BodyText']),
         Paragraph('<strong>Trailer/Preview</strong>', styleSheet['BodyText'])]
    ]

    for label_value_pair in label_value_pairs_1:
        table_data.append(
            [Paragraph('{0}'.format(label_value_pair[0]), styleSheet['BodyText']),
             video_configuration_data.get(label_value_pair[1]).get('feature'),
             video_configuration_data.get(label_value_pair[1]).get('preview')]
        )

    for label_value_pair in label_value_pairs_2:
        table_data.append(
            [Paragraph('{0}'.format(label_value_pair[0]), styleSheet['BodyText']),
             '',
             video_configuration_data.get(label_value_pair[1])]
        )

    table = Table(table_data, hAlign='LEFT', colWidths=[(3 * inch), (1.5 * inch), (1.5 * inch)])\

    return table


def get_video_configuration_table_two(report_data):
    styleSheet = getSampleStyleSheet()

    video_configuration_data = report_data.get('video_configuration')

    label_value_pairs_1 = (
        ('File Starts @ 00:59:59:00 With Black?', 'file_starts_with_black'),
        ('Program Starts @ 1:00:00:00?', 'program_starts'),
        ('Program ends with at least one black frame?', 'program_ends_black_frame_feature')
    )

    label_value_pairs_2 = (
        ('File starts @ 1:00:00:00 with fade up/down?', 'file_starts_fade_up_down'),
        ('Program begins with at least one black frame?', 'program_ends_black_frame_preview'),
        ('Program ends with fade down (with at least once black frame)?', 'program_ends_fade_down')
    )

    table_data_1 = [
        [Paragraph('<strong>Confirm the build of the feature</strong>', styleSheet['BodyText']), '']
    ]

    table_data_2 = [
        [Paragraph('<strong>Confirm the build of the trailer/preview</strong>', styleSheet['BodyText']), '']
    ]

    for label_value_pair in label_value_pairs_1:
        table_data_1.append(
            [Paragraph(label_value_pair[0], styleSheet['BodyText']),
             video_configuration_data.get(label_value_pair[1])]
        )

    for label_value_pair in label_value_pairs_2:
        table_data_2.append(
            [Paragraph(label_value_pair[0], styleSheet['BodyText']),
             video_configuration_data.get(label_value_pair[1])]
        )

    table_1 = Table(table_data_1, hAlign='LEFT')
    table_2 = Table(table_data_2, hAlign='LEFT')

    table = Table([[table_1, table_2]])

    return table


def get_audio_configuration_table_one(report_data):
    styleSheet = getSampleStyleSheet()

    audio_configuration_data = report_data.get('audio_configuration')

    table_data_1 = [
        [Paragraph('<strong>Feature: Audio Config</strong>', styleSheet['BodyText'])]
    ]

    table_data_2 = [
        [Paragraph('<strong>Audio Bundle</strong>', styleSheet['BodyText'])]
    ]

    table_data_3 = [
        [Paragraph('<strong>Preview/Trailer: Audio Config</strong>', styleSheet['BodyText'])]
    ]

    for i in range(1, 9):
        table_data_1.append(
            [Paragraph('TRK. {0}'.format(i), styleSheet['BodyText']),
             audio_configuration_data.get('feature_audio_config_language_{0}'.format(i)),
             audio_configuration_data.get('feature_audio_config_type_{0}'.format(i))]
        )

        table_data_2.append(
            [Paragraph('TRK. {0}'.format(i), styleSheet['BodyText']),
             audio_configuration_data.get('audio_bundle_language_{0}'.format(i)),
             audio_configuration_data.get('audio_bundle_type_{0}'.format(i))]
        )

        table_data_3.append(
            [Paragraph('TRK. {0}'.format(i), styleSheet['BodyText']),
             audio_configuration_data.get('preview_trailer_audio_config_language_{0}'.format(i)),
             audio_configuration_data.get('preview_trailer_audio_config_type_{0}'.format(i))]
        )

    table = Table([[Table(table_data_1), Table(table_data_2), Table(table_data_3)]])

    return table


def get_audio_configuration_table_two(report_data):
    styleSheet = getSampleStyleSheet()

    audio_configuration_data = report_data.get('audio_configuration')

    label_value_pairs = (
        ('Audio configuration verified (stereo or mono/mapping is correct)?', 'audio_configuration_verified'),
        ('Audio is in sync with video (checked in 3 random spots and head/tail)?', 'audio_in_sync_with_video'),
        ('Audio is tagged correctly?', 'audio_tagged_correctly'),
        ('No audio is cut off (at beginning or end)?', 'no_audio_cut_off'),
        ('TRT of audio equals TRT of the video?', 'trt_audio_equals_trt_video'),
        ('Correct language is present (on applicable channels)?', 'correct_language_present')
    )

    table_data = [
        ['', Paragraph('<strong>Feature</strong>', styleSheet['BodyText']),
         Paragraph('<strong>Trailer/Preview</strong>', styleSheet['BodyText'])]
    ]

    for label_value_pair in label_value_pairs:
        table_data.append(
            [Paragraph(label_value_pair[0], styleSheet['BodyText']),
             audio_configuration_data.get(label_value_pair[1]).get('feature'),
             audio_configuration_data.get(label_value_pair[1]).get('preview')]
        )

    table = Table(table_data, hAlign='LEFT', colWidths=[(3 * inch), (1.5 * inch), (1.5 * inch)])

    return table


class ExportMetaDataReportCommand(Command):
    def execute(self):
        report_search_key = self.kwargs.get('report_search_key')

        if report_search_key:
            self.export_pdf(Search.get_by_search_key(report_search_key))

    @staticmethod
    def export_pdf(metadata_report_sobject):
        report_data = json.loads(metadata_report_sobject.get('report_data'))

        parser = SafeConfigParser()
        config_path = os.path.abspath(os.path.dirname(__file__))
        parser.read(config_path + '/config.ini')

        file_name = metadata_report_sobject.get('name') + '.pdf'
        save_location = parser.get('save', 'metadata_directory')

        saved_file_path = os.path.join(save_location, file_name)

        styleSheet = getSampleStyleSheet()

        I = Image(os.path.dirname(os.path.realpath(__file__)) + '/2g_logo.png')
        I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
        I.drawWidth = 1.25 * inch

        top_address_paragraph = Paragraph('<strong>2G Digital Post, Inc.</strong>', styleSheet["BodyText"])

        address_table_data = [
            [top_address_paragraph],
            ['280 E. Magnolia Blvd.'],
            ['Burbank, CA 91502'],
            ['310 - 840 - 0600'],
            ['www.2gdigitalpost.com']
        ]

        address_table = Table(address_table_data)

        P = Paragraph('<strong>Metadata Report</strong>', styleSheet["Heading2"])

        header_table = Table([[I, address_table, P]])

        title_table = get_title_table(metadata_report_sobject)

        section_one_header = Paragraph('Section 1 - Video Configuration', styleSheet['Heading3'])

        section_one_table_one = get_video_configuration_table_one(report_data)
        section_one_table_two = get_video_configuration_table_two(report_data)

        section_two_header = Paragraph('Section 2 - Audio Configuration', styleSheet['Heading3'])

        section_two_table_one = get_audio_configuration_table_one(report_data)
        section_two_table_two = get_audio_configuration_table_two(report_data)

        elements = []

        elements.append(header_table)
        elements.append(title_table)
        elements.append(section_one_header)
        elements.append(section_one_table_one)
        elements.append(section_one_table_two)
        elements.append(section_two_header)
        elements.append(section_two_table_one)
        elements.append(section_two_table_two)

        doc = SimpleDocTemplate(saved_file_path)

        doc.build(elements, canvasmaker=NumberedCanvas)
