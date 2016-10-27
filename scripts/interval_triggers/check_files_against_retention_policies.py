import traceback
from datetime import date, datetime, timedelta

from pyasm.prod.biz import ProdSetting
from pyasm.search import Search


def get_most_recent_completed_order_date(orders):
    most_recent_completion_date = None

    for order in orders:
        if order.get('status') != 'complete':
            return None

        if most_recent_completion_date is None:
            most_recent_completion_date = datetime.strptime(order.get('date_completed'),
                                                            '%Y-%m-%d %H:%M:%S')
        else:
            new_completion_date = datetime.strptime(order.get('date_completed'),
                                                    '%Y-%m-%d %H:%M:%S')

            if new_completion_date > most_recent_completion_date:
                most_recent_completion_date = new_completion_date

    return most_recent_completion_date


def main(server=None, input=None):
    """
    :param server: the TacticServerStub object
    :param input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """

    # Start by getting all the divisions
    divisions_search = Search('twog/division')
    divisions = divisions_search.get_sobjects()

    for division in divisions:
        # Get the division's retention policy, if one exists
        retention_policy_search = Search('twog/retention_policy')
        retention_policy_search.add_code_filter(division.get('retention_policy_code'))
        retention_policy = retention_policy_search.get_sobject()

        if retention_policy:
            # Get the number of days until archive
            source_days_to_archive = retention_policy.get('source_file_archive_days')
            intermediate_days_to_archive = retention_policy.get('intermediate_file_archive_days')
            deliverable_days_to_archive = retention_policy.get('deliverable_file_archive_days')

            # Get the number of days until deletion
            source_days_to_delete = retention_policy.get('source_file_delete_days')
            intermediate_days_to_delete = retention_policy.get('intermediate_file_delete_days')
            deliverable_days_to_delete = retention_policy.get('deliverable_file_delete_days')

            # Get all the files associated with the division, if any
            division_file_search = Search('twog/file')
            division_file_search.add_filter('division_code', division.get_code())
            # Only get files with san_status 'exists', 'needs_archive', or 'archived', they are the only files that
            # potentially need updating
            division_file_search.add_filter('san_status', 'deleted', op='!=')
            division_file_search.add_filter('san_status', 'needs_delete', op='!=')
            division_files = division_file_search.get_sobjects()

            for division_file in division_files:
                # Search for any orders that the file is a part of
                file_in_order_search = Search('twog/file_in_order')
                file_in_order_search.add_filter('file_code', division_file.get_code())
                file_in_order_entries = file_in_order_search.get_sobjects()

                # Get all the orders that the file is a part of. Do this by first getting all the order codes,
                # then doing a search for all the order sobjects
                order_codes = []

                for file_in_order_entry in file_in_order_entries:
                    order_code = "'{0}'".format(file_in_order_entry.get('order_code'))

                    if order_code not in order_codes:
                        order_codes.append(order_code)

                if order_codes:
                    # Search for the orders
                    orders_search = Search('twog/order')
                    orders_search.add_where('\"code\" in ({0})'.format(','.join(order_codes)))
                    orders = orders_search.get_sobjects()

                    # If the file is part of any order that isn't marked as complete, return immediately, since the
                    # file is still in use. If it is complete, use the most recent completion date from all the orders
                    # to determine when the file was last used
                    most_recent_completion_date = get_most_recent_completed_order_date(orders)

                    if most_recent_completion_date:
                        number_of_days_passed = (datetime.today() - most_recent_completion_date).days
                        print(number_of_days_passed)

                        file_classification = division_file.get('classification')

                        # Determine the file type, and which part of the retention policy to compare against
                        if file_classification == 'source':
                            days_to_archive = source_days_to_archive
                            days_to_delete = source_days_to_delete
                        elif file_classification == 'intermediate':
                            days_to_archive = intermediate_days_to_archive
                            days_to_delete = intermediate_days_to_delete
                        else:
                            days_to_archive = deliverable_days_to_archive
                            days_to_delete = deliverable_days_to_delete

                        if days_to_delete and days_to_delete < number_of_days_passed:
                            # Mark the file for deletion
                            search_key = server.build_search_key('twog/file', division_file.get_code(),
                                                                 project_code='twog')

                            server.update(search_key, {'san_status': 'needs_delete'})
                        elif days_to_archive and days_to_archive < number_of_days_passed:
                            # Mark the file for archiving
                            search_key = server.build_search_key('twog/file', division_file.get_code(),
                                                                 project_code='twog')

                            server.update(search_key, {'san_status': 'needs_archive'})


if __name__ == '__main__':
    main()
