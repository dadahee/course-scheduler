import datetime


class Section:

    def __init__(self, index: int, title: str):
        self.index = index
        self.title = title

    def __str__(self):
        return f"{self.index:2}. {self.title}"


class Lesson:

    def __init__(self, section: Section, number: int, title: str, duration: str):
        self.section = section
        self.number = number
        self.title = title
        self.duration = self.parse_duration(duration)

    def __str__(self):
        return f"{self.section.index:2}.{self.number:2} {self.title} ({self.duration})"

    @staticmethod
    def parse_duration(duration_str: str) -> datetime.timedelta:
        time = [0, 0, 0]
        duration_meta = list(map(int, duration_str.split(":")))
        for i in range(len(duration_meta)):
            time[- i - 1] = duration_meta[- 1 - i]
        return datetime.timedelta(hours=time[0], minutes=time[1], seconds=time[2])
