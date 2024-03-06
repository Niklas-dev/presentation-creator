from dotenv import load_dotenv

from src.generation.topic_generator import TopicGenerator

load_dotenv()


topic_generator = TopicGenerator()

topic_generator.generate()

print(topic_generator.subtopics_array)


