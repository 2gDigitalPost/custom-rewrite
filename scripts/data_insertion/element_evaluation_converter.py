from client.tactic_client_lib import TacticServerStub
import ConfigParser

from pyasm.search import Search


def get_sobject_code_from_name(name, search_type):
    """
    Take the name of an sobject and return its code. Query the database and get all the sobjects, and then filter the
    sobject needed based on the name. Assuming that the queried table has unique names for each entry.

    :param name: String, name value of a machine
    :param search_type: String, a Tactic search type (ex: 'twog/machine')
    :return: String, code corresponding to a machine
    """

    search = Search('twog/machine')
    search.add_filter('name', name)
    sobject = search.get_sobject()

    return sobject.get_code()


def get_evaluation_lines(server, search_type, element_evaluation_code):
    """
    Perform a search for either sobjects of 'twog/element_evaluation_line' or 'twog/audio_evaluation_line' types. Return
    a list of found sobjects given an element evaluation code.

    Note that since the search is being done on the old server, using the Search class won't work.

    :param search_type: String, search type (either 'twog/element_evaluation_line' or 'twog/audio_evaluation_line')
    :param element_evaluation_code: String, the code of the sobject the lines are associated with
    :return:
    """
    lines = server.eval("@SOBJECT('{0}'['element_eval_code', '{1}'])".format(search_type, element_evaluation_code))

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

    # Get the old server to pull the data from
    old_server = TacticServerStub(server='http://tactic01.2gdigital.com', project=project, user=user, password=password)

    # Get all the element evaluations (this will probably take awhile)
    element_evaluations = old_server.eval("@SOBJECT(twog/element_eval)")

    # Now iterate through the list of reports, and put together a dictionary with the converted data for each one
    for element_evaluation in element_evaluations:
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
        new_element_evaluation['frame_rate'] = get_sobject_code_from_name(element_evaluation.get('frame_rate'),
                                                                          'twog/frame_rate')
        new_element_evaluation['language'] = get_sobject_code_from_name(element_evaluation.get('language'),
                                                                        'twog/language')
        new_element_evaluation['machine_number'] = get_sobject_code_from_name(element_evaluation.get('machine_number'),
                                                                              'twog/machine')

        # Now insert the report. We'll need the search key of the inserted report, so get that from the server.insert()
        # function
        inserted_element_evaluation = server.insert('twog/element_evaluation', new_element_evaluation)

        # Convert and insert the audio evaluation lines
        audio_eval_lines = convert_audio_eval_lines(get_evaluation_lines(old_server, 'twog/audio_evaluation_line',
                                                                         element_evaluation.get_code()),
                                                    inserted_element_evaluation.get_code())
        server.insert_multiple('twog/audio_evaluation_lines', audio_eval_lines)

        # Convert and insert the element evaluation lines
        element_eval_lines = convert_element_eval_lines(get_evaluation_lines(old_server, 'twog/element_evaluation_line',
                                                                             element_evaluation.get_code),
                                                        inserted_element_evaluation.get_code())
        server.insert_multiple('twog/element_evaluation_lines', element_eval_lines)


if __name__ == '__main__':
    main()
