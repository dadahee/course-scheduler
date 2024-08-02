import datetime
import re
from typing import List, Type

from config import Config
from data import Lesson, Section, Schedule, Course
from operation import areInstances


class Formatter:
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
        lesson_info = self.config.lesson_index_format_str.format(section=lesson.section.index,
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

    def format_section(self, section: Section) -> str:
        section_index = self.config.section_index_format_str.format(section=section.index)
        return f"{section_index} {section.title}"

    def enable_course_title(self):
        return self.config.include_course_name_header


class Exporter:
    def __init__(self, formatter: Formatter):
        self.formatter = formatter

    def save(self, course_name, data: List, filename: str):
        if areInstances(data, Lesson):
            self.save_lessons(course_name, data, filename)
        elif areInstances(data, Schedule):
            self.save_schedules(course_name, data, filename)

    def save_lessons(self, course_name: str, lessons: List[Lesson], filename: str):
        print(f"강의 목차를 {filename}에 저장합니다...")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if course_name and self.formatter.enable_course_title():
                    f.write(f"# {course_name}\n")
                for lesson in lessons:
                    if lesson.number == 1:
                        section = lesson.section
                        if section.index != 1:
                            f.write("\n")
                        f.write(f"## {self.formatter.format_section(section)}\n")
                    f.write(f"- {self.formatter.format_lesson(lesson, True, True)}  \n")
        except Exception:
            print("강의 목차 파일 저장에 실패하였습니다!")
            exit()
        else:
            print("강의 목차가 저장되었습니다!")

    def save_schedules(self, course_name: str, schedules: List[Schedule], filename: str):
        print(f"수강 일정을 {filename}에 저장합니다...")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if course_name and self.formatter.enable_course_title():
                    f.write(f"# {course_name}\n\n")
                for schedule in schedules:
                    f.write(f"- {self.formatter.format_schedule(schedule)}  \n")
        except Exception:
            print("수강 일정 파일 저장에 실패하였습니다!")
            exit()
        else:
            print("수강 일정이 저장되었습니다!")


class Loader:

    def __init__(self, config: Config):
        self.config = config

    def split_by_braces(self, input_string: str) -> List[str]:
        # 정규 표현식을 사용하여 {} 블록을 찾아 분리
        pattern = r'\{[^\{\}]+\}'
        matches = re.findall(pattern, input_string)
        if matches:
            parts = re.split(pattern, input_string)
            return [part for part in parts if part]
        return []

    def extract_and_parse_time_string(self, input_str: str, pattern: str) -> (str, dict[str, str]):
        # 정규 표현식 패턴 생성
        regex_pattern = re.sub(r'\{hh[^\{\}]*\}', r'(?P<hh>\\d{1,2})', pattern)
        regex_pattern = re.sub(r'\{mm[^\{\}]*\}', r'(?P<mm>\\d{1,2})', regex_pattern)
        regex_pattern = re.sub(r'\{ss[^\{\}]*\}', r'(?P<ss>\\d{1,2})', regex_pattern)

        match = re.search(regex_pattern, input_str)
        if match:
            time_dict = match.groupdict()
            prefix = input_str[:match.start() - 1]
            return prefix.strip(), time_dict
        return None, None

    def time_dict_to_standard_format(self, time_dict: dict[str, str]) -> str:
        hh = time_dict.get('hh', '00')
        mm = time_dict.get('mm', '00')
        ss = time_dict.get('ss', '00')
        return f"{hh:0>2}:{mm:0>2}:{ss:0>2}"

    def load_course(self, course_file: str) -> Course:
        print(f"강의 목차 파일 {course_file}을 로드합니다...")
        course_name = ""
        lessons = []
        try:
            section_format = re.sub(r'\{section[^\{\}]*\}', r'(\\d{1,2})', self.config.section_index_format_str)

            lesson_meta = self.split_by_braces(self.config.lesson_index_format_str)
            lesson_format = lesson_meta[0] if len(lesson_meta) > 0 else ''
            lesson_subformat = lesson_meta[1] if len(lesson_meta) > 1 else ''
            duration_format = self.config.duration_format_str

            with open(course_file, 'r', encoding='utf-8') as file:
                section = None
                for line in file:
                    content = line.strip()
                    if content:
                        COURSE_PREFIX_PAATERN = r'#'
                        SECTION_PREFIX_PATTERN = r'##+'
                        TITLE_PATTERN = r'(.+)'

                        section_match = re.match(f"{SECTION_PREFIX_PATTERN} {section_format} {TITLE_PATTERN}", content)
                        course_match = re.match(f"{COURSE_PREFIX_PAATERN} {TITLE_PATTERN}", content)
                        if section_match:
                            section = int(section_match.group(1))
                            title = section_match.group(2)
                            section = Section(section, title)
                        elif course_match:
                            course_name = course_match.group(1)
                            print(f"<{course_name}> 깅의 목차를 파싱합니다...")
                        else:
                            MARKDOWN_PREFIX_PATTERN = r'- '
                            INDEX_PATTERN = r'(\d{1,2})'
                            lesson_pattern = f'{MARKDOWN_PREFIX_PATTERN}{INDEX_PATTERN}{lesson_format}{INDEX_PATTERN}{lesson_subformat} {TITLE_PATTERN}'
                            match = re.match(lesson_pattern, content)
                            if match:
                                lesson_index = int(match.group(2))
                                lesson_content = match.group(3)
                                title, time_dict = self.extract_and_parse_time_string(lesson_content, duration_format)
                                if not time_dict:
                                    raise Exception(f"강의 시간을 찾을 수 없습니다. >>> {content}")
                                lesson = Lesson(section, lesson_index, title, self.time_dict_to_standard_format(time_dict))
                                lessons.append(lesson)
        except Exception as e:
            print("강의 목차를 불러오는 데 실패 했습니다.")
            print(e)
            exit()
        else:
            print("강의 목차 파싱이 완료되었습니다.")
            return Course(course_name, lessons)
