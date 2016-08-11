import os
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


class ExportMetaDataReportCommand(Command):
    def execute(self):
        report_search_key = self.kwargs.get('report_search_key')

        if report_search_key:
            self.export_pdf(Search.get_by_search_key(report_search_key))

    @staticmethod
    def export_pdf(metadata_report_sobject):
        parser = SafeConfigParser()
        config_path = os.path.abspath(os.path.dirname(__file__))
        parser.read(config_path + '/config.ini')

        file_name = metadata_report_sobject.get('name') + '.pdf'
        save_location = parser.get('save', 'metadata_directory')

        saved_file_path = os.path.join(save_location, file_name)

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

        P = Paragraph('<strong>Metadata Report</strong>', styleSheet["Heading2"])

        header_table = Table([[I, address_table, P]])

        title_table = get_title_table(metadata_report_sobject)

        elements.append(header_table)
        elements.append(title_table)

        doc = SimpleDocTemplate(saved_file_path)

        doc.build(elements, canvasmaker=NumberedCanvas)
