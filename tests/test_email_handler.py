from agentx.handler.send_email import SendEmailHandler
from agentx.handler.read_email import EmailReader

email_handler = SendEmailHandler(
    host="",
    port=345,
    username="",
    password=""
)


def test_email_1():
    res = email_handler.handle(action="SEND", **{})
    assert res


email_reader = EmailReader(
    imap_host='',
    imap_username="",
    imap_port=143,
    imap_password=""
)


def test_email_2():
    res = email_reader.handle(action="READ", **{})
    assert res
