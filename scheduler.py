import datetime
from typing import List

from config import Config
from data import Lesson, Schedule


class Scheduler:
    def __init__(self, config: Config, lessons: List[Lesson]):
        self.config = config
        self.minutes_per_count = self.config.minutes_per_count
        self.lessons = lessons
        self.total_time = self.calculate_total_time(0, len(self.lessons))
        self.schedules = []

    def calculate_total_time(self, start: int, end: int) -> datetime.timedelta:
        return sum((lesson.duration for lesson in self.lessons[start : end]), datetime.timedelta())

    def calculate_schedules(self):
        print("수강 일정을 계산합니다...")

        if len(self.lessons) < 1:
            raise ValueError("강의 정보가 존재하지 않습니다.")

        daily_limit = datetime.timedelta(minutes=self.minutes_per_count)
        current_sum = datetime.timedelta()
        start = 0
        count = 1

        # TODO
        for i, lesson in enumerate(self.lessons):
            if current_sum + lesson.duration > daily_limit:
                new_schedule = Schedule(count, self.lessons[start], self.lessons[i - 1], current_sum)
                self.schedules.append(new_schedule)
                start = i
                current_sum = lesson.duration
                count += 1
            else:
                current_sum += lesson.duration
        last_schedule = Schedule(count, self.lessons[start], self.lessons[len(self.lessons) - 1], current_sum)
        self.schedules.append(last_schedule)
        return self.schedules
