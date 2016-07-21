from pyasm.search import Search

from reportlab.lib.styles import getSampleStyleSheet
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
    styleSheet = getSampleStyleSheet()

    date = report_sobject.get('date')
    operator = report_sobject.get('operator')
    style = report_sobject.get('style')
    bay = report_sobject.get('bay')
    machine = get_name_from_code(report_sobject.get('machine_code'), 'twog/machine')

    top_table_header = []
    top_table_data = []

    for data, label in zip((date, operator, style, bay, machine), ('Date', 'Operator', 'Style', 'Bay', 'Machine')):
        if data:
            top_table_header.append(Paragraph('<strong>{0}</strong>'.format(label), styleSheet['Heading3']))
            top_table_data.append(data)

    top_table = Table([top_table_header, top_table_data], hAlign='LEFT', spaceBefore=5, spaceAfter=5)

    return top_table