import mailparser
from os import walk

EMAILS_FOLDER = '/home/dan/Desktop/suspect_emails/'
OUTPUT_FOLDER = ''


def get_a_list_of_all_the_files_in(EMAILS_FOLDER):
    files = []
    emails = []
    # grab all the files in the directory
    for (dirpath, dirnames, file_name) in walk(EMAILS_FOLDER):
        files.extend(file_name)

    # filter-out those which are not emails
    for file in files:
        if '.msg' in file:
            emails.append(file)
    return emails


def there_is_a_link_in(email_object):
    return 'href=' in email_object.body


def there_is_an_attachment_in(email_object):
    return not (len(email_object.attachments) == 0)


def print_emails_with_links():
    print('EMAILS WITH LINKS:')
    for e in emails_with_links:
        print(e)


def print_emails_with_attachments():
    print('EMAILS WITH ATTACHMENTS:')
    for e in emails_with_attachments:
        print(e)

#############################################   -MAIN EXECUTION BLOCK BELOW-  #################################

# let's go to the folder (specified above) and grab the file names for all the emails from there.
list_of_emails = get_a_list_of_all_the_files_in(EMAILS_FOLDER)

# here's where we will keep track of the emails with links and attachments
emails_with_links = []
emails_with_attachments = []

# for all those email filenames that we gathered above :
for filename in list_of_emails:

    # grab that file and convert it into an email object using the mailparser module
    # (git clone https://github.com/SpamScope/mail-parser.git)
    email = mailparser.parse_from_file_msg(EMAILS_FOLDER + filename)

    # does it contain a link?
    if there_is_a_link_in(email):
        emails_with_links.append(email)

    # does it contain an attachment?
    if there_is_an_attachment_in(email):
        emails_with_attachments.append(email)

# print the results
print_emails_with_links()
print()
print_emails_with_attachments()
