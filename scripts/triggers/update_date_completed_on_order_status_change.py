from datetime import datetime


def main(server=None, trigger_input=None):
    """
    On the update|twog/order|status event, if the order's status is set to 'completed', update the date_completed
    column with a timestamp.

    :param server: the TacticServerStub object
    :param trigger_input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not trigger_input:
        return

    # Get the order sobject.
    order_sobject = trigger_input.get('sobject')

    # Only perform the update if the status has been changed to 'complete'
    if order_sobject.get('status') == 'complete':
        # Get the current timestamp
        timestamp = datetime.now()

        # Build the order search key
        order_search_key = server.build_search_key('twog/order', order_sobject.get('code'), project_code='twog')

        # Send the update data to the server
        server.update(order_search_key, {'date_completed': timestamp})
