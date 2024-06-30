import streamlit as st

from src.llm_interface import LLMInterface
from src.math_processor import MathProcessor
from src.retriever import Retriever
from src.visualizer import Visualizer


def main():
    st.title("Wireless Cellular Communications RAG Application")

    # Initialize components
    retriever = Retriever()
    llm = LLMInterface()
    visualizer = Visualizer()
    math_processor = MathProcessor()

    # Main application logic
    query = st.text_input(
        "Enter your question about \
                          wireless cellular communications:"
    )
    if query:
        # Process query and generate response
        relevant_docs = retriever.get_relevant_documents(query)
        response = llm.generate_response(query, relevant_docs)

        # Display response
        st.write(response)

        # Add visualization if needed
        if visualizer.should_visualize(query, response):
            fig = visualizer.create_visualization(query, response)
            st.pyplot(fig)

        # Process mathematical content if present
        if math_processor.contains_math(response):
            math_explanation = math_processor.explain_math(response)
            st.latex(math_explanation)


if __name__ == "__main__":
    main()
