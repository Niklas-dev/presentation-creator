from typing import List


def format_subtopics_llm_output(subtopics_string: str) -> List[str]:
    return subtopics_string.split("/")
