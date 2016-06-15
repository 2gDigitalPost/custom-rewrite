from client.tactic_client_lib import TacticServerStub
import ConfigParser


def main():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    # Get credentials from config file
    user = config.get('credentials', 'user')
    password = config.get('credentials', 'password')
    project = config.get('credentials', 'project')

    # Just get the dev server URL for now
    url = config.get('server', 'dev')

    # Get a server object to perform queries
    server = TacticServerStub(server=url, project=project, user=user, password=password)

    # Set up a list of frame rates to insert
    machines = ('VTR221', 'VTR222', 'VTR223', 'VTR224', 'VTR225', 'VTR231', 'VTR232', 'VTR233', 'VTR234', 'VTR235',
                   'VTR251', 'VTR252', 'VTR253', 'VTR254', 'VTR255', 'VTR261', 'VTR262', 'VTR263', 'VTR264', 'VTR265',
                   'VTR281', 'VTR282', 'VTR283', 'VTR284', 'VTR285', 'FCP01', 'FCP02', 'FCP03', 'FCP04', 'FCP05',
                   'FCP06', 'FCP07', 'FCP08', 'FCP09', 'FCP10', 'FCP11', 'FCP12', 'Amberfin', 'Clipster', 'Stradis')

    # Get a list of already existing frame rates
    existing_machines = server.eval('@SOBJECT(twog/machine)')
    existing_machines = [existing_machine.get('name') for existing_machine in existing_machines]

    # Filter out the frame rates that are already in the database
    machines_to_insert = [machine for machine in machines if machine not in existing_machines]

    for machine in machines_to_insert:
        # Insert the frame rate
        server.insert('twog/machine', {'name': machine})


if __name__ == '__main__':
    main()