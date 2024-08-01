import datetime
import re
from typing import List

from src.config import Config
from src.data import Lesson, Section, Schedule


class Exporter:
    def __init__(self, config: Config):
        self.config = config

    def format_schedule(self, schedule: Schedule) -> str:
        count_str = self.format_count(schedule.count)
        start_lesson_str = self.format_lesson(schedule.start_lesson, self.config.enable_start_title, False)
        end_lesson_str = self.format_lesson(schedule.end_lesson, self.config.enable_end_title, False)

        range_separator = self.config.range_separator
        duration_str = self.format_duration(schedule.duration)

        range_str = [part for part in [count_str, start_lesson_str, range_separator, end_lesson_str, duration_str]
                     if part]
        return " ".join(range_str).strip()

    def format_count(self, count):
        if not self.config.enable_count:
            return ''
        return self.config.count_format_str.format(count=count)

    def format_lesson(self, lesson: Lesson, enable_title: bool, enable_duration: bool) -> str:
        lesson_info = self.config.index_format_str.format(section=lesson.section.index,
                                                          number=lesson.number)
        if enable_title:
            lesson_info += " " + lesson.title
        if enable_duration:
            lesson_info += " " + self.format_duration(lesson.duration)
        return lesson_info

    def format_duration(self, duration: datetime.timedelta) -> str:
        if not self.config.enable_duration:
            return ''
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_format = self.config.duration_format_str
        return duration_format.format(hh=hours, mm=minutes, ss=seconds)

    def export_lessons(self, lessons: List[Lesson], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            for lesson in lessons:
                if lesson.number == 1:
                    section = lesson.section
                    if section.index != 1:
                        f.write("\n")
                    f.write(f"## {section}\n")
                f.write(f"- {self.format_lesson(lesson, True, True)}  \n")

    def export_schedules(self, schedules: List[Schedule], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            for schedule in schedules:
                f.write(f"- {self.format_schedule(schedule)}  \n")


class Loader:

    def __init__(self, course_file: str):
        self.lessons = self.load_course_data(course_file)

    def load_course_data(self, course_file: str):
        lessons = []
        with open(course_file, 'r', encoding='utf-8') as file:
            section = None
            for line in file:
                main_match = re.match(r'(\d{2})\. (.+)', line.strip())
                if main_match:
                    section = int(main_match.group(1))
                    title = main_match.group(2)
                    section = Section(section, title)
                else:
                    match = re.match(r'\d{2}\.(\d{2}) (.+) \(((\d[2]:)?\d{2}:\d{2})\)', line.strip())
                    if match:
                        index = int(match.group(1))
                        title = match.group(2)
                        duration = match.group(3)
                        lesson = Lesson(section, index, title, duration)
                        lessons.append(lesson)
        return lessons
