import os

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class BaseGenerator:
    def __init__(self):
        self.llm_template = ""
        self.human_template = ""

    @staticmethod
    def load_chat_model():
        llm = ChatGroq(
            temperature=0,
            model="mixtral-8x7b-32768",
        )

        return llm
    def create_chat_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", self.llm_template),
            ("human", self.human_template)
        ])
