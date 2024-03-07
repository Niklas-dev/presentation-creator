import os

from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate


class BaseGenerator:
    def __init__(self):
        self.llm_template = ""
        self.human_template = ""

    @staticmethod
    def load_chat_model():
        return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                          model_name="gpt-3.5-turbo")

    def create_chat_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", self.llm_template),
            ("human", self.human_template)
        ])

