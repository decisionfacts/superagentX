import imaplib
import pprint
from enum import Enum
from typing import Any

from agentx.handler.base import BaseHandler
from agentx.handler.send_email.exceptions import RuntimeError


class EmailAction(str, Enum):
    SEND = "send"
    READ = "read"


class EmailReader(BaseHandler):

    def __init__(
            self,
            imap_host: str,
            imap_port: int,
            imap_username: str | None = None,
            imap_password: str | None = None
    ):
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.imap_username = imap_username
        self.imap_password = imap_password
        self.imap = None

    def handle(
            self,
            *,
            action: str | Enum,
            **kwargs
    ) -> Any:
        pass

    def connect(self):
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            self.imap.login(self.imap_username, self.imap_password)
        except imaplib.IMAP4.error as e:
            raise RuntimeError(f"IMAP login error: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during connection: {e}")

    def read_email(self):
        if self.imap is None:
            raise RuntimeError("Not connected to IMAP server.")

        try:
            self.imap.select('Inbox')
            result, data = self.imap.search(None, 'ALL')
            if result != 'OK':
                raise RuntimeError("Error searching inbox.")

            for num in data[0].split():
                result, data = self.imap.fetch(num, '(RFC822)')
                if result != 'OK':
                    raise RuntimeError(f"Error fetching email {num.decode()}")

                print(f'Message: {num.decode()}\n')
                pprint.pprint(data[0][1].decode('utf-8', errors='ignore'))

        except imaplib.IMAP4.error as e:
            raise RuntimeError(f"IMAP error occurred: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")
        finally:
            self.close_connection()

    def close_connection(self):
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except imaplib.IMAP4.error as e:
                raise RuntimeError(f"Error closing connection: {e}")
