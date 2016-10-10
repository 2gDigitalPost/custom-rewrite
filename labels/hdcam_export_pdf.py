import os
from ConfigParser import SafeConfigParser

from pyasm.command import Command
from pyasm.search import Search

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.platypus.flowables import HRFlowable

from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.lib.units import cm, inch


def main():
    canvas = reportlab_canvas.Canvas("hdcam.pdf")

    channel_one_text = 'Latin American Spanish Left Total'
    channel_two_text = 'Latin American Spanish Right Total'
    channel_three_text = 'English Left Total'
    channel_four_text = 'English Right Total'
    channel_five_text = 'Latin American Spanish 5.1 Left'
    channel_six_text = 'Latin American Spanish 5.1 Right'
    channel_seven_text = 'Latin American Spanish 5.1 Center'
    channel_eight_text = 'Latin American Spanish 5.1 Subwoofer/Boom'
    channel_nine_text = 'Latin American Spanish 5.1 Left Surround'
    channel_ten_text = 'Latin American Spanish 5.1 Right Surround'
    channel_eleven_text = 'MOS'
    channel_twelve_text = 'MOS'

    channels = [channel_one_text, channel_two_text, channel_three_text, channel_four_text, channel_five_text,
                channel_six_text, channel_seven_text, channel_eight_text, channel_nine_text, channel_ten_text,
                channel_eleven_text, channel_twelve_text]

    channel_pairs = [
        (channels[0], channels[6]),
        (channels[1], channels[7]),
        (channels[2], channels[8]),
        (channels[3], channels[9]),
        (channels[4], channels[10]),
        (channels[5], channels[11]),
    ]

    canvas.saveState()
    draw_section_one(canvas, channel_pairs)
    canvas.restoreState()





    canvas.saveState()
    canvas.setFont("Helvetica-Oblique", 8)
    canvas.translate(6.5 * inch, 8.9 * inch)
    canvas.rotate(90)

    canvas.drawString(0, 2.6 * inch, "Sony")
    canvas.setFont("Helvetica", 10)
    canvas.drawString(0, 2.4 * inch, "That's My Boy")

    canvas.setFont("Helvetica", 5)
    canvas.drawString(0, 2.25 * inch, "Version: Theatrical")
    canvas.drawString(0, 2.16 * inch, "Latin American Spanish Foreign Language Master")
    canvas.drawString(0, 2.07 * inch, "Aspect Ratio: 16x9 1.78 Full Frame")
    canvas.drawString(0, 1.98 * inch, "Textless: Textless at Tail")

    current_height_one = 0
    current_height_two = 0


    paragraph_style = ParagraphStyle('paraStyle')
    paragraph_style.fontSize = 6
    paragraph_style.leading = 8

    for iterator, channel_pair in enumerate([(channel_one_text, channel_seven_text), (channel_two_text, channel_eight_text),
                         (channel_three_text, channel_nine_text), (channel_four_text, channel_ten_text),
                         (channel_five_text, channel_eleven_text), (channel_six_text, channel_twelve_text)]):
        paragraph1 = Paragraph('CH{0:02d}: {1}'.format(iterator + 1, channel_pair[0]), paragraph_style)
        width1, height1 = paragraph1.wrap(1.2 * inch, 50)

        paragraph2 = Paragraph('CH{0:02d}: {1}'.format(iterator + 7, channel_pair[1]), paragraph_style)
        width2, height2 = paragraph2.wrap(1.2 * inch, 50)

        current_height_one += height1
        current_height_two += height2

        paragraph1.drawOn(canvas, 0, 1.7 * inch - current_height_one)
        paragraph2.drawOn(canvas, 1.25 * inch, 1.7 * inch - current_height_two)

    canvas.restoreState()






    canvas.saveState()

    canvas.translate(.25 * inch, 7.375 * inch)

    image = Image(os.path.dirname(os.path.realpath(__file__)) + '/2g_logo.png')
    image.drawHeight = .5 * inch * image.drawHeight / image.drawWidth
    image.drawWidth = .5 * inch

    image.drawOn(canvas, 0, inch * .43)

    canvas.setFont("Helvetica", 5)
    canvas.drawString(.7 * inch, inch * .81, '2G Digital Post, Inc.')
    canvas.drawString(.7 * inch, inch * .73, '280 East Magnolia Blvd.')
    canvas.drawString(.7 * inch, inch * .65, 'Burbank, CA 91502')
    canvas.drawString(.7 * inch, inch * .57, '818.863.8900')

    canvas.setFont("Helvetica", 12)
    canvas.drawString(1.6 * inch, inch * .7, '2G018653')

    canvas.drawString(2.5 * inch, inch * .7, "That's My Boy")

    canvas.setFont("Helvetica", 6)

    canvas.drawString(4 * inch, inch * .81, "Part: 1 of 1")
    canvas.drawString(4 * inch, inch * .73, "TRT: 114:17")

    canvas.restoreState()

    # 5P Labels
    canvas.saveState()

    canvas.translate(.25 * inch, 5.90625 * inch)

    image = Image(os.path.dirname(os.path.realpath(__file__)) + '/5P_vertical.png')
    image.drawHeight = .75 * inch
    image.drawWidth = .875 * inch

    image.drawOn(canvas, 0, 0)
    image.drawOn(canvas, .90625 * inch, 0)



    canvas.restoreState()
    canvas.saveState()

    translate_x = 2.5
    translate_y = 0.125

    canvas.translate(translate_x * inch, translate_y * inch)
    canvas.rotate(90)

    draw_side_binding(canvas)
    draw_section_five(canvas)

    canvas.restoreState()
    canvas.saveState()

    translate_x = 5.2

    canvas.translate(translate_x * inch, translate_y * inch)
    canvas.rotate(90)

    draw_side_binding(canvas)
    draw_section_six(canvas)

    canvas.restoreState()
    canvas.saveState()

    translate_x = 8.3

    canvas.translate(translate_x * inch, translate_y * inch)
    canvas.rotate(90)

    draw_side_binding(canvas)
    draw_section_seven(canvas)

    canvas.showPage()
    canvas.save()


def draw_section_one(canvas, channel_list):
    canvas.setFont("Helvetica-Oblique", 8)
    canvas.translate(.25 * inch, 8.75 * inch)
    canvas.drawString(0, 2.6 * inch, "Sony")

    canvas.setFont("Helvetica", 12)
    canvas.drawString(0, 2.4 * inch, "That's My Boy")

    canvas.setFont("Helvetica", 7)
    canvas.drawString(0, 2.25 * inch, "Version: Theatrical")
    canvas.drawString(0, 2.10 * inch, "Latin American Spanish Foreign Language Master")
    canvas.drawString(0, 1.95 * inch, "Aspect Ratio: 16x9 1.78 Full Frame")
    canvas.drawString(0, 1.8 * inch, "Textless: Textless at Tail")

    canvas.setFont("Helvetica", 6)

    paragraph_style = ParagraphStyle('paraStyle')
    paragraph_style.fontSize = 6
    paragraph_style.leading = 8

    current_height_one = 0
    current_height_two = 0

    for iterator, channel_pair in enumerate(channel_list):
        paragraph1 = Paragraph('CH{0:02d}: {1}'.format(iterator + 1, channel_pair[0]), paragraph_style)
        width1, height1 = paragraph1.wrap(1.2 * inch, 50)

        paragraph2 = Paragraph('CH{0:02d}: {1}'.format(iterator + 7, channel_pair[1]), paragraph_style)
        width2, height2 = paragraph2.wrap(1.2 * inch, 50)

        current_height_one += height1
        current_height_two += height2

        paragraph1.drawOn(canvas, 0, 1.7 * inch - current_height_one)
        paragraph2.drawOn(canvas, 1.25 * inch, 1.7 * inch - current_height_two)

    canvas.restoreState()

    canvas.saveState()
    canvas.setFont("Helvetica", 12)
    canvas.translate(2.8 * inch, 8.75 * inch)
    canvas.drawString(0, 2.6 * inch, '2G018653')

    image = Image(os.path.dirname(os.path.realpath(__file__)) + '/2g_logo.png')
    image.drawHeight = .70 * inch * image.drawHeight / image.drawWidth
    image.drawWidth = .70 * inch

    image.drawOn(canvas, 0, 1.8 * inch)

    canvas.setFont('Helvetica', 6)
    canvas.drawString(0, 1.6 * inch, '2g Digital Post, Inc.')
    canvas.drawString(0, 1.5 * inch, '280 East Magnolia Blvd')
    canvas.drawString(0, 1.4 * inch, 'Burbank, CA 91502')
    canvas.drawString(0, 1.3 * inch, '818.863.8900')
    canvas.drawString(0, 1.1 * inch, '2016-08-17')
    canvas.drawString(0, 1.0 * inch, 'Std: 1080')
    canvas.drawString(0, 0.9 * inch, 'FR: 23.98PsF')
    canvas.drawString(0, 0.8 * inch, 'Part: 1 of 1')
    canvas.drawString(0, 0.7 * inch, 'TRT: 114:17')


def draw_side_binding(canvas):
    canvas.setFont("Helvetica", 12)
    canvas.drawString(0, 2.2 * inch, '2G018653')

    image = Image(os.path.dirname(os.path.realpath(__file__)) + '/2g_logo.png')
    image.drawHeight = .70 * inch * image.drawHeight / image.drawWidth
    image.drawWidth = .70 * inch

    image.drawOn(canvas, 0, 1.4 * inch)

    paragraph_style = ParagraphStyle('paraStyle')
    paragraph_style.fontSize = 6
    paragraph_style.leading = 8

    company_name = '2g Digital Post, Inc.'
    address_one = '280 East Magnolia Blvd'
    address_two = 'Burbank, CA 91502'
    phone_number = '818.863.8900'
    todays_date = '2016-08-17'
    standard = 'Std: 1080'
    frames_per_second = 'FR: 23.98PsF'
    part = 'Part: 1 of 1'
    total_runtime = 'TRT: 114:17'

    current_y = 1.2

    for text in (company_name, address_one, address_two, phone_number, todays_date, standard, frames_per_second,
                 part, total_runtime):
        paragraph = Paragraph(text, paragraph_style)
        paragraph.wrap(.9375 * inch, .5 * inch)
        paragraph.drawOn(canvas, 0, current_y * inch)

        current_y -= .1


def draw_section_five(canvas):

    client = 'Sony'
    title = "That's My Boy"
    version = 'Version: Theatrical'
    language = 'Latin American Spanish Foreign Language Master'
    aspect_ratio = 'Aspect Ratio: 16x9 1.78 Full Frame'
    textless = 'Textless: Textless at Tail'

    client_paragraph_style = ParagraphStyle('clientStyle')
    client_paragraph_style.fontSize = 8
    client_paragraph_style.leading = 10

    client_paragraph = Paragraph(client, client_paragraph_style)
    client_paragraph.wrap(2.0 * inch, 0.6 * inch)
    client_paragraph.drawOn(canvas, 1.3125 * inch, 2.2 * inch)

    title_paragraph_style = ParagraphStyle('titleStyle')
    title_paragraph_style.fontSize = 10
    title_paragraph_style.leading = 12

    title_paragraph = Paragraph(title, title_paragraph_style)
    title_paragraph.wrap(2.0 * inch, 1.0 * inch)
    title_paragraph.drawOn(canvas, 1.3125 * inch, 2.0 * inch)

    paragraph_style = ParagraphStyle('detailStyle')
    paragraph_style.fontSize = 6
    paragraph_style.leading = 8

    current_height = 1.95 * inch

    for detail_text in (version, language, aspect_ratio, textless):
        paragraph = Paragraph(detail_text, paragraph_style)
        paragraph.wrap(2.0 * inch, 0.6 * inch)

        current_height -= paragraph.height

        paragraph.drawOn(canvas, 1.3125 * inch, current_height)


def draw_section_six(canvas):

    client = 'Sony'
    title = "That's My Boy"
    version = 'Version: Theatrical'
    language = 'Latin American Spanish Foreign Language Master'
    aspect_ratio = 'Aspect Ratio: 16x9 1.78 Full Frame'
    textless = 'Textless: Textless at Tail'

    client_paragraph_style = ParagraphStyle('clientStyle')
    client_paragraph_style.fontSize = 8
    client_paragraph_style.leading = 10

    client_paragraph = Paragraph(client, client_paragraph_style)
    client_paragraph.wrap(2.0 * inch, 0.6 * inch)
    client_paragraph.drawOn(canvas, 1.3125 * inch, 2.2 * inch)

    title_paragraph_style = ParagraphStyle('titleStyle')
    title_paragraph_style.fontSize = 10
    title_paragraph_style.leading = 12

    title_paragraph = Paragraph(title, title_paragraph_style)
    title_paragraph.wrap(2.0 * inch, 1.0 * inch)
    title_paragraph.drawOn(canvas, 1.3125 * inch, 2.0 * inch)

    paragraph_style = ParagraphStyle('detailStyle')
    paragraph_style.fontSize = 6
    paragraph_style.leading = 8

    current_height = 1.95 * inch

    for detail_text in (version, language, aspect_ratio, textless):
        paragraph = Paragraph(detail_text, paragraph_style)
        paragraph.wrap(2.0 * inch, 0.6 * inch)

        current_height -= paragraph.height

        paragraph.drawOn(canvas, 1.3125 * inch, current_height)


def draw_section_seven(canvas):

    client = 'Sony'
    title = "That's My Boy"
    version = 'Version: Theatrical'
    language = 'Latin American Spanish Foreign Language Master'
    aspect_ratio = 'Aspect Ratio: 16x9 1.78 Full Frame'
    textless = 'Textless: Textless at Tail'

    client_paragraph_style = ParagraphStyle('clientStyle')
    client_paragraph_style.fontSize = 8
    client_paragraph_style.leading = 10

    client_paragraph = Paragraph(client, client_paragraph_style)
    client_paragraph.wrap(2.0 * inch, 0.6 * inch)
    client_paragraph.drawOn(canvas, 1.3125 * inch, 2.2 * inch)

    title_paragraph_style = ParagraphStyle('titleStyle')
    title_paragraph_style.fontSize = 10
    title_paragraph_style.leading = 12

    title_paragraph = Paragraph(title, title_paragraph_style)
    title_paragraph.wrap(2.0 * inch, 1.0 * inch)
    title_paragraph.drawOn(canvas, 1.3125 * inch, 2.0 * inch)

    paragraph_style = ParagraphStyle('detailStyle')
    paragraph_style.fontSize = 6
    paragraph_style.leading = 8

    current_height = 1.95 * inch

    for detail_text in (version, language, aspect_ratio, textless):
        paragraph = Paragraph(detail_text, paragraph_style)
        paragraph.wrap(2.0 * inch, 0.6 * inch)

        current_height -= paragraph.height

        paragraph.drawOn(canvas, 1.3125 * inch, current_height)


if __name__ == '__main__':
    main()
