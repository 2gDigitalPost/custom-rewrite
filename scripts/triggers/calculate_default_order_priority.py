from tactic_client_lib import TacticServerStub

from pyasm.search import Search

from datetime import datetime, timedelta


def main(server=None, input_data=None):
    if not input_data:
        input_data = {}

    if not server:
        server = TacticServerStub.get()

    input_sobject = input_data.get('sobject')

    search_key = server.build_search_key('twog/order', input_sobject.get('code'), project_code='twog')

    order_search = Search('twog/order')
    order_search.get_by_search_key(search_key)
    order_sobject = order_search.get_sobject()

    due_date = input_sobject.get('due_date')

    if order_sobject and due_date:
        due_date_datetime_object = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        due_date_string = due_date_datetime_object.strftime('%Y-%m-%d')
        due_date_day_after_string = (due_date_datetime_object + timedelta(days=1)).strftime('%Y-%m-%d')

        orders_due_day_of_search = Search('twog/order')
        orders_due_day_of_search.add_filter('due_date', due_date_string)
        orders_due_day_of = orders_due_day_of_search.get_sobjects()

        if len(orders_due_day_of) > 1:
            priorities = [order_due_day_of.get('priority') for order_due_day_of in orders_due_day_of]
            priority = sum([float(priority) for priority in priorities]) / float(len(priorities) - 1)

        else:
            order_due_day_before_list = server.eval(
                "@SOBJECT(twog/order['due_date', 'is before', '{0}']['@ORDER_BY', 'due_date desc']['@LIMIT', '2'])".format(due_date_string))
            order_due_day_after_list = server.eval(
                "@SOBJECT(twog/order['due_date', 'is after', '{0}']['@ORDER_BY', 'due_date asc']['@LIMIT', '1'])".format(due_date_day_after_string))

            if len(order_due_day_before_list) > 1:
                order_due_day_before = order_due_day_before_list[1]
                priority_lower_bound = float(order_due_day_before.get('priority'))
            else:
                priority_lower_bound = 0.0

            if order_due_day_after_list:
                order_due_day_after = order_due_day_after_list[0]
                priority_upper_bound = float(order_due_day_after.get('priority'))
            else:
                priority_upper_bound = 600000.0

            priority = (priority_lower_bound + priority_upper_bound) / 2.0

        server.update(search_key, {'priority': priority})


if __name__ == '__main__':
    main()
