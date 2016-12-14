from tactic_client_lib import TacticServerStub

from pyasm.search import Search

from common_tools.time_utils import datetime_string_to_timezone_aware_string_tactic_formatted


def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    if not server:
        server = TacticServerStub.get()

    input_sobject = input_data.get('sobject')

    # Get the expected completion date. This is what determines priority
    expected_completion_date = input_sobject.get('expected_completion_date')

    if input_sobject and expected_completion_date:
        timezone_converted_completion_date = datetime_string_to_timezone_aware_string_tactic_formatted(expected_completion_date)

        # Search for orders due at the same time. Note that because this trigger runs after the insertion, the search
        # will find the new order, unless a filter is added to exclude it
        orders_completed_at_same_time_search = Search('twog/order')
        orders_completed_at_same_time_search.add_filter('expected_completion_date', timezone_converted_completion_date)
        orders_completed_at_same_time_search.add_filter('code', input_sobject.get('code'), op='!=')
        orders_completed_at_same_time = orders_completed_at_same_time_search.get_sobjects()

        if orders_completed_at_same_time:
            # Get any order from the list, shouldn't matter which one since they are all the same priority level
            order_completed_at_same_time = orders_completed_at_same_time[0]
            priority = float(order_completed_at_same_time.get('priority'))

            # Assign the priority of the other order to this one
            server.update(input_sobject.get('__search_key__'), {'priority': priority})
        else:
            # Need to get the orders that come immediately before and after this one's time.
            # Get the order before
            orders_before = server.eval('@SOBJECT(twog/order["expected_completion_date", "is before", "{0}"]["@ORDER_BY", "expected_completion_date"])'.format(timezone_converted_completion_date))

            if len(orders_before) > 1:
                order_before = orders_before[-2]
                previous_priority = order_before.get('priority')
            else:
                previous_priority = 0.0

            # Get the order after
            orders_after = server.eval(
                '@SOBJECT(twog/order["expected_completion_date", "is after", "{0}"]["@ORDER_BY", "expected_completion_date"]["@LIMIT", "2"])'.format(
                    timezone_converted_completion_date))

            if len(orders_after) > 1:
                order_after = orders_after[-1]
                next_priority = order_after.get('priority')
            else:
                next_priority = 600000.0

            priority = (previous_priority + next_priority) / 2.0

            server.update(input_sobject.get('__search_key__'), {'priority': priority})


if __name__ == '__main__':
    main()
