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


def get_top_table(element_eval_sobject):
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

    top_table = Table([top_table_header, top_table_data], hAlign='LEFT', spaceBefore=5, spaceAfter=5)

    return top_table


def get_title_table(element_eval_sobject):
    title_table_data = [
        ['Title:', element_eval_sobject.get('title'), 'Format:', element_eval_sobject.get('format')],
        ['Season:', element_eval_sobject.get('season'), 'Standard:', element_eval_sobject.get('standard')],
        ['Episode:', element_eval_sobject.get('episode'), 'Frame Rate:', element_eval_sobject.get('frame_rate')],
        ['Version:', element_eval_sobject.get('version'), 'PO #:', element_eval_sobject.get('po_number')],
        ['File Name:', element_eval_sobject.get('file_name')]
    ]

    title_table = Table(title_table_data, hAlign='LEFT', colWidths=[(1 * inch), (2 * inch), (1 * inch),
                                                                (2 * inch)])

    return title_table


def get_audio_configuration_table(element_eval_sobject):
    styleSheet = getSampleStyleSheet()

    audio_configuration_table_data = [
        [
            Paragraph('<strong>Channel</strong>', styleSheet['BodyText']),
            Paragraph('<strong>Content</strong>', styleSheet['BodyText']),
            Paragraph('<strong>Tone</strong>', styleSheet['BodyText']),
            Paragraph('<strong>Peak</strong>', styleSheet['BodyText'])
        ]
    ]

    audio_configuration_lines_search = Search('twog/audio_evaluation_line')
    audio_configuration_lines_search.add_filter('element_evaluation_code', element_eval_sobject.get_code())
    audio_configuration_lines = audio_configuration_lines_search.get_sobjects()

    for line in audio_configuration_lines:
        channel = line.get('channel')
        content = line.get('content')
        tone = line.get('tone')
        peak = line.get('peak')

        # If all the items in a row are blank, skip it
        if any([channel, content, tone, peak]):
            line_data = [channel, content, tone, peak]

            audio_configuration_table_data.append(line_data)

    audio_configuration_table = Table(audio_configuration_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)

    return audio_configuration_table


def get_element_eval_lines_table(element_eval_sobject):
    styleSheet = getSampleStyleSheet()
    styleSheet.fontSize = 10

    element_eval_lines_table_data = [['Timecode In', 'F', 'Description', 'In Safe', 'Timecode Out', 'F', 'Code',
                                      'Scale', 'Sector/Ch', 'In Source']]

    element_eval_lines_search = Search('twog/element_evaluation_line')
    element_eval_lines_search.add_filter('element_evaluation_code', element_eval_sobject.get_code())
    element_eval_lines = element_eval_lines_search.get_sobjects()

    for line in element_eval_lines:
        timecode_in = line.get('timecode_in')
        field_in = line.get('field_in')
        description = line.get('description')
        in_safe = line.get('in_safe')
        timecode_out = line.get('timecode_out')
        field_out = line.get('field_out')
        type_code = line.get('type_code')
        scale = line.get('scale')
        sector_or_channel = line.get('sector_or_channel')
        in_source = line.get('in_source')

        if any([timecode_in, field_in, description, in_safe, timecode_out, field_out, type_code, scale,
                sector_or_channel, in_source]):
            description_paragraph_style = ParagraphStyle(description)
            description_paragraph_style.fontSize = 8
            description_paragraph = Paragraph(line.get('description'), description_paragraph_style)

            line_data = [timecode_in, field_in, description_paragraph, in_safe, timecode_out, field_out, type_code,
                         scale, sector_or_channel, in_source]

            element_eval_lines_table_data.append(line_data)

    element_eval_lines_table = Table(element_eval_lines_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5,
                                     colWidths=[(.7 * inch), (.19 * inch), (inch * 2.6), (.4 * inch), (.82 * inch),
                                                (.19 * inch), (.75 * inch), (.3 * inch), (.55 * inch),
                                                (.55 * inch)])

    return element_eval_lines_table


def get_program_format_table(element_eval_sobject):
    styleSheet = getSampleStyleSheet()

    program_format_table_data = [
        [Paragraph('<strong>Roll-up (blank)</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('roll_up_blank')],
        [Paragraph('<strong>Bars/Tone</strong>', styleSheet['BodyText']), element_eval_sobject.get('bars_tone')],
        [Paragraph('<strong>Black/Silence</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('black_silence_1')],
        [Paragraph('<strong>Slate/Silence</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('slate_silence')],
        [Paragraph('<strong>Black/Silence</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('black_silence_2')],
        [Paragraph('<strong>Start of Program</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('start_of_program')],
        [Paragraph('<strong>End of Program</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('end_of_program')]
    ]

    program_format_table = Table(program_format_table_data, hAlign='LEFT', colWidths=[(1.2 * inch), (1.8 * inch)])

    return program_format_table


def get_video_measurements_table(element_eval_sobject):
    styleSheet = getSampleStyleSheet()

    video_measurements_table_data = [
        [Paragraph('<strong>Active Video Begins</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('active_video_begins')],
        [Paragraph('<strong>Active Video Ends</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('active_video_ends')],
        [Paragraph('<strong>Horizontal Blanking</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('horizontal_blanking')],
        [Paragraph('<strong>Luminance Peak</strong>', styleSheet['BodyText']),
         element_eval_sobject.get('luminance_peak')],
        [Paragraph('<strong>Chroma Peak</strong>', styleSheet['BodyText']), element_eval_sobject.get('chroma_peak')],
        [Paragraph('<strong>Head Logo</strong>', styleSheet['BodyText']), element_eval_sobject.get('head_logo')],
        [Paragraph('<strong>Tail Logo</strong>', styleSheet['BodyText']), element_eval_sobject.get('tail_logo')]
    ]

    video_measurements_table = Table(video_measurements_table_data, hAlign='LEFT', colWidths=[(1.4 * inch),
                                                                                              (1.8 * inch)])
    return video_measurements_table


def get_element_profile_table(element_eval_sobject):
    styleSheet = getSampleStyleSheet()

    element_profile_table_data = [
        [
            Paragraph('<strong>Total Runtime</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('total_runtime'),
            Paragraph('<strong>Language</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('language')
        ],
        [
            Paragraph('<strong>TV/Feature/Trailer</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('tv_feature_trailer'),
            Paragraph('<strong>(CC)/Subtitles</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('cc_subtitles')
        ],
        [
            Paragraph('<strong>Video Aspect Ratio</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('video_aspect_ratio'),
            Paragraph('<strong>VITC</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('vitc')
        ],
        [
            Paragraph('<strong>Textless @ Tail</strong>',styleSheet['BodyText']),
            element_eval_sobject.get('textless_tail'),
            Paragraph('<strong>Source Barcode</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('source_barcode')
        ],
        [
            Paragraph('<strong>Notices</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('notices'),
            Paragraph('<strong>Element QC Barcode</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('element_qc_barcode')
        ],
        [
            Paragraph('<strong>Label</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('label'),
            Paragraph('<strong>Record Date</strong>', styleSheet['BodyText']),
            element_eval_sobject.get('record_date')
        ]
    ]

    element_profile_table = Table(element_profile_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5)

    return element_profile_table


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

        program_format_header = Paragraph('Program Format', styleSheet['Heading3'])

        video_measurements_header = Paragraph('Video Measurements', styleSheet['Heading3'])

        element_profile_header = Paragraph('Element Profile', styleSheet['Heading3'])

        audio_configuration_header = Paragraph('Audio Configuration', styleSheet['Heading3'])

        general_comments_header = Paragraph('General Comments', styleSheet['Heading3'])
        general_comments = Paragraph(element_eval_sobject.get('general_comments'), styleSheet['BodyText'])

        top_table = get_top_table(element_eval_sobject)

        title_table = get_title_table(element_eval_sobject)

        program_format_table = get_program_format_table(element_eval_sobject)

        video_measurements_table = get_video_measurements_table(element_eval_sobject)

        element_profile_table = get_element_profile_table(element_eval_sobject)

        program_format_video_measurements_header_table = Table([[program_format_header, video_measurements_header]],
                                                               hAlign='LEFT')
        program_format_video_measurements_table = Table([[program_format_table, video_measurements_table]],
                                                        hAlign='LEFT')

        audio_configuration_table = get_audio_configuration_table(element_eval_sobject)

        element_eval_lines_table = get_element_eval_lines_table(element_eval_sobject)

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
