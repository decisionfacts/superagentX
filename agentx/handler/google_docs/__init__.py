from venv import logger

from agentx.handler.base import BaseHandler
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from agentx.handler.google_docs.exceptions import AuthException, FileNotFoundException

SCOPES = ['https://www.googleapis.com/auth/documents']
ENVIRONMENT_FILE = '/home/vijay/Agentx-google-Docs-Handler/agentxdocs-7e837f94cb17.json'
DOCUMENT_ID = '1uhl28TS8cKq8YN7cw5M2US0lTkT5cTQ1'

creds = Credentials.from_service_account_file(
    ENVIRONMENT_FILE,
    scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)


class DocsHandler(BaseHandler):

    @staticmethod
    def create_doc(
            title: str | None = None
    ):
        try:
            # Create a new Google Docs document with a title
            document = service.documents().create(
                body={
                    'title': title
                }
            ).execute()
            result = f'Create document with title: {document.get('title')}, Document Id: {document.get('documentId')}'
            print(result)
            return result
        except Exception as ex:
            err_msg = f'Google document Authentication problem {ex}'
            # logger.error(err_msg, exc_info=ex)
            raise AuthException(err_msg)

    @staticmethod
    def read_doc(
            documentId: str | None = None
    ):
        try:
            # Retrieve the document content by ID
            document = service.documents().get(documentId=documentId).execute()
            print('Document title: {0}'.format(document.get('title')))

            # Print document content
            for content in document.get('body').get('content'):
                if 'paragraph' in content:
                    for element in content.get('paragraph').get('elements'):
                        text_run = element.get('textRun')
                        if text_run:
                            print(text_run.get('content'))
                            return text_run.get('')
        except Exception as ex:
            err_msg = f'Google document Authentication problem {ex}'
            logger.error(err_msg, exc_info=ex)
            raise AuthException(err_msg)

    @staticmethod
    def update_doc(
            documentId: str | None = None,
            text: str | None = None,
            line_index: int | None = None
    ):
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': line_index,  # Inserts text at the start of the document
                        },
                        'text': text
                    }
                }
            ]
            # Execute the request to update the document
            result = service.documents().batchUpdate(documentId=documentId, body={'requests': requests}).execute()
            print(f"Updated document {documentId} with new text.")
        except Exception as ex:
            err_msg = f'Google document Authentication problem {ex}'
            # logger.error(err_msg, exc_info=ex)
            logger.error(err_msg, exc_info=ex)
            raise AuthException(err_msg)

    # create_doc(title="Test Vijay Docs")
    # read_doc(documentId="1VGr3QQYuqoNgKV8HDt3jeObotPT3ko3RxDW2mMxQA1k")
    # update_doc(documentId="1VGr3QQYuqoNgKV8HDt3jeObotPT3ko3RxDW2mMxQA1k", text="hello ", line_index=1)

    def __dir__(self):
        return (
            'create_doc',
            'read_doc',
            'update_doc'
        )
