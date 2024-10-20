import time
import sys
from langchain_groq import ChatGroq
from langchain.memory import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from .config import TypewriterCallbackHandler

class LangChainChatbot:
    def __init__(self, model_name="mixtral-8x7b-32768", temperature=0):
        self.llm = ChatGroq(
            model_name=model_name, temperature=temperature, streaming=True,
            callbacks=[TypewriterCallbackHandler()]
        )
        self.context = ""
        self.history = ChatMessageHistory()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Use the following context: {context}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.chain = self.prompt | self.llm
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain, lambda session_id: self.history,
            input_messages_key="input", history_messages_key="history"
        )

    def set_paragraph(self, paragraph):
        self.context = paragraph

    def answer_question(self, question):
        if not question.strip():
            raise ValueError("Question cannot be empty")
        if len(question) > 500:
            raise ValueError("Question is too long (max 500 characters)")
        response = self.chain_with_history.invoke(
            {"input": question, "context": self.context},
            config={"configurable": {"session_id": "chatbot"}}
        )
        return response.content
