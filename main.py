from dotenv import load_dotenv

from src.generation.content_generator import ContentGenerator
from src.generation.topic_generator import TopicGenerator

load_dotenv()

input_topic = "DDR, Der Warschauer Pakt im Kontext von Nationen"
input_subtopics_amount = 3
input_length_minutes = 5

topic_generator = TopicGenerator()

topic_generator.generate(topic=input_topic, subtopics_amount=input_subtopics_amount,
                         length_minutes=input_length_minutes)

print(topic_generator.subtopics_array)

content_generator = ContentGenerator()
with open('./output/output.txt', 'a', encoding="utf-8") as file:
    for subtopic in topic_generator.subtopics_array:
        content_generator.generate(sub_topic=subtopic, topic=input_topic, subtopics_amount=input_subtopics_amount,
                                   length_minutes=input_length_minutes)

        print(content_generator.subtopics_text)

        file.write(content_generator.subtopics_text)
        content_generator.clear_output_text()

        print("-------------------------------------------------------------------------- \n ")
