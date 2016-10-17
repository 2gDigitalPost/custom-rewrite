import traceback


def main(server=None, trigger_input=None):
    """
    On the insert|twog/package event, search for an existing connection from the package's division to platform.
    If no entry exists in the twog/platform_connection table, create it by inserting the division_code, platform_code,
    and a connection_status set to 'disconnected'.

    :param server: the TacticServerStub object
    :param trigger_input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not trigger_input:
        return

    try:
        from pyasm.search import Search

        # Get the package sobject.
        package_sobject = trigger_input.get('sobject')

        # Search for the twog/order sobject (which leads to the division)
        order_search = Search('twog/order')
        order_search.add_code_filter(package_sobject.get('order_code'))
        order_sobject = order_search.get_sobject()

        # Search for the twog/division sobject
        division_search = Search('twog/division')
        division_search.add_code_filter(order_sobject.get('division_code'))
        division_sobject = division_search.get_sobject()

        # Search for an existing entry in the twog/platform_connection table. If it already exists, no action is needed
        existing_platform_connection_search = Search('twog/platform_connection')
        existing_platform_connection_search.add_filter('division_code', division_sobject.get_code())
        existing_platform_connection_search.add_filter('platform_code', package_sobject.get('platform_code'))
        existing_platform_connection = existing_platform_connection_search.get_sobject()

        if not existing_platform_connection:
            # Insert the new entry
            data_to_insert = {
                'division_code': division_sobject.get_code(),
                'platform_code': package_sobject.get('platform_code'),
                'connection_status': 'disconnected'
            }

            server.insert('twog/platform_connection', data_to_insert)

    except Exception as e:
        traceback.print_exc()
        print str(e)
        raise e


if __name__ == '__main__':
    main()
