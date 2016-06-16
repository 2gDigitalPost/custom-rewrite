from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table

import datetime


def main(report_data):
    doc = SimpleDocTemplate("Simple_table.pdf", pagesize=letter)

    elements = []

    styleSheet = getSampleStyleSheet()

    I = Image('2GLogo_small4.png')
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch

    top_address_paragraph = Paragraph('<strong>2G Digital Post, Inc.</strong>', styleSheet["BodyText"])

    address_table_data = [
        [top_address_paragraph],
        ['280 E.Magnolia Blvd.'],
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

    P = Paragraph('<strong>{0}</strong>'.format(report_data.get('client')), styleSheet["BodyText"])

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

    program_format_table_data = [
        ['Program Format'],
        ['Roll-up (blank)', report_data.get('roll_up_blank')],
        ['Bars/Tone', report_data.get('bars_tone')],
        ['Black/Silence', report_data.get('black_silence_1')],
        ['Slate/Silence', report_data.get('slate_silence')],
        ['Black/Silence', report_data.get('black_silence_2')],
        ['Start of Program', report_data.get('start_of_program')],
        ['End of Program', report_data.get('end_of_program')]
    ]

    video_measurements_table_data = [
        ['Video Measurements'],
        ['Active Video Begins', report_data.get('active_video_begins')],
        ['Active Video Ends', report_data.get('active_video_ends')],
        ['Horizontal Blanking', report_data.get('horizontal_blanking')],
        ['Luminance Peak', report_data.get('luminance_peak')],
        ['Chroma Peak', report_data.get('chroma_peak')],
        ['Head Logo', report_data.get('head_logo')],
        ['Tail Logo', report_data.get('tail_logo')]
    ]

    element_profile_table_data = [
        ['Element Profile'],
        ['Total Runtime', report_data.get('total_runtime'), 'Language', report_data.get('language')],
        ['TV/Feature/Trailer', report_data.get('tv_feature_trailer'), '(CC)/Subtitles', report_data.get('cc_subtitles')],
        ['Video Aspect Ratio', report_data.get('video_aspect_ratio'), 'VITC', report_data.get('vitc')],
        ['Textless @ Tail', report_data.get('textless_tail'), 'Source Barcode', report_data.get('source_barcode')],
        ['Notices', report_data.get('notices'), 'Element QC Barcode', report_data.get('element_qc_barcode')],
        ['Label', report_data.get('label'), 'Record Date', report_data.get('record_date')]
    ]

    audio_configuration_table_data = [['Audio Configuration'], ['Channel', 'Content', 'Tone', 'Peak']]

    for line in range(report_data.get('audio_configuration_lines')):
        line_data = []
        line_data.append(report_data.get('audio_configuration_lines_values').get('channel-{}'.format(line)))
        line_data.append(report_data.get('audio_configuration_lines_values').get('content-{}'.format(line)))
        line_data.append(report_data.get('audio_configuration_lines_values').get('tone-{}'.format(line)))
        line_data.append(report_data.get('audio_configuration_lines_values').get('peak-{}'.format(line)))

        audio_configuration_table_data.append(line_data)

    top_table = Table(top_table_data)
    title_table = Table(title_table_data)
    program_format_table = Table(program_format_table_data)
    video_measurements_table = Table(video_measurements_table_data)
    program_format_video_measurements_table = Table([[program_format_table, video_measurements_table]])
    element_profile_table = Table(element_profile_table_data)
    audio_configuration_table = Table(audio_configuration_table_data)

    map(lambda x: x.setStyle([
        ('BOX', (0,0), (-1,-1), 0.25, colors.black), ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
    ]), [top_table, title_table, program_format_table, video_measurements_table, element_profile_table,
         audio_configuration_table])

    elements.append(top_table)
    elements.append(title_table)
    elements.append(program_format_video_measurements_table)
    elements.append(element_profile_table)
    elements.append(audio_configuration_table)

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
        'audio_configuration_lines': 8,
        'audio_configuration_lines_values': {
            'channel-0': '1',
            'content-0': 'Test Content',
            'tone-0': 'Test Tone',
            'peak-0': 'Test Peak',
            'channel-1': '2',
            'content-1': 'Test Content',
            'tone-1': 'Test Tone',
            'peak-1': 'Test Peak',
            'channel-2': '3',
            'content-2': 'Test Content',
            'tone-2': 'Test Tone',
            'peak-2': 'Test Peak',
            'channel-3': '4',
            'content-3': 'Test Content',
            'tone-3': 'Test Tone',
            'peak-3': 'Test Peak',
            'channel-4': '5',
            'content-4': 'Test Content',
            'tone-4': 'Test Tone',
            'peak-4': 'Test Peak',
            'channel-5': '6',
            'content-5': 'Test Content',
            'tone-5': 'Test Tone',
            'peak-5': 'Test Peak',
            'channel-6': '7',
            'content-6': 'Test Content',
            'tone-6': 'Test Tone',
            'peak-6': 'Test Peak',
            'channel-7': '8',
            'content-7': 'Test Content',
            'tone-7': 'Test Tone',
            'peak-7': 'Test Peak',
        }
    }

    return report_data


if __name__ == '__main__':
    main(get_test_report_data())
