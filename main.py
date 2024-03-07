from dotenv import load_dotenv
from pptx.util import Pt

from src.generation.bullet_point_generator import BulletPointGenerator
from src.generation.content_generator import ContentGenerator
from src.generation.powerpoint_generator import PowerPointGenerator
from src.generation.topic_generator import TopicGenerator
from pptx import Presentation

load_dotenv()
prs = Presentation()

input_topic = "Die DDR im Warschauer Pakt und im Rat für gegenseitige Wirtschaftshilfe"
input_subtopics_amount = 10
input_length_minutes = 20

topic_generator = TopicGenerator()

topic_generator.generate(topic=input_topic, subtopics_amount=input_subtopics_amount,
                         length_minutes=input_length_minutes)

print(topic_generator.subtopics_array)

content_generator = ContentGenerator()
bullet_point_generator = BulletPointGenerator()
powerpoint_generator = PowerPointGenerator()
script_save = None
with open('./output/output.txt', 'a', encoding="utf-8") as file:
    for subtopic in topic_generator.subtopics_array:
        content_generator.generate(sub_topic=subtopic, topic=input_topic, subtopics_amount=input_subtopics_amount,
                                   length_minutes=input_length_minutes, first_script=script_save)

        bullet_point_generator.generate(script=content_generator.subtopics_text, sub_topic=subtopic)

        if script_save is None:
            script_save = content_generator.subtopics_text

        file.write(content_generator.subtopics_text)
        file.write("\n-------------------------------------------------\n")

        slide = powerpoint_generator.add_slide()

        powerpoint_generator.add_title(topic_title=subtopic, slide=slide)

        powerpoint_generator.add_bullet_points(points_array=list(filter(None, bullet_point_generator.bullet_points_text.split("- "))), slide=slide)

        powerpoint_generator.save_pptx("./output/multiple_slides.pptx")

        content_generator.clear_output_text()

        print("-------------------------------------------------------------------------- \n ")
