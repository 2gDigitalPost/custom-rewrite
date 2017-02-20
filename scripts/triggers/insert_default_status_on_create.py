def main(server=None, input_data=None):
    if not input_data:
        return

    sobject_input = input_data.get('sobject')

    if not sobject_input.get('status'):
        server.update(sobject_input.get('__search_key__'), {'status': 'pending'})
