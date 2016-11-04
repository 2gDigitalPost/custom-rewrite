def fix_message_characters(message):
    """Fixes the escaped characters and replaces them with equivalents
    that are formatted for html.

    :param message: the message as a string
    :return: the html-formatted string
    """
    if isinstance(message, bool):
        return str(message)

    import sys
    from json import dumps as jsondumps
    if message not in [None, '']:
        if sys.stdout.encoding:
            message = message.decode(sys.stdout.encoding)
    message = jsondumps(message)

    tab = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    newline = '<br/>'
    # OrderedDict does not exist in python 2.6, so do this the long way for now
    message = message.replace('||t', tab)
    message = message.replace('\\\\t', tab)
    message = message.replace('\\\t', tab)
    message = message.replace('\\t', tab)
    message = message.replace('\t', tab)
    message = message.replace('||n', newline)
    message = message.replace('\\\\n', newline)
    message = message.replace('\\\n', newline)
    message = message.replace('\\n', newline)
    message = message.replace('\n', newline)
    message = message.replace('\\"', '"')
    message = message.replace('\"', '"')

    return message