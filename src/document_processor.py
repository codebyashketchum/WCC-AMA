from typing import Dict, List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader


class DocumentProcessor:
    def __init__(self):
        self.loaders = {
            "txt": TextLoader,
            "pdf": PyPDFLoader,
        }
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def load_document(self, file_path: str) -> List[Document]:
        file_extension = file_path.split(".")[-1].lower()
        if file_extension not in self.loaders:
            raise ValueError(f"Unsupported file type: {file_extension}")

        loader = self.loaders[file_extension](file_path)
        return loader.load()

    def process_documents(self, documents: List[Document]) -> List[Document]:
        return self.text_splitter.split_documents(documents)

    def ingest_and_process(self, file_paths: List[str]) -> List[Document]:
        all_documents = []
        for file_path in file_paths:
            documents = self.load_document(file_path)
            processed_documents = self.process_documents(documents)
            all_documents.extend(processed_documents)
        return all_documents

    def get_document_metadata(self, documents: List[Document]) -> List[Dict]:
        return [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", None),
                "total_pages": doc.metadata.get("total_pages", None),
            }
            for doc in documents
        ]
