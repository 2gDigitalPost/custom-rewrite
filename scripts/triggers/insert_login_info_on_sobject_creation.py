from pyasm.common import Environment


def main(server=None, input_data=None):
    if not input_data:
        return

    sobject_input = input_data.get('sobject')

    login = Environment.get_login()
    user_name = login.get_value("login")

    server.update(sobject_input.get('__search_key__'), {'login': user_name})
