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
    frame_rates = ['23.98fps', '59.94i', '50i', '29.97fps', '24p', '25p', '59.94p', 'DFTC', 'NDFTC', 'PAL/EBU']

    # Get a list of already existing frame rates
    existing_frame_rates = server.eval('@SOBJECT(twog/frame_rate)')
    existing_frame_rates = [existing_frame_rate.get('name') for existing_frame_rate in existing_frame_rates]

    # Filter out the frame rates that are already in the database
    frame_rates_to_insert = [frame_rate for frame_rate in frame_rates if frame_rate not in existing_frame_rates]

    for frame_rate in frame_rates_to_insert:
        # Insert the frame rate
        server.insert('twog/frame_rate', {'name': frame_rate})


if __name__ == '__main__':
    main()