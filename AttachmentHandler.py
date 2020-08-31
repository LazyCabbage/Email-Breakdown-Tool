from mailparser import MailParser


def there_is_an_attachment_in(email_object: MailParser) -> bool:
    return not (len(email_object.attachments) == 0)


def pull_attachments_from(email):
    # todo: given an email object, find and return all the attachments it has.
    return None


def write_attachments_to_disk(attachments_found: list, output_file_location: str):
    # todo: given a list of attachments, write all those attachments to a file at the specified path.
    pass
