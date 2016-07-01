import datetime
import os
from reportlab.platypus.flowables import HRFlowable

from pyasm.command import Command
from pyasm.search import Search

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table


def get_top_table_data(element_eval_sobject):
    styleSheet = getSampleStyleSheet()

    date = element_eval_sobject.get('date')
    operator = element_eval_sobject.get('operator')
    style = element_eval_sobject.get('style')
    bay = element_eval_sobject.get('bay')
    machine = element_eval_sobject.get('machine')

    top_table_header = []
    top_table_data = []

    for data, label in zip((date, operator, style, bay, machine), ('Date', 'Operator', 'Style', 'Bay', 'Machine')):
        if data:
            top_table_header.append(Paragraph('<strong>{0}</strong>'.format(label), styleSheet['Heading3']))
            top_table_data.append(data)

    return [top_table_header, top_table_data]


def get_title_table_data(element_eval_sobject):
    title_table_data = [
        ['Title:', element_eval_sobject.get('title'), 'Format:', element_eval_sobject.get('format')],
        ['Season:', element_eval_sobject.get('season'), 'Standard:', element_eval_sobject.get('standard')],
        ['Episode:', element_eval_sobject.get('episode'), 'Frame Rate:', element_eval_sobject.get('frame_rate')],
        ['Version:', element_eval_sobject.get('version'), 'PO #:', element_eval_sobject.get('po_number')],
        ['File Name:', element_eval_sobject.get('file_name')]
    ]

    return title_table_data


def get_audio_configuration_lines(element_eval_code):
    audio_configuration_table_data = [['Channel', 'Content', 'Tone', 'Peak']]

    audio_configuration_lines_search = Search('twog/audio_evaluation_line')
    audio_configuration_lines_search.add_filter('element_evaluation_code', element_eval_code)
    audio_configuration_lines = audio_configuration_lines_search.get_sobjects()

    for line in audio_configuration_lines:
        line_data = [
            line.get('channel'),
            line.get('content'),
            line.get('tone'),
            line.get('peak')
        ]

        audio_configuration_table_data.append(line_data)

    return audio_configuration_table_data


def get_element_eval_lines(element_eval_code):
    styleSheet = getSampleStyleSheet()
    styleSheet.fontSize = 10

    element_eval_lines_table_data = [['Timecode In', 'F', 'Description', 'In Safe', 'Timecode Out', 'F', 'Code',
                                      'Scale', 'Sector/Ch', 'In Source']]

    element_eval_lines_search = Search('twog/element_evaluation_line')
    element_eval_lines_search.add_filter('element_evaluation_code', element_eval_code)
    element_eval_lines = element_eval_lines_search.get_sobjects()

    for line in element_eval_lines:
        description_paragraph_style = ParagraphStyle('description')
        description_paragraph_style.fontSize = 8

        description_paragraph = Paragraph(line.get('description'), description_paragraph_style)

        line_data = [
            line.get('timecode_in'),
            line.get('field_in'),
            description_paragraph,
            line.get('in_safe'),
            line.get('timecode_out'),
            line.get('field_out'),
            line.get('type_code'),
            line.get('scale'),
            line.get('sector_or_channel'),
            line.get('in_source')
        ]

        element_eval_lines_table_data.append(line_data)

    return element_eval_lines_table_data


class ExportElementEvalCommand(Command):
    def execute(self):
        report_search_key = self.kwargs.get('report_search_key')

        if report_search_key:
            self.export_pdf(Search.get_by_search_key(report_search_key))

    @staticmethod
    def export_pdf(element_eval_sobject):
        print(element_eval_sobject)
        file_name = element_eval_sobject.get('name') + datetime.datetime.now().strftime('-%m%d%y-%H%M%S') + '.pdf'
        save_location = '/var/www/html/element_evaluations'

        saved_file_path = os.path.join(save_location, file_name)

        doc = SimpleDocTemplate(saved_file_path, pagesize=letter)

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

        P = Paragraph('<strong>{0}</strong>'.format(element_eval_sobject.get('client')), styleSheet["Heading2"])

        header_table = Table([[I, address_table, P, approved_rejected_table]])

        elements.append(header_table)

        top_table_data = get_top_table_data(element_eval_sobject)
        title_table_data = get_title_table_data(element_eval_sobject)

        program_format_header = Paragraph('Program Format', styleSheet['Heading3'])

        program_format_table_data = [
            ['Roll-up (blank)', element_eval_sobject.get('roll_up_blank')],
            ['Bars/Tone', element_eval_sobject.get('bars_tone')],
            ['Black/Silence', element_eval_sobject.get('black_silence_1')],
            ['Slate/Silence', element_eval_sobject.get('slate_silence')],
            ['Black/Silence', element_eval_sobject.get('black_silence_2')],
            ['Start of Program', element_eval_sobject.get('start_of_program')],
            ['End of Program', element_eval_sobject.get('end_of_program')]
        ]

        video_measurements_header = Paragraph('Video Measurements', styleSheet['Heading3'])

        video_measurements_table_data = [
            ['Active Video Begins', element_eval_sobject.get('active_video_begins')],
            ['Active Video Ends', element_eval_sobject.get('active_video_ends')],
            ['Horizontal Blanking', element_eval_sobject.get('horizontal_blanking')],
            ['Luminance Peak', element_eval_sobject.get('luminance_peak')],
            ['Chroma Peak', element_eval_sobject.get('chroma_peak')],
            ['Head Logo', element_eval_sobject.get('head_logo')],
            ['Tail Logo', element_eval_sobject.get('tail_logo')]
        ]

        element_profile_header = Paragraph('Element Profile', styleSheet['Heading3'])

        element_profile_table_data = [
            ['Total Runtime', element_eval_sobject.get('total_runtime'), 'Language', element_eval_sobject.get('language')],
            ['TV/Feature/Trailer', element_eval_sobject.get('tv_feature_trailer'), '(CC)/Subtitles',
             element_eval_sobject.get('cc_subtitles')],
            ['Video Aspect Ratio', element_eval_sobject.get('video_aspect_ratio'), 'VITC', element_eval_sobject.get('vitc')],
            ['Textless @ Tail', element_eval_sobject.get('textless_tail'), 'Source Barcode', element_eval_sobject.get('source_barcode')],
            ['Notices', element_eval_sobject.get('notices'), 'Element QC Barcode', element_eval_sobject.get('element_qc_barcode')],
            ['Label', element_eval_sobject.get('label'), 'Record Date', element_eval_sobject.get('record_date')]
        ]

        audio_configuration_header = Paragraph('Audio Configuration', styleSheet['Heading3'])

        audio_configuration_table_data = get_audio_configuration_lines(element_eval_sobject.get_code())

        element_eval_lines_table_data = get_element_eval_lines(element_eval_sobject.get_code())

        general_comments_header = Paragraph('General Comments', styleSheet['Heading3'])
        general_comments = Paragraph(element_eval_sobject.get('general_comments'), styleSheet['BodyText'])

        top_table = Table(top_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)

        title_table = Table(title_table_data, hAlign='LEFT', colWidths=[(1 * inch), (2 * inch), (1 * inch),
                                                                        (2 * inch)])

        program_format_table = Table(program_format_table_data, hAlign='LEFT')
        video_measurements_table = Table(video_measurements_table_data, hAlign='LEFT')
        program_format_video_measurements_header_table = Table([[program_format_header, video_measurements_header]])
        program_format_video_measurements_table = Table([[program_format_table, video_measurements_table]],
                                                        hAlign='LEFT')
        element_profile_table = Table(element_profile_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)
        audio_configuration_table = Table(audio_configuration_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)
        element_eval_lines_table = Table(element_eval_lines_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5,
                                         colWidths=[(.7 * inch), (.19 * inch), (inch * 2.6), (.4 * inch), (.82 * inch),
                                                    (.19 * inch), (.75 * inch), (.3 * inch), (.55 * inch),
                                                    (.55 * inch)])
        element_eval_lines_table.setStyle([('BOX', (0, 0), (-1, -1), 0.2, colors.black),
                                           ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black),
                                           ('FONTSIZE', (0, 0), (-1, -1), 8),
                                           ('LEFTPADDING', (0, 0), (-1, -1), 1),
                                           ('RIGHTPADDING', (0, 0), (-1, -1), 1)])

        map(lambda x: x.setStyle([
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        ]), [program_format_table, video_measurements_table, element_profile_table,
             audio_configuration_table])

        hrFlowable = HRFlowable(color=colors.gray, width='100%')

        elements.append(top_table)
        elements.append(title_table)
        elements.append(hrFlowable)
        elements.append(program_format_video_measurements_header_table)
        elements.append(program_format_video_measurements_table)
        elements.append(element_profile_header)
        elements.append(element_profile_table)
        elements.append(audio_configuration_header)
        elements.append(audio_configuration_table)

        if element_eval_sobject.get('general_comments'):
            elements.append(general_comments_header)
            elements.append(general_comments)

        elements.append(element_eval_lines_table)

        doc.build(elements)


def get_test_element_eval_sobject():
    element_eval_sobject = {
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

    return element_eval_sobject

