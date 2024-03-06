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
                "of them. You should write a script that I can read out and will contain all information that you "
                "have gathered. Make sure that the content can be alter transformed into bullet points but should be "
                "a continues text/script for now. Its important that a lot of quality information is included and not "
                "just the surface. Each part will be alter "
                "connected to form the full presentation. So it should include information and some slight evaluation "
                "but not introduction or conclusion. It should be able to suite well between the other content. So No "
                "specific end sentence. You must use the language that was used for the sub topic input for the "
                "writing of the script, Dont assume to write in english if the input topic was written in another "
                "language for example german or others. ALso make sure to write the script with information specific "
                "for the sub topic to avoid duplication. Also add the sub topic at the top of the script and avoid "
                "bold text. Its a must to just write the script about the given sub topic and dont include other "
                "information as they are given in other sub topic scripts. DONT GIVE A GENERAL INTRO TO THE TOPIC "
                "AGAIN JUST WRITE ABOUT THE GIVEN SUB TOPIC OR THIS WILL FAIL. THANK YOU! DONT DO BULLET POINTS, WRITE "
                "A SCRIPT THAT CAN BE READ AND CONTAINS ALL INFORMATION! I will also give you the first created sub "
                "topic script so you can make sure to avoid duplication, if its empty you are currently writing the "
                "first sub topic script. Make sure you search for historic sources so you can provide deep knowledge "
                "and not just common info."
            )
        self.human_template = ("your sub topic to focus on: {sub_topic} the main topic for context: {topic} the "
                               "amount of other sub topics: {subtopics_amount} the required full length of the "
                               "presentation in minutes: {length_minutes} the script of the last subtopic: {first_script}")

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

    def generate(self, sub_topic: str, topic: str, subtopics_amount: int, length_minutes: int, first_script: str):
        chat_model = self.load_chat_model()

        chat_prompt = self.create_chat_prompt()

        formatted_prompt = chat_prompt.format_messages(sub_topic=sub_topic, topic=topic,
                                                       subtopics_amount=subtopics_amount - 1,
                                                       length_minutes=length_minutes, first_script=first_script)
        result = chat_model.invoke(formatted_prompt)

        self.subtopics_text = result.content
