from abc import ABC, abstractmethod
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.vectorstores import Redis
import os
import warnings
import config
import re

# Ignore all warnings
warnings.filterwarnings("ignore")


# Abstract base class for vector databases
class VectorDatabase(ABC):
    @abstractmethod
    def index_texts(self, texts, embeddings, index_name):
        pass


# Concrete implementation of Redis vector database
class RedisVectorDatabase(VectorDatabase):
    def __init__(self):
        self.document_search = None

    def index_texts(self, texts, embeddings, index_name):
        self.document_search = Redis.from_texts(
            texts,
            embeddings,
            redis_url=config.REDIS_URL,
            index_name=index_name,
        )
        return self.document_search


# Abstract base class for question-answering chains
class QAChain(ABC):
    @abstractmethod
    def create_chain(self):
        pass


# Concrete implementation of OpenAI question-answering chain
class OpenAIQAChain(QAChain):
    def create_chain(self):
        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        return chain


# Factory pattern for creating vector databases
class VectorDatabaseFactory:
    @staticmethod
    def get_vector_database(db_type: str) -> VectorDatabase:
        if db_type == "redis":
            return RedisVectorDatabase()
        raise ValueError(f"Unknown vector database type: {db_type}")


# Factory pattern for creating question-answering chains
class QAChainFactory:
    @staticmethod
    def get_qa_chain(model_type: str) -> QAChain:
        if model_type == "openai":
            return OpenAIQAChain()
        raise ValueError(f"Unknown QA chain type: {model_type}")


# The main class to manage text processing and querying
class TextQueryProcessor:
    def __init__(self, vector_db: VectorDatabase, qa_chain: QAChain):
        self.vector_db = vector_db
        self.qa_chain = qa_chain

    def process_texts(self, raw_text, embeddings):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text)
        self.vector_db.index_texts(texts, embeddings, "reviewidx")

    def query_texts(self, query):
        docs = self.vector_db.document_search.similarity_search(query)
        answer = self.qa_chain.run(input_documents=docs, question=query)
        return answer


class Chatbot:
    def __init__(self, vector_db_type, llm_model_type) -> None:
        self.vector_db_type = vector_db_type
        self.llm_model_type = llm_model_type

    def preprocess_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def answer_questions(self, text_data: str, questions: list) -> dict:
        # Create instances using factories
        vector_db = VectorDatabaseFactory.get_vector_database(
            self.vector_db_type
        )
        qa_chain = QAChainFactory.get_qa_chain(self.llm_model_type)
        qa_chain = qa_chain.create_chain()
        embeddings = OpenAIEmbeddings()

        # Initialize TextQueryProcessor with the created instances
        text_query_processor = TextQueryProcessor(vector_db, qa_chain)

        # Process the text and query
        text_query_processor.process_texts(text_data, embeddings)

        output = {}
        for question in questions:
            answer = text_query_processor.query_texts(question)
            output[question] = self.preprocess_text(answer)

        return output
