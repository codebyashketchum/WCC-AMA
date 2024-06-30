import pytest
from langchain.schema import Document

from src.llm_interface import LLMInterface


@pytest.fixture
def llm_interface():
    return LLMInterface()


def test_generate_response(llm_interface):
    query = "What is 5G?"
    relevant_docs = [
        Document(page_content="5G is the fifth generation of cellular networks."),
        Document(page_content="5G offers faster speeds and lower latency than 4G."),
    ]
    response = llm_interface.generate_response(query, relevant_docs)

    assert isinstance(response, str)
    assert len(response) > 0
    assert "5g" in response.lower()  # The response should mention 5G (case-insensitive)
    print(f"Response: {response}")  # Add this line to print the response for debugging


# Add more tests as needed
