from multiprocessing.managers import BaseManager
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from typing import Optional,List
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from utills.model_utils import ModelLoader
from prompt.prompt_analyzer import PROMPT_REGISTRY
from model.base_model import PromptType,SummaryResponse
from pathlib import Path
import sys
from langchain_core.documents import Document
from operator import itemgetter



class DocumentRetriever:
    def __init__(self, retriver, session_id: str = None):
        """
        Initializes the DocumentRetriever with the path for the FAISS index.
        :param faiss_index_path: Directory where FAISS index is stored.
        :param session_id: Unique identifier for the session, defaults to current timestamp.
        """
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.retriver = retriver
            self.parser = StrOutputParser()
            self.session_id = session_id or "document_chat_session"
            self.model = ModelLoader()
            self.llm = self.model.load_llm()
            self.embeddings = self.model.load_embedding()
            self.qa_prompt = PROMPT_REGISTRY.get(PromptType.CONTEXT_QA.value)
            self.rewriter_prompt = PROMPT_REGISTRY.get(PromptType.CONTEXTUALIZE_QUESTION.value)

            self.log.info("DocumentRetriever successfully initialized")

        except Exception as e:
            self.log.error("Error in initialization DocumentRetriever")
            raise (e, sys)
        

    def invoke(self,user_query:str,chat_history:Optional[List[BaseMessage]]=None):
        try:
            if self.main_chain is None:
                raise CustomException(
                    "RAG chain not initialized. Call load_retriever_from_faiss() before invoke().", sys)
            self.chat_history = chat_history or []
            self.payload = {"user_input":user_query, "chat_history":self.chat_history}
            if self.retriver is None:
                #retriver = self._create_retrivel(self.documents)
                self.log.error("Retriever is not initialized")
                raise CustomException("Retriever is not initialized", sys)
            self.log.info("Retrieving relevant documents for the query")
            response = self.main_chain.invoke(self.payload)
            if not response:
                self.log.warning("no response from main chain invoke")
            self.log.info("Documents invoke successfully")
        except Exception as e:
            self.log.error("Error in initialization DocumentRetriever")
            raise (e, sys)


    def _create_retrivel(self, documents):
        """
        Builds a LangChain retriever using the provided documents.
        :param documents: List of Document objects to be used for retrieval.
        :return: A LangChain retriever object.
        """
        try:
            if not documents:
                raise CustomException("No documents provided for retrieval", sys)
            self.log.info("Building LangChain retriever")
            vector_store = FAISS.from_documents(documents, self.embeddings)
            retriever = vector_store.as_retriever(search_kwargs={"k": 5})
            self.log.info("LangChain retriever successfully built")
            return retriever
        except Exception as e:
            self.log.error(f"Error building LangChain retriever: {e}")
            raise CustomException(f"Error building LangChain retriever: {e}", sys)
        


    def _built_lcel_chain(self,):
        try:
            # 1) Rewrite user question with chat history context
            question_rewritter = {"user_input":itemgetter("user_input"),"chat_history":itemgetter("chat_history")} | self.rewriter_prompt | self.llm | self.parser
            self.log.info("Question rewriting chain successfully built")
            # 2) Retrieve relevant documents based on the rewritten question
            if self.retriver is None:
                self.log.error("Retriever is not initialized")
                raise CustomException("Retriever is not initialized", sys)
            retriving_doc_chain = question_rewritter | self.retriver | self._format_doc
            self.log.info("LCEL chain successfully built")
            # 3) Main chain that combines the rewritten question, retrieved documents, and chat history
            self.main_chain = {"context": retriving_doc_chain,"user_input":itemgetter("user_input"),"chat_history":itemgetter("chat_history")} | self.qa_prompt | self.llm | self.parser
            self.log.info("Main lcel chain successfully built")
        except:
            self.log.error("Error building LCEL chain")
            raise CustomException("Error building LCEL chain", sys)


    def _format_doc(self,docs):
        """
        Formats the retrieved documents into a string for further processing.
        :param docs: List of Document objects retrieved from the retriever.
        :return: A formatted string containing the content of the documents.
        """
        try:
            if not docs:
                raise CustomException("No documents to format", sys)
            self.log.info("Formatting retrieved documents")
            formatted_docs = "\n\n".join([doc.page_content for doc in docs])
            self.log.info("Documents successfully formatted")
            return formatted_docs
        except Exception as e:
            self.log.error(f"Error formatting documents: {e}")
            raise CustomException(f"Error formatting documents: {e}", sys)