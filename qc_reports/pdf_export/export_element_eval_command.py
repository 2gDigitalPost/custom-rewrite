import os
from ConfigParser import SafeConfigParser

from pyasm.command import Command
from pyasm.search import Search

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.platypus.flowables import HRFlowable

from pdf_export_utils import get_name_from_code, get_top_table, NumberedCanvas


def get_paragraph(text, style_sheet_type='BodyText'):
    style_sheet = getSampleStyleSheet()

    return Paragraph(text, style_sheet[style_sheet_type])


def get_title_table(element_eval_sobject):
    title_table_data = [
        [
            'Title:', get_paragraph(element_eval_sobject.get('title')),
            'Format:', get_paragraph(element_eval_sobject.get('format'))
        ],
        [
            'Season:', get_paragraph(element_eval_sobject.get('season')),
            'Standard:', get_paragraph(element_eval_sobject.get('standard'))],
        [
            'Episode:', get_paragraph(element_eval_sobject.get('episode')),
            'Frame Rate:', get_paragraph(get_name_from_code(element_eval_sobject.get('frame_rate_code'),
                                                            'twog/frame_rate'))
        ],
        [
            'Version:', get_paragraph(element_eval_sobject.get('version')),
            'PO #:', get_paragraph(element_eval_sobject.get('po_number'))
        ],
        [
            'File Name:', element_eval_sobject.get('file_name')
        ]
    ]

    title_table = Table(title_table_data, hAlign='LEFT', colWidths=[(1 * inch), (2 * inch), (1 * inch), (2 * inch)])

    return title_table


def get_audio_configuration_table(element_eval_sobject):
    audio_configuration_lines_search = Search('twog/audio_evaluation_line')
    audio_configuration_lines_search.add_filter('element_evaluation_code', element_eval_sobject.get_code())
    audio_configuration_lines = audio_configuration_lines_search.get_sobjects()

    # If no audio configuration lines exist for this element evaluation, return None so that the PDF won't display
    # a table
    if not audio_configuration_lines:
        return None

    audio_configuration_table_data = [
        [
            get_paragraph('<strong>Channel</strong>'),
            get_paragraph('<strong>Content</strong>'),
            get_paragraph('<strong>Tone</strong>'),
            get_paragraph('<strong>Peak</strong>')
        ]
    ]

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


def translate_in_source(text):
    """
    Take the value of the in_source field and convert it to readable text. Remove underscores and replace with spaces,
    and capitalize the first word

    :param text: String
    :return: String
    """

    words = text.split('_')
    translated_text = ' '.join(words)
    translated_text = translated_text.capitalize()

    return translated_text


def get_element_eval_lines_table(element_eval_sobject):
    element_eval_lines_search = Search('twog/element_evaluation_line')
    element_eval_lines_search.add_filter('element_evaluation_code', element_eval_sobject.get_code())
    element_eval_lines = element_eval_lines_search.get_sobjects()

    # If no element eval lines exist for this element evaluation, return None so that the PDF won't display a table
    if not element_eval_lines:
        return None

    element_eval_lines_table_data = [['Timecode In', 'F', 'Description', 'In Safe', 'Timecode Out', 'F', 'Code',
                                      'Scale', 'Sector/Ch', 'In Source']]

    lines_with_values = []
    lines_without_values = []

    for line in element_eval_lines:
        if line.get_value('timecode_in'):
            lines_with_values.append(line)
        else:
            lines_without_values.append(line)

    element_eval_lines = sorted(lines_with_values, key=lambda x: x.get_value('timecode_in'))
    element_eval_lines.extend(lines_without_values)

    for line in element_eval_lines:
        timecode_in = line.get('timecode_in')
        field_in = line.get('field_in')
        description = line.get('description')
        in_safe = line.get('in_safe')

        if in_safe == 'True':
            in_safe = 'Yes'
        elif in_safe == 'False':
            in_safe = 'No'
        else:
            in_safe = ''

        timecode_out = line.get('timecode_out')
        field_out = line.get('field_out')
        type_code = line.get('type_code').capitalize()
        scale = line.get('scale').upper()
        sector_or_channel = line.get('sector_or_channel')
        in_source = translate_in_source(line.get('in_source'))

        if any([timecode_in, field_in, description, in_safe, timecode_out, field_out, type_code, scale,
                sector_or_channel, in_source]):
            line_data = []

            for attribute in [timecode_in, field_in, description, in_safe, timecode_out, field_out, type_code, scale,
                              sector_or_channel, in_source]:
                paragraph_style = ParagraphStyle(attribute)
                paragraph_style.fontSize = 8

                if scale == '3':
                    paragraph = Paragraph('<b>' + attribute + '</b>', paragraph_style)
                else:
                    paragraph = Paragraph(attribute, paragraph_style)

                line_data.append(paragraph)

            element_eval_lines_table_data.append(line_data)

    element_eval_lines_table = Table(element_eval_lines_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5,
                                     colWidths=[(.7 * inch), (.19 * inch), (inch * 3.3), (.4 * inch), (.82 * inch),
                                                (.19 * inch), (.5 * inch), (.3 * inch), (.55 * inch),
                                                (.75 * inch)],
                                     repeatRows=1)

    element_eval_lines_table.setStyle([('BOX', (0, 0), (-1, -1), 0.2, colors.black),
                                       ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black),
                                       ('FONTSIZE', (0, 0), (-1, -1), 8),
                                       ('LEFTPADDING', (0, 0), (-1, -1), 1),
                                       ('RIGHTPADDING', (0, 0), (-1, -1), 1)])

    return element_eval_lines_table


def get_program_format_table(element_eval_sobject):
    program_format_table_data = [
        [get_paragraph('<strong>Roll-up (blank)</strong>'),
         element_eval_sobject.get('roll_up_blank')],
        [get_paragraph('<strong>Bars/Tone</strong>'), element_eval_sobject.get('bars_tone')],
        [get_paragraph('<strong>Black/Silence</strong>'),
         element_eval_sobject.get('black_silence_1')],
        [get_paragraph('<strong>Slate/Silence</strong>'),
         element_eval_sobject.get('slate_silence')],
        [get_paragraph('<strong>Black/Silence</strong>'),
         element_eval_sobject.get('black_silence_2')],
        [get_paragraph('<strong>Start of Program</strong>'),
         element_eval_sobject.get('start_of_program')],
        [get_paragraph('<strong>End of Program</strong>'),
         element_eval_sobject.get('end_of_program')]
    ]

    program_format_table = Table(program_format_table_data, hAlign='LEFT', colWidths=[(1.2 * inch), (1.8 * inch)])

    return program_format_table


def get_video_measurements_table(element_eval_sobject):
    video_measurements_table_data = [
        [get_paragraph('<strong>Active Video Begins</strong>'), element_eval_sobject.get('active_video_begins')],
        [get_paragraph('<strong>Active Video Ends</strong>'), element_eval_sobject.get('active_video_ends')],
        [get_paragraph('<strong>Horizontal Blanking</strong>'), element_eval_sobject.get('horizontal_blanking')],
        [get_paragraph('<strong>Luminance Peak</strong>'), element_eval_sobject.get('luminance_peak')],
        [get_paragraph('<strong>Chroma Peak</strong>'), element_eval_sobject.get('chroma_peak')],
        [get_paragraph('<strong>Head Logo</strong>'), get_paragraph(element_eval_sobject.get('head_logo'))],
        [get_paragraph('<strong>Tail Logo</strong>'), get_paragraph(element_eval_sobject.get('tail_logo'))]
    ]

    video_measurements_table = Table(video_measurements_table_data, hAlign='LEFT', colWidths=[(1.4 * inch),
                                                                                              (1.8 * inch)])
    return video_measurements_table


def get_element_profile_table(element_eval_sobject):
    element_profile_table_data = [
        [
            get_paragraph('<strong>Total Runtime</strong>'), element_eval_sobject.get('total_runtime'),
            get_paragraph('<strong>Language</strong>'), get_name_from_code(element_eval_sobject.get('language_code'),
                                                                           'twog/language')
        ],
        [
            get_paragraph('<strong>TV/Feature/Trailer</strong>'), element_eval_sobject.get('tv_feature_trailer'),
            get_paragraph('<strong>(CC)/Subtitles</strong>'), element_eval_sobject.get('cc_subtitles')
        ],
        [
            get_paragraph('<strong>Video Aspect Ratio</strong>'), element_eval_sobject.get('video_aspect_ratio'),
            get_paragraph('<strong>VITC</strong>'), element_eval_sobject.get('vitc')
        ],
        [
            get_paragraph('<strong>Textless @ Tail</strong>'), element_eval_sobject.get('textless_tail'),
            get_paragraph('<strong>Source Barcode</strong>'), element_eval_sobject.get('source_barcode')
        ],
        [
            get_paragraph('<strong>Notices</strong>'), element_eval_sobject.get('notices'),
            get_paragraph('<strong>Element QC Barcode</strong>'), element_eval_sobject.get('element_qc_barcode')
        ],
        [
            get_paragraph('<strong>Label</strong>'), element_eval_sobject.get('label'),
            get_paragraph('<strong>Record Date</strong>'), element_eval_sobject.get('record_date')
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
        parser = SafeConfigParser()
        config_path = os.path.abspath(os.path.dirname(__file__))
        parser.read(config_path + '/config.ini')

        file_name = element_eval_sobject.get('name') + '.pdf'
        save_location = parser.get('save', 'element_directory')

        saved_file_path = os.path.join(save_location, file_name)

        elements = []

        image = Image(os.path.dirname(os.path.realpath(__file__)) + '/2g_logo.png')
        image.drawHeight = 1.25 * inch * image.drawHeight / image.drawWidth
        image.drawWidth = 1.25 * inch

        top_address_paragraph = get_paragraph('<strong>2G Digital Post, Inc.</strong>')

        address_table_data = [
            [top_address_paragraph],
            ['280 E. Magnolia Blvd.'],
            ['Burbank, CA 91502'],
            ['310 - 840 - 0600'],
            ['www.2gdigitalpost.com']
        ]

        address_table = Table(address_table_data)

        approved_rejected_status = element_eval_sobject.get('status')
        approved_rejected_table_data = [
            [get_paragraph('Status: <strong>{0}</strong>'.format(approved_rejected_status))]]

        approved_rejected_table = Table(approved_rejected_table_data)

        client_name = get_name_from_code(element_eval_sobject.get('client_code'), 'twog/client')

        # If a client name is not specified, just put 'Element Evaluation' at the top of the report in its place
        if not client_name:
            client_name = "Element Evaluation"

        client_paragraph = get_paragraph('<strong>{0}</strong>'.format(client_name), "Heading2")

        header_table = Table([[image, address_table, client_paragraph, approved_rejected_table]])

        elements.append(header_table)

        program_format_header = get_paragraph('Program Format', 'Heading3')

        video_measurements_header = get_paragraph('Video Measurements', 'Heading3')

        element_profile_header = get_paragraph('Element Profile', 'Heading3')

        audio_configuration_header = get_paragraph('Audio Configuration', 'Heading3')

        general_comments_header = get_paragraph('General Comments', 'Heading3')
        general_comments = get_paragraph(element_eval_sobject.get('general_comments'))

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

        # Now apply some styling to all the tables (except the bottom one, which is styled separately since it needs
        # special styling to fit on the page). Only include audio_configuration_table if it exists
        tables_to_style = [program_format_table, video_measurements_table, element_profile_table]

        if audio_configuration_table:
            tables_to_style.append(audio_configuration_table)

        map(lambda x: x.setStyle([
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        ]), tables_to_style)

        hr_flowable = HRFlowable(color=colors.gray, width='100%')

        # Add the segments to the report, regardless of whether or not there is data in the tables
        elements.append(top_table)
        elements.append(title_table)
        elements.append(hr_flowable)
        elements.append(program_format_video_measurements_header_table)
        elements.append(program_format_video_measurements_table)
        elements.append(element_profile_header)
        elements.append(element_profile_table)

        # Only include the next few segments if they have data
        if audio_configuration_table:
            elements.append(audio_configuration_header)
            elements.append(audio_configuration_table)

        if element_eval_sobject.get('general_comments'):
            elements.append(general_comments_header)
            elements.append(general_comments)

        if element_eval_lines_table:
            elements.append(element_eval_lines_table)

        doc = SimpleDocTemplate(saved_file_path, leftMargin=10, rightMargin=10, topMargin=30, bottomMargin=40)

        doc.build(elements, canvasmaker=NumberedCanvas)
