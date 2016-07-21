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


class ExportElementEvalCommand(Command):
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
