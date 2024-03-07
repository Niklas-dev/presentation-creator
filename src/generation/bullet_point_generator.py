import json
import os
from typing import List

from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class BulletPointGenerator:
    def __init__(self):
        self.llm_template = \
            (
                "You are now a presentation creator agent. You will just respond in the given scheme. You must follow "
                "this"
                "everytime. You are given a script that will be read at a presentation and you must transform this "
                "into short but informative bullet points. Make sure to answer with just the bullet points. You are "
                "also given the sub topic of the script so you are aware of the context. Make sure the bullet points "
                "include as much info as possible but leave something that can be said. The bullet point dont have to "
                "be full sentences all the time. the output scheme should be and must be followed: long bullet point "
                "one/another long"
                "bullet point/a cool bullet point three. Make sure you use the slash as separation so I can later "
                "format the bullet points how I want to. So I repeat: point one/point two/point three/ and so on. "
                "THIS IS VERY IMPORTANT. The bullet points shouldn't be too long, this means a maximum of 10 words "
                "per point."
            )
        self.human_template = "the script: {script} the sub topic: {subtopic}"

        self.bullet_points_text = None

    @staticmethod
    def load_chat_model():
        return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                          model_name="gpt-3.5-turbo")

    def create_chat_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", self.llm_template),
            ("human", self.human_template)
        ])

    def clear_output_text(self):
        self.bullet_points_text = None

    def generate(self, script: str, sub_topic: str):
        chat_model = self.load_chat_model()

        chat_prompt = self.create_chat_prompt()

        formatted_prompt = chat_prompt.format_messages(script=script, subtopic=sub_topic)
        result = chat_model.invoke(formatted_prompt)

        self.bullet_points_text = result.content
