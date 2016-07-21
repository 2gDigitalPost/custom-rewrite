from client.tactic_client_lib import TacticServerStub
import ConfigParser


def get_sobject_code_from_name(server, name, search_type):
    """
    Take the name of an sobject and return its code. Query the database and get all the sobjects, and then filter the
    sobject needed based on the name. Assuming that the queried table has unique names for each entry.

    :param name: String, name value of a machine
    :param search_type: String, a Tactic search type (ex: 'twog/machine')
    :return: String, code corresponding to a machine
    """

    sobject = server.eval("@SOBJECT({0}['name', '{1}'])".format(search_type, name))[0]
    # search = Search('twog/machine')
    # search.add_filter('name', name)
    # sobject = search.get_sobject()

    return sobject.get_code()


def get_frame_rate_code_from_name(name):
    frame_rates = {
        '23.98fps': 'FRAME_RATE00052',
        '59.94i': 'FRAME_RATE00053',
        '50i': 'FRAME_RATE00054',
        '29.97fps': 'FRAME_RATE00055',
        '24p': 'FRAME_RATE00056',
        '25p': 'FRAME_RATE00057',
        '59.94p': 'FRAME_RATE00058',
        'DFTC': 'FRAME_RATE00059',
        'NDFTC': 'FRAME_RATE00060',
        'PAL / EBU': 'FRAME_RATE00061'
    }

    return frame_rates.get(name, '')


def get_language_code_from_name(name):
    languages = {
        'Afar': 'LANGUAGE00005',
        'Abkhazian': 'LANGUAGE00006',
        'Afrikaans': 'LANGUAGE00007',
        'Akan': 'LANGUAGE00008',
        'Albanian': 'LANGUAGE00009',
        'Amharic': 'LANGUAGE00010',
        'Arabic': 'LANGUAGE00011',
        'Aragonese': 'LANGUAGE00012',
        'Armenian': 'LANGUAGE00013',
        'Assamese': 'LANGUAGE00014',
        'Avaric': 'LANGUAGE00015',
        'Avestan': 'LANGUAGE00016',
        'Aymara': 'LANGUAGE00017',
        'Azerbaijani': 'LANGUAGE00018',
        'Bashkir': 'LANGUAGE00019',
        'Bambara': 'LANGUAGE00020',
        'Basque': 'LANGUAGE00021',
        'Belarusian': 'LANGUAGE00022',
        'Bengali': 'LANGUAGE00023',
        'Bihari languages': 'LANGUAGE00024',
        'Bislama': 'LANGUAGE00025',
        'Tibetan': 'LANGUAGE00026',
        'Bosnian': 'LANGUAGE00027',
        'Breton': 'LANGUAGE00028',
        'Bulgarian': 'LANGUAGE00029',
        'Burmese': 'LANGUAGE00030',
        'Catalan; Valencian': 'LANGUAGE00031',
        'Czech': 'LANGUAGE00032',
        'Chamorro': 'LANGUAGE00033',
        'Chechen': 'LANGUAGE00034',
        'Chinese': 'LANGUAGE00035',
        'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic': 'LANGUAGE00036',
        'Chuvash': 'LANGUAGE00037',
        'Cornish': 'LANGUAGE00038',
        'Corsican': 'LANGUAGE00039',
        'Cree': 'LANGUAGE00040',
        'Welsh': 'LANGUAGE00041',
        'Danish': 'LANGUAGE00042',
        'German': 'LANGUAGE00043',
        'Divehi; Dhivehi; Maldivian': 'LANGUAGE00044',
        'Dutch; Flemish': 'LANGUAGE00045',
        'Dzongkha': 'LANGUAGE00046',
        'Greek, Modern(1453 -)': 'LANGUAGE00047',
        'English': 'LANGUAGE00048',
        'Esperanto': 'LANGUAGE00049',
        'Estonian': 'LANGUAGE00050',
        'Ewe': 'LANGUAGE00051',
        'Faroese': 'LANGUAGE00052',
        'Persian': 'LANGUAGE00053',
        'Fijian': 'LANGUAGE00054',
        'Finnish': 'LANGUAGE00055',
        'French': 'LANGUAGE00056',
        'Western Frisian': 'LANGUAGE00057',
        'Fulah': 'LANGUAGE00058',
        'Georgian': 'LANGUAGE00059',
        'Gaelic; Scottish Gaelic': 'LANGUAGE00060',
        'Irish': 'LANGUAGE00061',
        'Galician': 'LANGUAGE00062',
        'Manx': 'LANGUAGE00063',
        'Guarani': 'LANGUAGE00064',
        'Gujarati': 'LANGUAGE00065',
        'Haitian; Haitian Creole': 'LANGUAGE00066',
        'Hausa': 'LANGUAGE00067',
        'Hebrew': 'LANGUAGE00068',
        'Herero': 'LANGUAGE00069',
        'Hindi': 'LANGUAGE00070',
        'Hiri Motu': 'LANGUAGE00071',
        'Croatian': 'LANGUAGE00072',
        'Hungarian': 'LANGUAGE00073',
        'Igbo': 'LANGUAGE00074',
        'Icelandic': 'LANGUAGE00075',
        'Ido': 'LANGUAGE00076',
        'Sichuan Yi; Nuosu': 'LANGUAGE00077',
        'Inuktitut': 'LANGUAGE00078',
        'Interlingue; Occidental': 'LANGUAGE00079',
        'Interlingua(International Auxiliary Language Association)': 'LANGUAGE00080',
        'Indonesian': 'LANGUAGE00081',
        'Inupiaq': 'LANGUAGE00082',
        'Italian': 'LANGUAGE00083',
        'Javanese': 'LANGUAGE00084',
        'Japanese': 'LANGUAGE00085',
        'Kalaallisut; Greenlandic': 'LANGUAGE00086',
        'Kannada': 'LANGUAGE00087',
        'Kashmiri': 'LANGUAGE00088',
        'Kanuri': 'LANGUAGE00089',
        'Kazakh': 'LANGUAGE00090',
        'Central Khmer': 'LANGUAGE00091',
        'Kikuyu; Gikuyu': 'LANGUAGE00092',
        'Kinyarwanda': 'LANGUAGE00093',
        'Kirghiz; Kyrgyz': 'LANGUAGE00094',
        'Komi': 'LANGUAGE00095',
        'Kongo': 'LANGUAGE00096',
        'Korean': 'LANGUAGE00097',
        'Kuanyama; Kwanyama': 'LANGUAGE00098',
        'Kurdish': 'LANGUAGE00099',
        'Lao': 'LANGUAGE00100',
        'Latin': 'LANGUAGE00101',
        'Latvian': 'LANGUAGE00102',
        'Limburgan; Limburger; Limburgish': 'LANGUAGE00103',
        'Lingala': 'LANGUAGE00104',
        'Lithuanian': 'LANGUAGE00105',
        'Luxembourgish; Letzeburgesch': 'LANGUAGE00106',
        'Luba - Katanga': 'LANGUAGE00107',
        'Ganda': 'LANGUAGE00108',
        'Macedonian': 'LANGUAGE00109',
        'Marshallese': 'LANGUAGE00110',
        'Malayalam': 'LANGUAGE00111',
        'Maori': 'LANGUAGE00112',
        'Marathi': 'LANGUAGE00113',
        'Malay': 'LANGUAGE00114',
        'Malagasy': 'LANGUAGE00115',
        'Maltese': 'LANGUAGE00116',
        'Mongolian': 'LANGUAGE00117',
        'Nauru': 'LANGUAGE00118',
        'Navajo; Navaho': 'LANGUAGE00119',
        'Ndebele, South; South Ndebele': 'LANGUAGE00120',
        'Ndebele, North; North Ndebele': 'LANGUAGE00121',
        'Ndonga': 'LANGUAGE00122',
        'Nepali': 'LANGUAGE00123',
        'Norwegian Nynorsk; Nynorsk, Norwegian': 'LANGUAGE00124',
        'Bokmal, Norwegian; Norwegian Bokmal': 'LANGUAGE00125',
        'Norwegian': 'LANGUAGE00126',
        'Chichewa; Chewa; Nyanja': 'LANGUAGE00127',
        'Occitan(post 1500)': 'LANGUAGE00128',
        'Ojibwa': 'LANGUAGE00129',
        'Oriya': 'LANGUAGE00130',
        'Oromo': 'LANGUAGE00131',
        'Ossetian; Ossetic': 'LANGUAGE00132',
        'Panjabi; Punjabi': 'LANGUAGE00133',
        'Pali': 'LANGUAGE00134',
        'Polish': 'LANGUAGE00135',
        'Portuguese': 'LANGUAGE00136',
        'Pushto; Pashto': 'LANGUAGE00137',
        'Quechua': 'LANGUAGE00138',
        'Romansh': 'LANGUAGE00139',
        'Romanian; Moldavian; Moldovan': 'LANGUAGE00140',
        'Rundi': 'LANGUAGE00141',
        'Russian': 'LANGUAGE00142',
        'Sango': 'LANGUAGE00143',
        'Sanskrit': 'LANGUAGE00144',
        'Sinhala; Sinhalese': 'LANGUAGE00145',
        'Slovak': 'LANGUAGE00146',
        'Slovenian': 'LANGUAGE00147',
        'Northern Sami': 'LANGUAGE00148',
        'Samoan': 'LANGUAGE00149',
        'Shona': 'LANGUAGE00150',
        'Sindhi': 'LANGUAGE00151',
        'Somali': 'LANGUAGE00152',
        'Sotho, Southern': 'LANGUAGE00153',
        'Spanish; Latin': 'LANGUAGE00154',
        'Spanish; Castilian': 'LANGUAGE00155',
        'Sardinian': 'LANGUAGE00156',
        'Serbian': 'LANGUAGE00157',
        'Swati': 'LANGUAGE00158',
        'Sundanese': 'LANGUAGE00159',
        'Swahili': 'LANGUAGE00160',
        'Swedish': 'LANGUAGE00161',
        'Tahitian': 'LANGUAGE00162',
        'Tamil': 'LANGUAGE00163',
        'Tatar': 'LANGUAGE00164',
        'Telugu': 'LANGUAGE00165',
        'Tajik': 'LANGUAGE00166',
        'Tagalog': 'LANGUAGE00167',
        'Thai': 'LANGUAGE00168',
        'Tigrinya': 'LANGUAGE00169',
        'Tonga(Tonga Islands)': 'LANGUAGE00170',
        'Tswana': 'LANGUAGE00171',
        'Tsonga': 'LANGUAGE00172',
        'Turkmen': 'LANGUAGE00173',
        'Turkish': 'LANGUAGE00174',
        'Twi': 'LANGUAGE00175',
        'Uighur; Uyghur': 'LANGUAGE00176',
        'Ukrainian': 'LANGUAGE00177',
        'Urdu': 'LANGUAGE00178',
        'Uzbek': 'LANGUAGE00179',
        'Venda': 'LANGUAGE00180',
        'Vietnamese': 'LANGUAGE00181',
        'Volapuk': 'LANGUAGE00182',
        'Walloon': 'LANGUAGE00183',
        'Wolof': 'LANGUAGE00184',
        'Xhosa': 'LANGUAGE00185',
        'Yiddish': 'LANGUAGE00186',
        'Yoruba': 'LANGUAGE00187',
        'Zhuang; Chuang': 'LANGUAGE00188',
        'Zulu': 'LANGUAGE00189',
        'MLF': 'LANGUAGE00190',
        'Cantonese': 'LANGUAGE00191',
        'French Canadien': 'LANGUAGE00192',
        'Various': 'LANGUAGE00193',
        'Mandarin Simplified': 'LANGUAGE00194',
        'French Parisian Dubbed': 'LANGUAGE00195',
        'Portuguese; Brazilian': 'LANGUAGE00196'
    }

    return languages.get(name, '')


def get_machine_code_from_name(name):
    machines = {
        'VTR221': 'MACHINE00002',
        'VTR222': 'MACHINE00003',
        'VTR223': 'MACHINE00004',
        'VTR224': 'MACHINE00005',
        'VTR225': 'MACHINE00006',
        'VTR231': 'MACHINE00007',
        'VTR232': 'MACHINE00008',
        'VTR233': 'MACHINE00009',
        'VTR234': 'MACHINE00010',
        'VTR235': 'MACHINE00011',
        'VTR251': 'MACHINE00012',
        'VTR252': 'MACHINE00013',
        'VTR253': 'MACHINE00014',
        'VTR254': 'MACHINE00015',
        'VTR255': 'MACHINE00016',
        'VTR261': 'MACHINE00017',
        'VTR262': 'MACHINE00018',
        'VTR263': 'MACHINE00019',
        'VTR264': 'MACHINE00020',
        'VTR265': 'MACHINE00021',
        'VTR281': 'MACHINE00022',
        'VTR282': 'MACHINE00023',
        'VTR283': 'MACHINE00024',
        'VTR284': 'MACHINE00025',
        'VTR285': 'MACHINE00026',
        'FCP01': 'MACHINE00027',
        'FCP02': 'MACHINE00028',
        'FCP03': 'MACHINE00029',
        'FCP04': 'MACHINE00030',
        'FCP05': 'MACHINE00031',
        'FCP06': 'MACHINE00032',
        'FCP07': 'MACHINE00033',
        'FCP08': 'MACHINE00034',
        'FCP09': 'MACHINE00035',
        'FCP10': 'MACHINE00036',
        'FCP11': 'MACHINE00037',
        'FCP12': 'MACHINE00038',
        'Amberfin': 'MACHINE00039',
        'Clipster': 'MACHINE00040',
        'Stradis': 'MACHINE00041'
    }

    return machines.get(name, '')


def get_evaluation_lines(server, search_type, element_evaluation_code):
    """
    Perform a search for either sobjects of 'twog/element_evaluation_line' or 'twog/audio_evaluation_line' types. Return
    a list of found sobjects given an element evaluation code.

    Note that since the search is being done on the old server, using the Search class won't work.

    :param search_type: String, search type (either 'twog/element_evaluation_line' or 'twog/audio_evaluation_line')
    :param element_evaluation_code: String, the code of the sobject the lines are associated with
    :return:
    """
    lines = server.eval("@SOBJECT({0}['element_eval_code', '{1}'])".format(search_type, element_evaluation_code))

    return lines


def convert_audio_eval_lines(audio_eval_lines, element_evaluation_code):
    """
    Take a list of audio evaluation lines, and get the relevant data points. Then, assign it to an element evaluation.
    Return a list of the new audio evaluation lines to be inserted into the server.

    :param audio_eval_lines: List of audio_evaluation_line sobjects
    :param element_evaluation_code: String, the code of the sobject these lines will be associated with
    :return: List of dictionaries
    """
    new_audio_eval_lines = []

    for audio_eval_line in audio_eval_lines:
        new_audio_eval_line = {}

        for data_point in ('channel', 'content', 'peak', 'tone'):
            new_audio_eval_line[data_point] = audio_eval_line.get(data_point)

        new_audio_eval_line['element_evaluation_code'] = element_evaluation_code

        new_audio_eval_lines.append(new_audio_eval_line)

    return new_audio_eval_lines


def convert_element_eval_lines(element_eval_lines, element_evaluation_code):
    """
    Similar to the function convert_audio_eval_lines, but for element_evaluation_lines

    :param element_eval_lines: List of element_evaluation_line sobjects
    :param element_evaluation_code: String, the code of the sobject these lines will be associated with
    :return: List of dictionaries
    """
    new_element_eval_lines =[]

    for element_eval_line in element_eval_lines:
        new_element_eval_line = {}

        for data_point in ('description', 'field_in', 'field_out', 'in_source', 'scale', 'sector_or_channel',
                           'timecode_in', 'timecode_out', 'type_code'):
            new_element_eval_line[data_point] = element_eval_line.get(data_point)

        # 'in_source' is a special case because we're converting from strings 'Yes' and 'No' to booleans True and False
        if element_eval_line.get('in_source') == 'Yes':
            new_element_eval_line['in_source'] = True
        elif element_eval_line.get('in_source') == 'No':
            new_element_eval_line['in_source'] = False

        new_element_eval_line['element_evaluation_code'] = element_evaluation_code

        new_element_eval_lines.append(new_element_eval_line)

    return new_element_eval_lines


def get_audio_eval_lines(audio_lines, element_evaluation_code):
    matched_lines = []

    for audio_line in audio_lines:
        if element_evaluation_code == audio_line.get('code'):
            matched_lines.append(audio_line)

    return matched_lines


def get_element_eval_lines(element_lines, element_evaluation_code):
    matched_lines = []

    for element_line in element_lines:
        if element_evaluation_code == element_line.get('code'):
            matched_lines.append(element_line)

    return matched_lines


def main():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    # Get credentials from config file
    user = config.get('credentials', 'user')
    password = config.get('credentials', 'password')
    project = config.get('credentials', 'project')

    # Just get the dev server URL for now
    url = config.get('server', 'dev')

    # Get a server object to perform queries
    server = TacticServerStub(server=url, project=project, user=user, password=password)

    # Get the file holding the old element evaluation data
    element_evaluations_file = open('element_evals.txt', 'r')

    audio_lines = []
    audio_lines_file = open('audio_lines.txt', 'r')

    for line in audio_lines_file:
        audio_lines.append(eval(line))

    eval_lines = []
    eval_lines_file = open('eval_lines.txt', 'r')

    for line in eval_lines_file:
        eval_lines.append(eval(line))

    # Now iterate through the list of reports, and put together a dictionary with the converted data for each one
    for line in element_evaluations_file:
        print(line)
        element_evaluation = eval(line)

        # Initialize the dictionary to store the values
        new_element_evaluation = {}

        # First, grab the values that are a 1:1 conversion (that is, they don't need any special processing)
        data_points = (
            'active_video_begins',
            'active_video_ends',
            'bars_tone',
            'bay',
            'black_silence_1',
            'black_silence_2',
            'cc_subtitles',
            'chroma_peak',
            'end_of_program',
            'episode',
            'file_name',
            'format',
            'head_logo',
            'horizontal_blanking',
            'label',
            'login',
            'notices',
            'operator',
            'po_number',
            'record_date',
            'season',
            'slate_silence',
            'standard',
            'start_of_program',
            'style',
            'tail_logo',
            'total_runtime',
            'tv_feature_trailer',
            'version',
            'video_aspect_ratio',
            'vitc'
        )

        for data_point in data_points:
            new_element_evaluation[data_point] = element_evaluation.get(data_point)

        # Next, get the values that are named differently in the new server. No special processing required other than
        # to change the name
        new_element_evaluation['client'] = element_evaluation.get('client_code')
        new_element_evaluation['date'] = element_evaluation.get('timecode')
        new_element_evaluation['general_comments'] = element_evaluation.get('description')
        new_element_evaluation['luminance_peak'] = element_evaluation.get('video_peak')
        new_element_evaluation['status'] = element_evaluation.get('conclusion')
        new_element_evaluation['roll_up_blank'] = element_evaluation.get('roll_up')
        new_element_evaluation['source_barcode'] = element_evaluation.get('record_vendor')
        new_element_evaluation['textless_tail'] = element_evaluation.get('textless_at_tail')

        # Now comes the fun part. Some of the values stored as varchars in the old server are now using Foreign Key
        # relations. They probably should have been stored as Foreign Keys in the first place, but they weren't. To do
        # this, get the value from the old server, and using one of the reversed key-value dictionaries, look up its
        # code in the new server.
        new_element_evaluation['frame_rate'] = get_frame_rate_code_from_name(element_evaluation.get('frame_rate'))
        new_element_evaluation['language'] = get_language_code_from_name(element_evaluation.get('language'))
        new_element_evaluation['machine'] = get_machine_code_from_name(element_evaluation.get('machine_number'))

        # Give the report a name. Use the Title and code
        new_element_evaluation['name'] = element_evaluation.get('code') + ' in ' + element_evaluation.get('title', '')

        # Now insert the report. We'll need the search key of the inserted report, so get that from the server.insert()
        # function
        inserted_element_evaluation = server.insert('twog/element_evaluation', new_element_evaluation)

        # Convert and insert the audio evaluation lines
        audio_eval_lines = get_audio_eval_lines(audio_lines, element_evaluation.get('code'))
        server.insert_multiple('twog/audio_evaluation_lines', audio_eval_lines)

        # Convert and insert the element evaluation lines
        element_eval_lines = get_element_eval_lines(eval_lines, element_evaluation.get('code'))
        server.insert_multiple('twog/element_evaluation_lines', element_eval_lines)


    element_evaluations_file.close()


if __name__ == '__main__':
    main()
