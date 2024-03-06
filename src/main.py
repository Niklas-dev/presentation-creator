import json
import os
from typing import List

from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
chat_model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                        model_name="gpt-3.5-turbo")

template = \
    (
        "You are now a presentation creator agent. You will just respond in the given scheme. You must follow this "
        "everytime. You are given a Topic and how many sub topics you should create, you are also given the expected "
        "length of the topic in minutes so you must think about the sub topic to fill the time frame. Your output "
        "should be the list of topics in this format: long topic one/long topic 2/another cool topic. Lets say you "
        "get tennis as the topic with 3 sub topics and 5 minutes you could create this output: All important "
        "tournaments/The rules of tennis/The best players in history. Make sure the sub topics are not too short and "
        "easy for another agent to research and generate content for. Make sure the sub topics allow a high level "
        "presentation."
    )
human_template = "the topic: {topic} subtopic amount: {subtopics_amount} the time length: {length_minutes} in minutes"
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

formatted_prompt = chat_prompt.format_messages(topic="Die DDR, Der Warschauer Pakt im Kontext von Nationen",
                                               subtopics_amount=10, length_minutes="15")
result = chat_model.invoke(formatted_prompt)

# json_result = json.loads(result.content)




def format_subtopics_to_array(subtopics_string: str) -> List[str]:
    return subtopics_string.split("/")


print(format_subtopics_to_array(result.content))
