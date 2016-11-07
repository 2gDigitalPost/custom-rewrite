import traceback
from datetime import date

from pyasm.search import Search

from formatted_emailer import email_sender
from email_senders import send_download_request_complete_email


def main(server=None, trigger_input=None):
    """
    Upon a Download Task being marked as 'Complete', send an email to the person who put in the request, notifying
    them that their request is finished.

    :param server: the TacticServerStub object
    :param trigger_input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not trigger_input:
        trigger_input = {}

    try:
        # Get the task
        task = trigger_input.get('sobject')

        # If this task is not a request to download a file, then skip the script
        # Not the prettiest way to make this happen, but I don't have any other ideas at the moment
        if 'Download Request:' not in task.get('process'):
            return

        # Only send the notification if the task is being marked as completed.
        if task.get('status') != 'Complete':
            return

        # The name of the task follows the 'Download Request: ' part
        download_task_name = task.get('process').split(': ')[-1]

        # Get the login id of the person who put in this request
        login = task.get('login')

        # Search for the person's data from the users table
        user_search = Search("sthpw/login")
        user_search.add_filter('login', login)
        user = user_search.get_sobject()

        # There should never be a case in which there's no user found, but you never know
        if user:
            # Email the user who put in the request
            email_address = user.get('email')

            # Call the function to send the email, using the download task's data
            send_download_request_complete_email.main(download_task_name, task.get('code'), task.get('description'),
                                                      email_address)

    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
        raise e
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the input dictionary does not exist.'
        raise e
    except Exception as e:
        traceback.print_exc()
        print str(e)
        raise e


if __name__ == '__main__':
    main()
