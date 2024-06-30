import os
from typing import List
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class Retriever:
    def __init__(self, persist_directory: str = "vector_store"):
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store = None
        self.persist_directory = persist_directory

    def add_documents(self, documents: List[Document]):
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)

    def get_relevant_documents(self, query: str, k: int = 4) -> List[Document]:
        if self.vector_store is None:
            raise ValueError("No documents have been added to the retriever yet.")
        return self.vector_store.similarity_search(query, k=k)

    def save_vector_store(self):
        if self.vector_store is None:
            raise ValueError("No vector store to save.")
        self.vector_store.save_local(self.persist_directory)

    def load_vector_store(self):
        if os.path.exists(self.persist_directory):
            self.vector_store = FAISS.load_local(
                self.persist_directory,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            print(f"No existing vector store found at {self.persist_directory}")

    def clear_vector_store(self):
        self.vector_store = None
        if os.path.exists(self.persist_directory):
            import shutil

            shutil.rmtree(self.persist_directory)
        print("Vector store cleared.")
