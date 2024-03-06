from dotenv import load_dotenv

from src.generation.bullet_point_generator import BulletPointGenerator
from src.generation.content_generator import ContentGenerator
from src.generation.topic_generator import TopicGenerator

load_dotenv()

input_topic = "Rolle der DDR im Warschauer Pakt und im Rat für gegenseitige Wirtschaftshilfe(Comecon)"
input_subtopics_amount = 4
input_length_minutes = 15

topic_generator = TopicGenerator()

topic_generator.generate(topic=input_topic, subtopics_amount=input_subtopics_amount,
                         length_minutes=input_length_minutes)

print(topic_generator.subtopics_array)

content_generator = ContentGenerator()
bullet_point_generator = BulletPointGenerator()
script_save = None
with open('./output/output.txt', 'a', encoding="utf-8") as file:
    for subtopic in topic_generator.subtopics_array:
        content_generator.generate(sub_topic=subtopic, topic=input_topic, subtopics_amount=input_subtopics_amount,
                                   length_minutes=input_length_minutes, first_script=script_save)

        bullet_point_generator.generate(script=content_generator.subtopics_text, sub_topic=subtopic)

        print(bullet_point_generator.bullet_points_text)
        if script_save is None:
            script_save = content_generator.subtopics_text

        file.write(bullet_point_generator.bullet_points_text)
        file.write("\n-------------------------------------------------\n")
        content_generator.clear_output_text()

        print("-------------------------------------------------------------------------- \n ")
