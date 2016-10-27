from datetime import datetime


def main(server=None, trigger_input=None):
    """
    On the insert|twog/contact event, insert the contact's "name" field based on the first_name and last_name fields.

    :param server: the TacticServerStub object
    :param trigger_input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not trigger_input:
        return

    # Get the contact sobject.
    contact_sobject = trigger_input.get('sobject')

    # Use the first_name and last_name fields to build the name. If one is empty, don't include it
    first_name = contact_sobject.get('first_name')
    last_name = contact_sobject.get('last_name')

    if first_name and last_name:
        name = first_name + ' ' + last_name
    elif first_name:
        name = first_name
    elif last_name:
        name = last_name
    else:
        # No first or last name was given, so just return
        return

    # Build the contact search key
    contact_search_key = server.build_search_key('twog/contact', contact_sobject.get('code'), project_code='twog')

    # Send the update data to the server
    server.update(contact_search_key, {'name': name})
