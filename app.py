import os

import streamlit as st

from src.document_processor import DocumentProcessor
from src.llm_interface import LLMInterface
from src.math_processor import MathProcessor
from src.retriever import Retriever
from src.visualizer import Visualizer


@st.cache_resource
def get_retriever():
    return Retriever()


@st.cache_resource
def get_llm_interface():
    return LLMInterface()


def main():
    st.title("Wireless Cellular Communications RAG Application")

    # Initialize components
    doc_processor = DocumentProcessor()
    retriever = get_retriever()
    llm = get_llm_interface()
    visualizer = Visualizer()
    math_processor = MathProcessor()

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload knowledge base documents", accept_multiple_files=True
    )

    if uploaded_files:
        documents = []
        for file in uploaded_files:
            file_path = os.path.join("temp", file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            documents.extend(doc_processor.ingest_and_process([file_path]))
            os.remove(file_path)

        retriever.add_documents(documents)
        st.success(
            f"Processed and added {len(documents)} document chunks to the knowledge base."
        )

        # Display document metadata
        metadata = doc_processor.get_document_metadata(documents)
        st.write("Document Metadata:", metadata)

    # Main application logic
    query = st.text_input("Enter your question about wireless cellular communications:")
    if query:
        try:
            # Process query and generate response
            relevant_docs = retriever.get_relevant_documents(query)
            response = llm.generate_response(query, relevant_docs)

            # Display response
            st.write("Answer:", response)

            # Display relevant document sources
            st.write("Relevant Sources:")
            for doc in relevant_docs:
                st.write(f"- {doc.metadata.get('source', 'Unknown')}")

            # Add visualization if needed
            if visualizer.should_visualize(query, response):
                fig, ax = visualizer.create_visualization(query, response)
                st.pyplot(fig)

            # Process mathematical content if present
            if math_processor.contains_math(response):
                math_explanation = math_processor.explain_math(response)
                st.latex(math_explanation)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
