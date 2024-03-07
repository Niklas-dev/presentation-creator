from dotenv import load_dotenv
from pptx.util import Pt

from src.generation.bullet_point_generator import BulletPointGenerator
from src.generation.content_generator import ContentGenerator
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

        slide_layout = prs.slide_layouts[1]  # Title and content layout
        slide = prs.slides.add_slide(slide_layout)

        # Set title
        title = slide.shapes.title
        title.text = subtopic

        title_text_frame = title.text_frame
        title_text_frame.paragraphs[0].font.size = Pt(16)

        # Add bullet points
        content_placeholder = slide.placeholders[1]  # Index 1 is the content placeholder

        content_text_frame = content_placeholder.text_frame

        filtered_bullet_points = list(filter(None, bullet_point_generator.bullet_points_text.split("- ")))

        for point in filtered_bullet_points:
            p = content_text_frame.add_paragraph()

            p.text = point.removesuffix('\n')

            print(point.removesuffix('\n'))

        for paragraph in range(len(content_text_frame.paragraphs)):
            content_text_frame.paragraphs[paragraph].font.size = Pt(10)

        prs.save("./output/multiple_slides.pptx")

        content_generator.clear_output_text()

        print("-------------------------------------------------------------------------- \n ")
