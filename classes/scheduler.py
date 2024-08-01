import datetime
from typing import List

from classes.config import Config
from classes.lesson import Lesson

class Scheduler:
    def __init__(self, course_url: str, config: Config, lessons: List[Lesson]):
        self.course_url = course_url
        self.config = config
        self.minutes_per_count = self.config.minutes_per_count
        self.course_data = lessons
        self.total_time = self.calculate_total_time()
        self.ranges = self.calculate_ranges()

    def calculate_total_time(self) -> datetime.timedelta:
        return sum((lesson.duration for lesson in self.course_data), datetime.timedelta())

    def calculate_ranges(self) -> List[tuple]:
        ranges = []
        daily_limit = datetime.timedelta(minutes=self.minutes_per_count)
        current_sum = datetime.timedelta()
        start = 0

        for i, lesson in enumerate(self.course_data):
            if current_sum + lesson.duration > daily_limit:
                ranges.append((start, i - 1))
                start = i
                current_sum = lesson.duration
            else:
                current_sum += lesson.duration
        ranges.append((start, len(self.course_data) - 1))

        return ranges

    def format_schedules(self) -> str:
        formatter = Scheduler.ScheduleRangeFormatter(self.config)
        output = [formatter.format_range(count, self.course_data[start], self.course_data[end],
                                         sum((lesson.duration for lesson in self.course_data[start:end + 1]),
                                             datetime.timedelta()))
                  for count, (start, end) in enumerate(self.ranges, start=1)]
        return "\n".join(output)

    class ScheduleRangeFormatter:
        def __init__(self, config):
            self.config = config

        def format_range(self, count, start_lesson, end_lesson, total_duration):
            count_str = self.format_count(count)
            start_lesson_str = self.format_lesson(start_lesson, self.config.enable_start_title)
            end_lesson_str = self.format_lesson(end_lesson, self.config.enable_end_title)

            range_separator = self.config.range_separator
            duration_str = self.format_duration(total_duration)

            range_str = [part for part in [count_str, start_lesson_str, range_separator, end_lesson_str, duration_str]
                         if part]
            return " ".join(range_str).strip()

        def format_count(self, count):
            if not self.config.enable_count:
                return ''
            return self.config.count_format_str.format(count=count)

        def format_lesson(self, lesson: Lesson, enable_title: bool) -> str:
            lesson_info = self.config.index_format_str.format(section=lesson.section.index,
                                                              number=lesson.number)
            if enable_title:
                lesson_info += " " + lesson.title
            return lesson_info

        def format_duration(self, duration):
            if not self.config.enable_duration:
                return ''
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_format = self.config.duration_format_str
            return duration_format.format(hh=hours, mm=minutes, ss=seconds)
