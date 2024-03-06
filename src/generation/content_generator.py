import json
import os
from typing import List

from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class ContentGenerator:
    def __init__(self):
        self.llm_template = \
            (
                "You are now a presentation creator agent. You will just respond in the given scheme. You must follow "
                "this"
                "everytime. You are given a topic that was previously created by another agent that generated several "
                "of them. You should research and write content for the given topic which will be later connected "
                "to the other topics. Your main focus should be on the sub topics but will also get the main topic as "
                "context, the amount of other sub topics and the required length in minutes of the whole presentation "
                "so you can fulfill your task as best as you can. Make sure you gather enough content to fill the "
                "presentation with quality information. In the end you should just return the generated text and "
                "return a continuous text with the sub topic as a heading at the top. Make sure the text is content "
                "rich and not just scratching the surface of the given sub topic. I will later transform this text "
                "into bullet points, so you must make sure it has a lot of value."
            )
        self.human_template = ("your sub topic to focus on: {sub_topic} the main topic for context: {topic} the "
                               "amount of other sub topics: {subtopics_amount} the required full length of the "
                               "presentation in minutes {length_minutes}")

        self.subtopics_text = None

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
        self.subtopics_text = None

    def generate(self, sub_topic: str, topic: str, subtopics_amount: int, length_minutes: int):
        chat_model = self.load_chat_model()

        chat_prompt = self.create_chat_prompt()

        formatted_prompt = chat_prompt.format_messages(sub_topic=sub_topic, topic=topic,
                                                       subtopics_amount=subtopics_amount - 1,
                                                       length_minutes=length_minutes)
        result = chat_model.invoke(formatted_prompt)

        self.subtopics_text = result.content
