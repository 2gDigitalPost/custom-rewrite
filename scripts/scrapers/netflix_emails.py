import os
import argparse


def main():
    mail_path = '/DATA/TACTIC-MAIL'

    for dir_entry in os.listdir(mail_path):
        file_path = os.path.join(mail_path, dir_entry)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as email_file:
                for line in email_file:
                    pass


if __name__ == '__main__':
    main()
