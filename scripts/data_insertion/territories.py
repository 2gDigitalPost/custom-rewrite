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

    # Set up a list of territories to insert. These are all the territories that previously existed in TACTIC
    territories = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
                   'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria',
                   'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize',
                   'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire', 'Bosnia and Herzegovina', 'Botswana',
                   'Bouvet Island', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
                   'Cameroon', 'Canada', 'Cantonese', 'Cape Verde', 'Cayman Islands', 'Central African Republic',
                   'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos Islands', 'Colombia', 'Comoros', 'Congo',
                   'Dem. Rep. of Congo', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech',
                   'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
                   'English', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands',
                   'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia',
                   'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greek', 'Greenland', 'Grenada', 'Guadeloupe',
                   'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras',
                   'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man',
                   'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya',
                   'Kiribati', 'Kuwait', 'Kyrgyztan', 'Laos', 'Latin America', 'Latin Spanish', 'Latvia', 'Lebanon',
                   'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luzembourg', 'Macao', 'Macedonia',
                   'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
                   'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia',
                   'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Multi-language', 'Myanmar', 'Namibia', 'Nauru',
                   'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue',
                   'Norfolk Island', 'North Korea', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
                   'Palestine', 'Panama', 'Papua New Guinea', 'Pan-Asia', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn',
                   'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Russian', 'Rwanda',
                   'St Barthelemy', 'St Helena', 'St Kitts and Nevis', 'St Lucia', 'St Martin', 'St Pierre and Miquelo',
                   'St Vincent and Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia',
                   'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Signapore', 'Sint Maarten', 'Slovakia',
                   'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and Swch Islands',
                   'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard', 'Swaziland',
                   'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thai', 'Thailand',
                   'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
                   'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'UAE', 'United Kingdom',
                   'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Various', 'Vatican', 'Venezuela', 'Vietnam',
                   'Virgin Islands', 'Wallis and Futuna', 'West Indies', 'Western Sahara', 'Yemen', 'Zambia',
                   'Zimbabwe']

    # Get a list of already existing territories
    existing_territories = server.eval('@SOBJECT(twog/territory)')
    existing_territories = [existing_territory.get('name') for existing_territory in existing_territories]

    # Filter out the territories that are already in the database
    territories_to_insert = [territory for territory in territories if territory not in existing_territories]
    print(territories_to_insert)

    for territory in territories_to_insert:
        # Insert the territory
        server.insert('twog/territory', {'name': territory})


if __name__ == '__main__':
    main()
