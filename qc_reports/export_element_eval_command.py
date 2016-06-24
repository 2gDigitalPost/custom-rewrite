import datetime

from pyasm.command import Command

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table


class ExportElementEvalCommand(Command):
    def execute(self):
        report_data = self.kwargs.get('report_data')
        self.export_pdf(get_test_report_data())

    @staticmethod
    def export_pdf(report_data):
        doc = SimpleDocTemplate("Simple_table.pdf", pagesize=letter)

        elements = []

        styleSheet = getSampleStyleSheet()

        I = Image('/opt/spt/custom/qc_reports/2GLogo_small4.png')
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

        approved_rejected_table_data = [
            ['', 'Approved'],
            ['', 'Rejected']
        ]

        approved_rejected_table = Table(approved_rejected_table_data)

        P = Paragraph('<strong>{0}</strong>'.format(report_data.get('client')), styleSheet["Heading2"])

        header_table = Table([[I, address_table, P, approved_rejected_table]])

        elements.append(header_table)

        top_table_data = [
            ['Date', 'Operator', 'Style', 'Bay', 'Machine #'],
            [report_data.get('date'), report_data.get('operator'), report_data.get('style'), report_data.get('bay'),
             report_data.get('machine_number')]
        ]

        title_table_data = [
            ['Title:', report_data.get('title'), 'Format:', report_data.get('format')],
            ['Season:', report_data.get('season'), 'Standard:', report_data.get('standard')],
            ['Episode:', report_data.get('episode'), 'Frame Rate:', report_data.get('frame_rate')],
            ['Version:', report_data.get('version'), 'PO #:', report_data.get('po_number')],
            ['File Name:', report_data.get('file_name')]
        ]

        program_format_header = Paragraph('Program Format', styleSheet['Heading3'])

        program_format_table_data = [
            ['Roll-up (blank)', report_data.get('roll_up_blank')],
            ['Bars/Tone', report_data.get('bars_tone')],
            ['Black/Silence', report_data.get('black_silence_1')],
            ['Slate/Silence', report_data.get('slate_silence')],
            ['Black/Silence', report_data.get('black_silence_2')],
            ['Start of Program', report_data.get('start_of_program')],
            ['End of Program', report_data.get('end_of_program')]
        ]

        video_measurements_header = Paragraph('Video Measurements', styleSheet['Heading3'])

        video_measurements_table_data = [
            ['Active Video Begins', report_data.get('active_video_begins')],
            ['Active Video Ends', report_data.get('active_video_ends')],
            ['Horizontal Blanking', report_data.get('horizontal_blanking')],
            ['Luminance Peak', report_data.get('luminance_peak')],
            ['Chroma Peak', report_data.get('chroma_peak')],
            ['Head Logo', report_data.get('head_logo')],
            ['Tail Logo', report_data.get('tail_logo')]
        ]

        element_profile_header = Paragraph('Element Profile', styleSheet['Heading3'])

        element_profile_table_data = [
            ['Total Runtime', report_data.get('total_runtime'), 'Language', report_data.get('language')],
            ['TV/Feature/Trailer', report_data.get('tv_feature_trailer'), '(CC)/Subtitles',
             report_data.get('cc_subtitles')],
            ['Video Aspect Ratio', report_data.get('video_aspect_ratio'), 'VITC', report_data.get('vitc')],
            ['Textless @ Tail', report_data.get('textless_tail'), 'Source Barcode', report_data.get('source_barcode')],
            ['Notices', report_data.get('notices'), 'Element QC Barcode', report_data.get('element_qc_barcode')],
            ['Label', report_data.get('label'), 'Record Date', report_data.get('record_date')]
        ]

        audio_configuration_header = Paragraph('Audio Configuration', styleSheet['Heading3'])

        audio_configuration_table_data = [['Channel', 'Content', 'Tone', 'Peak']]

        for line in report_data.get('audio_configuration_lines'):
            line_data = [
                line.get('channel'),
                line.get('content'),
                line.get('tone'),
                line.get('peak')
            ]

            audio_configuration_table_data.append(line_data)

        element_eval_lines_table_data = [['Timecode In', 'F', 'Description', 'In Safe', 'Timecode Out', 'F', 'Code',
                                          'Scale', 'Sector/Ch', 'In Source']]

        for line in report_data.get('element_eval_lines'):
            line_data = [
                line.get('timecode_in'),
                line.get('field_in'),
                line.get('description'),
                line.get('in_safe'),
                line.get('timecode_out'),
                line.get('field_out'),
                line.get('type_code'),
                line.get('scale'),
                line.get('sector_or_channel'),
                line.get('in_source')
            ]

            element_eval_lines_table_data.append(line_data)

        general_comments_header = Paragraph('General Comments', styleSheet['Heading3'])
        general_comments = Paragraph(report_data.get('general_comments'), styleSheet['BodyText'])

        top_table = Table(top_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)
        title_table = Table(title_table_data, hAlign='LEFT')
        program_format_table = Table(program_format_table_data, hAlign='LEFT')
        video_measurements_table = Table(video_measurements_table_data, hAlign='LEFT')
        program_format_video_measurements_header_table = Table([[program_format_header, video_measurements_header]])
        program_format_video_measurements_table = Table([[program_format_table, video_measurements_table]],
                                                        hAlign='LEFT')
        element_profile_table = Table(element_profile_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)
        audio_configuration_table = Table(audio_configuration_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)
        element_eval_lines_table = Table(element_eval_lines_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)

        map(lambda x: x.setStyle([
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        ]), [top_table, title_table, program_format_table, video_measurements_table, element_profile_table,
             audio_configuration_table, element_eval_lines_table])

        elements.append(top_table)
        elements.append(title_table)
        elements.append(program_format_video_measurements_header_table)
        elements.append(program_format_video_measurements_table)
        elements.append(element_profile_header)
        elements.append(element_profile_table)
        elements.append(audio_configuration_header)
        elements.append(audio_configuration_table)

        if report_data.get('general_comments'):
            elements.append(general_comments_header)
            elements.append(general_comments)

        elements.append(element_eval_lines_table)

        doc.build(elements)


def get_test_report_data():
    report_data = {
        'client': 'Test Client',
        'status': 'Approved',
        'date': datetime.date.today().strftime('%m-%d-%Y'),
        'operator': 'Test Operator',
        'style': 'Test Style',
        'bay': 'Test Bay',
        'machine_number': 'Test Machine',
        'title': 'Some test title with a long name',
        'format': 'File format',
        'season': 'Season 1',
        'standard': 'File standard',
        'episode': 'Episode 1',
        'frame_rate': '59.94p',
        'version': 'One hour version',
        'po_number': 'A72945521',
        'file_name': 'Some_test_file.txt',
        'roll_up_blank': 'Test Roll Up Blank',
        'bars_tone': 'Test Bars/Tone',
        'black_silence_1': 'Test Black/Silence (1)',
        'slate_silence': 'Test Slate/Silence',
        'black_silence_2': 'Test Black/Silence (2)',
        'start_of_program': 'Test Start of Program',
        'end_of_program': 'Test End of Program',
        'active_video_begins': 'Test Active Video Begins',
        'active_video_ends': 'Test Active Video Ends',
        'horizontal_blanking': 'Test Horizontal Blanking',
        'luminance_peak': 'Test Luminance Peak',
        'chroma_peak': 'Test Chroma Peak',
        'head_logo': 'Test Head Logo',
        'tail_logo': 'Test Tail Logo',
        'total_runtime': 'Test Total Runtime',
        'tv_feature_trailer': 'Test TV/Feature/Trailer',
        'textless_tail': 'Test Textless @ Tail',
        'notices': 'Test Notices',
        'language': 'Test Language',
        'cc_subtitles': 'Test CC/Subtitles',
        'vitc': 'Test VITC',
        'source_barcode': 'Test Source Barcode',
        'element_qc_barcode': 'Test Element QC Barcode',
        'record_date': datetime.date.today().strftime('%m-%d-%Y'),
        'general_comments': 'This is a test.',
        'audio_configuration_lines': [
            {
                'channel': '1',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak'
            },
            {
                'channel': '2',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak'
            },
            {
                'channel': '3',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak',
            },
            {
                'channel': '4',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak',
            },
            {
                'channel': '5',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak'
            },
            {
                'channel': '6',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak',
            },
            {
                'channel': '7',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak'
            },
            {
                'channel': '8',
                'content': 'Test Content',
                'tone': 'Test Tone',
                'peak': 'Test Peak'
            }
        ],
        'element_eval_lines': [
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            },
            {
                'timecode_in': '00:00:00:00',
                'field_in': '1',
                'description': 'Test Description',
                'in_safe': 'Yes',
                'timecode_out': '00:00:10:00',
                'field_out': '1',
                'type_code': 'Video',
                'scale': 'FYI',
                'sector_or_channel': '1,2',
                'in_source': 'Approved as is'
            }
        ]
    }

    return report_data

