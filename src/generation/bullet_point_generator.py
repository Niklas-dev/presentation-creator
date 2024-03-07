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
                "You are now a presentation creator agent. You will just respond in the given scheme. You task is to "
                "transform the text you are given into bullet points Make sure the bullet points are "
                "not longer than 10 words but are still informative and precise. You must always follow the / "
                "separation format as I can just continue with the formatting if the output has the correct format. "
                "Also maintain the language in the bullet points that was used in the given text. Thank You."


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
