from agentx.handler.google_docs import DocsHandler

docs = DocsHandler()


def test_docs():
    docs.read_doc(documentId="1VGr3QQYuqoNgKV8HDt3jeObotPT3ko3RxDW2mMxQA1k")
