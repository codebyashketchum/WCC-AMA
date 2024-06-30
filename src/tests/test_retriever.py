import pytest
from langchain.schema import Document

from src.retriever import Retriever


@pytest.fixture
def retriever(tmp_path):
    return Retriever(persist_directory=str(tmp_path / "test_vector_store"))


def test_add_documents(retriever):
    docs = [
        Document(page_content="This is a test document."),
        Document(page_content="This is another test document."),
    ]
    retriever.add_documents(docs)
    assert retriever.vector_store is not None


def test_get_relevant_documents(retriever):
    docs = [
        Document(page_content="Wireless communication uses radio waves."),
        Document(page_content="5G is the fifth generation of cellular networks."),
    ]
    retriever.add_documents(docs)

    relevant_docs = retriever.get_relevant_documents("What is 5G?")
    assert len(relevant_docs) > 0
    assert "5G" in relevant_docs[0].page_content


def test_save_and_load_vector_store(retriever, tmp_path):
    docs = [Document(page_content="Test document for saving and loading.")]
    retriever.add_documents(docs)
    retriever.save_vector_store()

    new_retriever = Retriever(persist_directory=str(tmp_path / "test_vector_store"))
    new_retriever.load_vector_store()

    assert new_retriever.vector_store is not None
    relevant_docs = new_retriever.get_relevant_documents("Test document")
    assert len(relevant_docs) > 0


def test_clear_vector_store(retriever):
    docs = [Document(page_content="Test document for clearing.")]
    retriever.add_documents(docs)
    retriever.clear_vector_store()

    assert retriever.vector_store is None
    with pytest.raises(ValueError):
        retriever.get_relevant_documents("Test")
