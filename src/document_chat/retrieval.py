from multiprocessing.managers import BaseManager
from langchain_core.messages import BaseMessage
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from typing import Optional,List
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from utils.model_utils import ModelLoader
from prompt.prompt_analyzer import PROMPT_REGISTRY
from model.base_model import PromptType,SummaryResponse
from pathlib import Path
import sys
from langchain_core.documents import Document
from operator import itemgetter
from dotenv import load_dotenv

load_dotenv()


class ConversationalRAG:
    def __init__(self, retriver, session_id: str = None):
        """
        Initializes the DocumentRetriever with the path for the FAISS index.
        :param faiss_index_path: Directory where FAISS index is stored.
        :param session_id: Unique identifier for the session, defaults to current timestamp.
        """
        try:
            
            self.retriver = retriver
            self.parser = StrOutputParser()
            self.session_id = session_id or "document_chat_session"
            self.model = ModelLoader()
            self.llm = self.model.load_llm()
            self.embeddings = self.model.load_embedding()
            self.qa_prompt = PROMPT_REGISTRY.get(PromptType.CONTEXT_QA.value)
            self.rewriter_prompt = PROMPT_REGISTRY.get(PromptType.CONTEXTUALIZE_QUESTION.value)

            log.info("DocumentRetriever successfully initialized")
            self._built_lcel_chain()
        except Exception as e:
            log.error("Error in initialization DocumentRetriever")
            raise (e, sys)
        

    def Invoke(self,user_query:str,chat_history:Optional[List[BaseMessage]]=None):
        try:
            if self.main_chain is None:
                raise CustomException(
                    "RAG chain not initialized. Call load_retriever_from_faiss() before invoke().", sys)
            self.chat_history = chat_history or []
            self.payload = {"user_input":user_query, "chat_history":self.chat_history}

            if self.retriver is None:
                #retriver = self._create_retrivel(self.documents)
                log.error("Retriever is not initialized")
                raise CustomException("Retriever is not initialized", sys)
            rewritten = self.question_rewritter.invoke(self.payload)
            log.info(f"Rewritten question: {rewritten}")
            if not rewritten or not rewritten.strip():
               rewritten = user_query   # fallback: use original

            docs = self.retriver.invoke(rewritten) if self.retriver else []
            log.info(f"Retrieved {len(docs)} documents")
            if docs:
                context = self._format_doc(docs)
            else:
                context = "No relevant context available."

            final_payload = {
             "context": context,
             "user_input": user_query,
            "chat_history": chat_history or []
           }

            response = self.main_chain.invoke(final_payload)
            log.info("Successfully generated answer from DocumentRetriever")
            return response
        except Exception as e:
            log.error("Error in invoking DocumentRetriever")
            raise CustomException(f"Error generating answer in invoke: {e}", sys)


    def _create_retrivel(self,documents):
        """
        Builds a LangChain retriever using the provided documents.
        :param documents: List of Document objects to be used for retrieval.
        :return: A LangChain retriever object.
        """
        try:
            if not documents:
                raise CustomException("No documents provided for retrieval", sys)
            log.info("Building LangChain retriever")
            vector_store = FAISS.from_documents(documents, self.embeddings)
            retriever = vector_store.as_retriever(search_kwargs={"k": 5})
            log.info("LangChain retriever successfully built")
            return retriever
        except Exception as e:
            log.error(f"Error building LangChain retriever: {e}")
            raise CustomException(f"Error building LangChain retriever: {e}", sys)
        


    def _built_lcel_chain(self):
        try:
            # 1) Rewrite user question with chat history context
            self.question_rewritter = {"user_input":itemgetter("user_input"),"chat_history":itemgetter("chat_history")} | self.rewriter_prompt | self.llm | self.parser
            log.info("Question rewriting chain successfully built")
            
            # 2) Main chain that combines the rewritten question, retrieved documents, and chat history
            self.main_chain = {"context": itemgetter("context"),"user_input":itemgetter("user_input"),"chat_history":itemgetter("chat_history")} | self.qa_prompt | self.llm | self.parser
            log.info("Main lcel chain successfully built")
        except:
            log.error("Error building LCEL chain")
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
            log.info("Formatting retrieved documents")
            formatted_docs = "\n\n".join([doc.page_content for doc in docs])
            log.info("Documents successfully formatted")
            return formatted_docs
        except Exception as e:
            log.error(f"Error formatting documents: {e}")
            raise CustomException(f"Error formatting documents: {e}", sys)
        



