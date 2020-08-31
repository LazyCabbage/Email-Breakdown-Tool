from mailparser import MailParser
import csv
import os

CHARACTERS_AT_BEGINNING_OF_HYPERLINKS = 'href='
CHARACTERS_AT_END_OF_HYPERLINKS = '>'


def there_is_a_link_in(email_object: MailParser) -> bool:
    return 'href=' in email_object.body


def pull_links_from(email_object: MailParser) -> set:
    return_set = set()

    # get the body of the email.
    text_to_check = email_object.body



    while True:
        # find first instance of ' href=" ', and delete everything up to that point.
        # (the +1 is to make up for the ' " ' symbol after href= )
        beginning_of_next_hyperlink = text_to_check.find(CHARACTERS_AT_BEGINNING_OF_HYPERLINKS) + len(
            CHARACTERS_AT_BEGINNING_OF_HYPERLINKS) + 1

        # if the above returned a "0", there are no more hyperlinks and we can break out of this loop
        if beginning_of_next_hyperlink == len(CHARACTERS_AT_BEGINNING_OF_HYPERLINKS):
            break

        # delete everything up to that point
        text_to_check = text_to_check[beginning_of_next_hyperlink:]

        # find the end of the hyperlink
        end_of_next_hyperlink = text_to_check.find(CHARACTERS_AT_END_OF_HYPERLINKS) - 1

        # grab that hyperlink
        hyperlink = text_to_check[:end_of_next_hyperlink]
        return_set.add(hyperlink)

        # delete everything we've gone over so far
        text_to_check = text_to_check[end_of_next_hyperlink:]
    return return_set


def write_links_to_disk(malicious_links, non_malicious_links, no_response_links, not_able_to_submit_links,
                        confused_links, PATH):
    os.mkdir(PATH)

    with open(PATH + 'malicious', 'w+', newline='') as file:
        writer = csv.writer(file)
        for link in malicious_links:
            writer.writerow([link])

    with open(PATH + 'non-malicious', 'w+', newline='') as file:
        writer = csv.writer(file)
        for link in non_malicious_links:
            writer.writerow([link])

    with open(PATH + 'no_response', 'w+', newline='') as file:
        writer = csv.writer(file)
        for link in no_response_links:
            writer.writerow([link])

    with open(PATH + 'not_able_to_submit', 'w+', newline='') as file:
        writer = csv.writer(file)
        for link in not_able_to_submit_links:
            writer.writerow([link])

    with open(PATH + 'confused', 'w', newline='') as file:
        writer = csv.writer(file)
        for link in confused_links:
            writer.writerow([link])
