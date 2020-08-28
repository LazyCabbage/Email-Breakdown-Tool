from mailparser import MailParser


def there_is_a_link_in(email_object: MailParser) -> bool:
    return 'href=' in email_object.body


def pull_links_from(email_object: MailParser) -> list:
    # todo: given an email object, find and return all the hyperlinks inside.
    pass


def write_links_to_disk(links_found: list, output_file_location: str):
    # todo: given a list of strings, write all those strings to a file at the specified path.
    pass
