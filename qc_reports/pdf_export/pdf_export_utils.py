from pyasm.search import Search

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table


def get_name_from_code(code, search_type):
    """
    Using a unique code and a search type, find an SObject and return its name

    :param code: String, Unique code for an SObject (ex: CLIENT00050)
    :param search_type: String, An SType (ex: 'twog/client')
    :return: String, Name of an SObject
    """
    search = Search(search_type)
    search.add_code_filter(code)
    sobject = search.get_sobject()

    if not sobject:
        return None

    return sobject.get('name')


def get_top_table(report_sobject):
    style_sheet = getSampleStyleSheet()

    date = report_sobject.get('date')
    operator = report_sobject.get('operator')
    style = report_sobject.get('style')
    bay = report_sobject.get('bay')
    machine = get_name_from_code(report_sobject.get('machine_code'), 'twog/machine')

    top_table_header = []
    top_table_data = []

    for data, label in zip((date, operator, style, bay, machine), ('Date', 'Operator', 'Style', 'Bay', 'Machine')):
        if data:
            top_table_header.append(Paragraph('<strong>{0}</strong>'.format(label), style_sheet['Heading3']))
            top_table_data.append(data)

    top_table = Table([top_table_header, top_table_data], hAlign='LEFT', spaceBefore=5, spaceAfter=5)

    return top_table


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        self.drawRightString(200*mm, 20*mm, "Page %d of %d" % (self._pageNumber, page_count))
