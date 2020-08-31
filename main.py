import mailparser
from os import walk
import LinkHandler as lh
import AttachmentHandler as ah
import urlScan_API as scanner

IO_FOLDER = '/home/dan/Desktop/suspect_emails/'


def get_a_list_of_all_the_files_in(folder):
    files = []
    emails = []

    # grab all the files in the directory
    for (dirpath, dirnames, file_name) in walk(folder):
        files.extend(file_name)

    # filter-out those which are not emails
    for file in files:
        if '.msg' in file:
            emails.append(file)
    return emails


# ############################################   -MAIN EXECUTION BLOCK BELOW-  ################################# #

# let's go to the folder (specified above) and grab the file names for all the emails from there.
list_of_emails = get_a_list_of_all_the_files_in(IO_FOLDER)

# here's where we will keep track of links and attachments
emails_with_links = []
links_found = set()

emails_with_attachments = []
attachments_found = []

# for all those email filenames that we gathered above :
for filename in list_of_emails:

    # grab that file and convert it into an email object using the mailparser module
    # (git clone https://github.com/SpamScope/mail-parser.git)
    email = mailparser.parse_from_file_msg(IO_FOLDER + filename)

    # does it contain a link? If so, store the link.
    if lh.there_is_a_link_in(email):
        emails_with_links.append(email)
        links_in_this_email = lh.pull_links_from(email)
        links_found = links_found.union(links_in_this_email)

    # does it contain an attachment?
    if ah.there_is_an_attachment_in(email):
        emails_with_attachments.append(email)
        attachments_in_this_email = ah.pull_attachments_from(email)
        attachments_found.append(attachments_in_this_email)

# output our findings WRT links
print()
print('links found: ')
print(links_found)

malicious_links = set()
non_malicious_links = set()
not_able_to_submit_links = set()
no_response_links = set()
confused_links = set()

for link in links_found:
    scan_result = scanner.scan_link(link)
    if scan_result == 'MALICIOUS':
        malicious_links.add(link)

    if scan_result == 'NON-MALICIOUS':
        non_malicious_links.add(link)

    if scan_result == 'NOT ABLE TO SUBMIT':
        not_able_to_submit_links.add(link)

    if scan_result == 'ABLE TO SUBMIT BUT NO RESULT PROVIDED':
        no_response_links.add(link)

    if scan_result == 'CONFUSED':
        confused_links.add(link)

lh.write_links_to_disk(malicious_links, non_malicious_links, no_response_links, not_able_to_submit_links,
                       confused_links, IO_FOLDER + "links/")

ah.write_attachments_to_disk(attachments_found, IO_FOLDER + "attachments/")
