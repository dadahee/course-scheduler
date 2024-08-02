import datetime
from typing import List


class Section:

    def __init__(self, index: int, title: str):
        self.index = index
        self.title = title

    def __str__(self):
        return f"{self.index:0>2}. {self.title}"


class Lesson:

    def __init__(self, section: Section, number: int, title: str, duration: str):
        self.section = section
        self.number = number
        self.title = title
        self.duration = self.parse_duration(duration)

    def __str__(self):
        return f"{self.section.index:0>2}.{self.number:0>2} {self.title} ({self.duration})"

    @staticmethod
    def parse_duration(duration_str: str) -> datetime.timedelta:
        time = [0, 0, 0]
        duration_meta = list(map(int, duration_str.split(":")))
        for i in range(len(duration_meta)):
            time[- i - 1] = duration_meta[- 1 - i]
        return datetime.timedelta(hours=time[0], minutes=time[1], seconds=time[2])


class Schedule:

    def __init__(self, count: int, start_lesson: Lesson, end_lesson: Lesson, duration: datetime.timedelta):
        self.count = count
        self.start_lesson = start_lesson
        self.end_lesson = end_lesson
        self.duration = duration


class Course:
    name: str
    lessons: List[Lesson]

    def __init__(self, name:str, lessons: List[Lesson]):
        self.name = name
        self.lessons = lessons
