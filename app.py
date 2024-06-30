import streamlit as st
import os
from src.document_processor import DocumentProcessor
from src.retriever import Retriever
from src.llm_interface import LLMInterface
from src.visualizer import Visualizer
from src.math_processor import MathProcessor

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
    
    # Create temp directory if it doesn't exist
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # File uploader
    uploaded_files = st.file_uploader("Upload knowledge base documents", accept_multiple_files=True)
    
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            # Create a safe filename
            file_name = "".join(c for c in uploaded_file.name if c.isalnum() or c in (' ', '.', '_')).rstrip()
            file_path = os.path.join(temp_dir, file_name)
            
            try:
                # Save uploaded file temporarily
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process the document
                documents.extend(doc_processor.ingest_and_process([file_path]))
                
                # Remove the temporary file
                os.remove(file_path)
            except Exception as e:
                st.error(f"Error processing file {file_name}: {str(e)}")
        
        if documents:
            retriever.add_documents(documents)
            st.success(f"Processed and added {len(documents)} document chunks to the knowledge base.")
            
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