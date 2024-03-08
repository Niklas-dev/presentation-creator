import argparse
from argparse import Namespace


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Create presentations easily')
        self.add_parser()

    def add_parser(self):
        self.parser.add_argument('--topic', help='The topic of your presentation')
        self.parser.add_argument('--subtopics_amount', help='The subtopic amount of your presentation')
        self.parser.add_argument('--length_minutes', help='The length of your presentation in minutes.')

    def get_args(self) -> Namespace:
        args = self.parser.parse_args()

        if args.topic is None:
            raise Exception("You need to pass in a topic: --topic <topic>")

        if args.subtopics_amount is None:
            raise Exception("You need to pass in a subtopics amount: --subtopics_amount <amount>")

        if args.length_minutes is None:
            raise Exception("You need to pass in a length: --length_minutes <minutes>")
        return args
