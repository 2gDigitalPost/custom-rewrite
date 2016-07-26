import os
from ConfigParser import SafeConfigParser

from pyasm.command import Command
from pyasm.search import Search

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.platypus.flowables import HRFlowable

from pdf_export_utils import get_name_from_code, get_top_table


def get_title_table(prequal_eval_sobject):
    title_table_data = [
        ['Title:', prequal_eval_sobject.get('title'), 'Format:', prequal_eval_sobject.get('format')],
        ['Season:', prequal_eval_sobject.get('season'), 'Standard:', prequal_eval_sobject.get('standard')],
        ['Episode:', prequal_eval_sobject.get('episode'),
         'Frame Rate:', get_name_from_code(prequal_eval_sobject.get('frame_rate_code'), 'twog/frame_rate')],
        ['Version:', prequal_eval_sobject.get('version'), 'PO #:', prequal_eval_sobject.get('po_number')],
        ['Video Aspect Ratio:', prequal_eval_sobject.get('video_aspect_ratio')]
    ]

    title_table = Table(title_table_data, hAlign='LEFT', colWidths=[(1 * inch), (2 * inch), (1 * inch),
                                                                (2 * inch)])

    return title_table


def get_prequal_eval_lines_table(prequal_eval_sobject):
    prequal_eval_lines_search = Search('twog/prequal_evaluation_line')
    prequal_eval_lines_search.add_filter('prequal_evaluation_code', prequal_eval_sobject.get_code())
    prequal_eval_lines = prequal_eval_lines_search.get_sobjects()

    # If no prequal eval lines exist for this report, return None so that the PDF won't display a table
    if not prequal_eval_lines:
        return None

    style_sheet = getSampleStyleSheet()
    style_sheet.font_size = 10

    prequal_eval_lines_table_data = [['Timecode', 'F', 'Description', 'Code', 'Scale', 'Sector/Ch', 'In Source']]

    lines_with_values = []
    lines_without_values = []

    for line in prequal_eval_lines:
        if line.get_value('timecode'):
            lines_with_values.append(line)
        else:
            lines_without_values.append(line)

    prequal_eval_lines = sorted(lines_with_values, key=lambda x: x.get_value('timecode'))
    prequal_eval_lines.extend(lines_without_values)

    for line in prequal_eval_lines:
        timecode = line.get('timecode')
        field = line.get('field')
        prequal_line_description = line.get('prequal_line_description')
        type_code = line.get('type_code')
        scale = line.get('scale')
        sector_or_channel = line.get('sector_or_channel')
        in_source = line.get('in_source')

        if any([timecode, field, prequal_line_description, type_code, scale, sector_or_channel, in_source]):
            description_paragraph_style = ParagraphStyle(prequal_line_description)
            description_paragraph_style.fontSize = 8
            description_paragraph = Paragraph(line.get('description'), description_paragraph_style)

            line_data = [timecode, field, description_paragraph, type_code, scale, sector_or_channel, in_source]

            prequal_eval_lines_table_data.append(line_data)

    prequal_eval_lines_table = Table(prequal_eval_lines_table_data, hAlign='LEFT', spaceBefore=5, spaceAfter=5,
                                     colWidths=[(.7 * inch), (.19 * inch), (inch * 2.6), (.4 * inch), (.82 * inch),
                                                (.19 * inch), (.75 * inch), (.3 * inch), (.55 * inch),
                                                (.55 * inch)])

    prequal_eval_lines_table.setStyle([('BOX', (0, 0), (-1, -1), 0.2, colors.black),
                                       ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black),
                                       ('FONTSIZE', (0, 0), (-1, -1), 8),
                                       ('LEFTPADDING', (0, 0), (-1, -1), 1),
                                       ('RIGHTPADDING', (0, 0), (-1, -1), 1)])

    return prequal_eval_lines_table


def get_element_eval_lines_table(element_eval_sobject):
    element_eval_lines_search = Search('twog/element_evaluation_line')
    element_eval_lines_search.add_filter('element_evaluation_code', element_eval_sobject.get_code())
    element_eval_lines = element_eval_lines_search.get_sobjects()

    # If no element eval lines exist for this element evaluation, return None so that the PDF won't display a table
    if not element_eval_lines:
        return None

    styleSheet = getSampleStyleSheet()
    styleSheet.fontSize = 10

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

    element_eval_lines_table.setStyle([('BOX', (0, 0), (-1, -1), 0.2, colors.black),
                                       ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black),
                                       ('FONTSIZE', (0, 0), (-1, -1), 8),
                                       ('LEFTPADDING', (0, 0), (-1, -1), 1),
                                       ('RIGHTPADDING', (0, 0), (-1, -1), 1)])

    return element_eval_lines_table


class ExportPreqaulEvalCommand(Command):
    def execute(self):
        report_search_key = self.kwargs.get('report_search_key')

        if report_search_key:
            self.export_pdf(Search.get_by_search_key(report_search_key))

    @staticmethod
    def export_pdf(prequal_eval_sobject):
        parser = SafeConfigParser()
        config_path = os.path.abspath(os.path.dirname(__file__))
        parser.read(config_path + '/config.ini')

        file_name = prequal_eval_sobject.get('name') + '.pdf'
        save_location = parser.get('save', 'directory')

        saved_file_path = os.path.join(save_location, file_name)

        doc = SimpleDocTemplate(saved_file_path, pagesize=letter)

        elements = []

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

        approved_rejected_status = prequal_eval_sobject.get('status')
        approved_rejected_table_data = [[Paragraph('Status: <strong>{0}</strong>'.format(approved_rejected_status),
                                                   styleSheet["BodyText"])]]

        approved_rejected_table = Table(approved_rejected_table_data)

        client_name = get_name_from_code(prequal_eval_sobject.get('client_code'), 'twog/client')

        # If a client name is not specified, just put 'Element Evaluation' at the top of the report in its place
        if not client_name:
            client_name = "Element Evaluation"

        P = Paragraph('<strong>{0}</strong>'.format(client_name), styleSheet["Heading2"])

        header_table = Table([[I, address_table, P, approved_rejected_table]])

        elements.append(header_table)

        general_comments_header = Paragraph('General Comments', styleSheet['Heading3'])
        general_comments = Paragraph(prequal_eval_sobject.get('general_comments'), styleSheet['BodyText'])

        top_table = get_top_table(prequal_eval_sobject)

        title_table = get_title_table(prequal_eval_sobject)

        prequal_eval_lines_table = get_prequal_eval_lines_table(prequal_eval_sobject)
