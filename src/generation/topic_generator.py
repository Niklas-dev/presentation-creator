import json
import os
from typing import List

from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from ..formatters.output_formatting import format_subtopics_llm_output

load_dotenv()


class TopicGenerator:
    def __init__(self):
        self.subtopics_string = None
        self.llm_template = \
            (
                "You are now a presentation creator agent. You will just respond in the given scheme. You must follow "
                "this"
                "everytime. You are given a Topic and how many sub topics you should create, you are also given the "
                "expected"
                "length of the topic in minutes so you must think about the sub topic to fill the time frame. Your "
                "output"
                "should be the list of topics in this format: long topic one/long topic 2/another cool topic. Lets "
                "say you"
                "get tennis as the topic with 3 sub topics and 5 minutes you could create this output: All important "
                "tournaments/The rules of tennis/The best players in history. Make sure the sub topics are not too "
                "short and"
                "easy for another agent to research and generate content for. Make sure the sub topics allow a high "
                "level"
                "presentation."
            )
        self.human_template = ("the topic: {topic} subtopic amount: {subtopics_amount} the time length: {"
                               "length_minutes} in minutes")

        self.subtopics_array = None

    @staticmethod
    def load_chat_model():
        return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                          model_name="gpt-3.5-turbo")

    @staticmethod
    def format_subtopics(subtopics_string) -> List[str]:
        print("Formatting topics")
        return format_subtopics_llm_output(subtopics_string=subtopics_string)

    def create_chat_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", self.llm_template),
            ("human", self.human_template)
        ])

    def generate(self, topic: str, subtopics_amount: int, length_minutes: int):
        chat_model = self.load_chat_model()

        chat_prompt = self.create_chat_prompt()

        formatted_prompt = chat_prompt.format_messages(topic=topic, subtopics_amount=subtopics_amount,
                                                       length_minutes=length_minutes)
        result = chat_model.invoke(formatted_prompt)

        output_array = self.format_subtopics(subtopics_string=result.content)

        self.subtopics_array = output_array
