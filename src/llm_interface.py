from typing import List

from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough


class LLMInterface:
    def __init__(self, model_name="llama2"):
        self.llm = Ollama(model=model_name)
        self.prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""You are an AI assistant specializing in wireless cellular communications.
            Use the following pieces of context to answer the query at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context:
            {context}

            Query: {query}

            Answer:""",
        )
        self.chain = (
            {"context": RunnablePassthrough(), "query": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )

    def generate_response(self, query: str, relevant_docs: List[Document]) -> str:
        context = "\n".join([doc.page_content for doc in relevant_docs])
        response = self.chain.invoke({"query": query, "context": context})
        return response
