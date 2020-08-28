import mailparser
from os import walk
import LinkHandler as lh
import AttachmentHandler as ah

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

# here's where we will keep track of links and attachments
emails_with_links = []
links_found = []

emails_with_attachments = []
attachments_found = []

# for all those email filenames that we gathered above :
for filename in list_of_emails:

    # grab that file and convert it into an email object using the mailparser module
    # (git clone https://github.com/SpamScope/mail-parser.git)
    email = mailparser.parse_from_file_msg(EMAILS_FOLDER + filename)

    # does it contain a link?
    if lh.there_is_a_link_in(email):
        emails_with_links.append(email)
        links_in_this_email = lh.pull_links_from(email)
        links_found.append(links_in_this_email)

    # does it contain an attachment?
    if ah.there_is_an_attachment_in(email):
        emails_with_attachments.append(email)
        attachments_in_this_email = ah.pull_attachments_from(email)
        attachments_found.append(attachments_in_this_email)

# time to record our finding
print_emails_with_links()
print()
print_emails_with_attachments()

lh.write_links_to_disk(links_found, OUTPUT_FOLDER + "links")
ah.write_attachments_to_disk(attachments_found, OUTPUT_FOLDER + "attachments")
