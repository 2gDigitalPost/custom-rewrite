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

    # Set up a list of languages to insert
    languages = ["Afar", "Abkhazian", "Afrikaans", "Akan", "Albanian", "Amharic", "Arabic", "Aragonese", "Armenian",
                 "Assamese", "Avaric", "Avestan", "Aymara", "Azerbaijani", "Bashkir", "Bambara", "Basque", "Belarusian",
                 "Bengali", "Bihari languages", "Bislama", "Tibetan", "Bosnian", "Breton", "Bulgarian", "Burmese",
                 "Catalan; Valencian", "Czech", "Chamorro", "Chechen", "Chinese",
                 "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic", "Chuvash",
                 "Cornish", "Corsican", "Cree", "Welsh", "Danish", "German", "Divehi; Dhivehi; Maldivian",
                 "Dutch; Flemish", "Dzongkha", "Greek, Modern (1453-)", "English", "Esperanto", "Estonian", "Ewe",
                 "Faroese", "Persian", "Fijian", "Finnish", "French", "Western Frisian", "Fulah", "Georgian",
                 "Gaelic; Scottish Gaelic", "Irish", "Galician", "Manx", "Guarani", "Gujarati",
                 "Haitian; Haitian Creole", "Hausa", "Hebrew", "Herero", "Hindi", "Hiri Motu", "Croatian", "Hungarian",
                 "Igbo", "Icelandic", "Ido", "Sichuan Yi; Nuosu", "Inuktitut", "Interlingue; Occidental",
                 "Interlingua (International Auxiliary Language Association)", "Indonesian", "Inupiaq", "Italian",
                 "Javanese", "Japanese", "Kalaallisut; Greenlandic", "Kannada", "Kashmiri", "Kanuri", "Kazakh",
                 "Central Khmer", "Kikuyu; Gikuyu", "Kinyarwanda", "Kirghiz; Kyrgyz", "Komi", "Kongo", "Korean",
                 "Kuanyama; Kwanyama", "Kurdish", "Lao", "Latin", "Latvian", "Limburgan; Limburger; Limburgish",
                 "Lingala", "Lithuanian", "Luxembourgish; Letzeburgesch", "Luba-Katanga", "Ganda", "Macedonian",
                 "Marshallese", "Malayalam", "Maori", "Marathi", "Malay", "Malagasy", "Maltese", "Mongolian", "Nauru",
                 "Navajo; Navaho", "Ndebele, South; South Ndebele", "Ndebele, North; North Ndebele", "Ndonga", "Nepali",
                 "Norwegian Nynorsk; Nynorsk, Norwegian", "Bokmal, Norwegian; Norwegian Bokmal", "Norwegian",
                 "Chichewa; Chewa; Nyanja", "Occitan (post 1500)", "Ojibwa", "Oriya", "Oromo", "Ossetian; Ossetic",
                 "Panjabi; Punjabi", "Pali", "Polish", "Portuguese", "Pushto; Pashto", "Quechua", "Romansh",
                 "Romanian; Moldavian; Moldovan", "Rundi", "Russian", "Sango", "Sanskrit", "Sinhala; Sinhalese",
                 "Slovak", "Slovenian", "Northern Sami", "Samoan", "Shona", "Sindhi", "Somali", "Sotho, Southern",
                 "Spanish; Latin", "Spanish; Castilian", "Sardinian", "Serbian", "Swati", "Sundanese", "Swahili",
                 "Swedish", "Tahitian", "Tamil", "Tatar", "Telugu", "Tajik", "Tagalog", "Thai", "Tigrinya",
                 "Tonga (Tonga Islands)", "Tswana", "Tsonga", "Turkmen", "Turkish", "Twi", "Uighur; Uyghur",
                 "Ukrainian", "Urdu", "Uzbek", "Venda", "Vietnamese", "Volapuk", "Walloon", "Wolof", "Xhosa", "Yiddish",
                 "Yoruba", "Zhuang; Chuang", "Zulu", "MLF", "Cantonese", "French Canadien", "Various",
                 "Mandarin Simplified", "French Parisian Dubbed", "Portuguese; Brazilian"]

    # Get a list of already existing languages
    existing_languages = server.eval('@SOBJECT(twog/language)')
    existing_languages = [existing_language.get('name') for existing_language in existing_languages]

    # Filter out the languages that are already in the database
    languages_to_insert = [language for language in languages if language not in existing_languages]

    for language in languages_to_insert:
        # Insert the language
        server.insert('twog/language', {'name': language})


if __name__ == '__main__':
    main()
