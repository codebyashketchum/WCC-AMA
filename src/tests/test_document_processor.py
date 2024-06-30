import pytest
from langchain.schema import Document

from src.document_processor import DocumentProcessor


@pytest.fixture
def doc_processor():
    return DocumentProcessor()


def test_load_document(doc_processor, tmp_path):
    # Create a temporary text file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.txt"
    p.write_text("This is a test document.")

    # Load the document
    docs = doc_processor.load_document(str(p))

    assert len(docs) == 1
    assert isinstance(docs[0], Document)
    assert docs[0].page_content == "This is a test document."


def test_process_documents(doc_processor):
    docs = [Document(page_content="This is a long document " * 100)]
    processed_docs = doc_processor.process_documents(docs)

    assert len(processed_docs) > 1
    for doc in processed_docs:
        assert len(doc.page_content) <= 1000


def test_get_document_metadata(doc_processor):
    docs = [
        Document(page_content="Doc1", metadata={"source": "file1.txt", "page": 1}),
        Document(page_content="Doc2", metadata={"source": "file2.txt", "page": 2}),
    ]
    metadata = doc_processor.get_document_metadata(docs)

    assert len(metadata) == 2
    assert metadata[0]["source"] == "file1.txt"
    assert metadata[1]["page"] == 2
