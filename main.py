import argparse
from typing import List

from config import Config
from crawler import Crawler
from data import Course, Schedule
from file import Formatter, Exporter, Loader
from scheduler import Scheduler


def read_course(config: Config, filename: str) -> Course:
    loader = Loader(config)
    return loader.load_course(filename)

def fetch_course_with_lessons(url: str) -> Course:
    crawler = Crawler(url)
    return crawler.crawl_and_extract_course()

def extract_schedules(config: Config, course: Course) -> List[Schedule]:
    scheduler = Scheduler(config, course.lessons)
    schedules = scheduler.calculate_schedules()
    return schedules


def main():

    try:
        parser = argparse.ArgumentParser(description='Inflearn Course Scheduler')
        subparsers = parser.add_subparsers(dest='command')

        DEFAULT_CONFIG_FILENAME = 'config.json'

        TOC_OUTPUT = 'toc_output'
        SCHEDULE_OUTPUT = 'schedule_output'

        AUTO_COMMAND = 'auto'
        TOC_COMMAND = 'toc'
        SCHEDULE_COMMAND = 'schedule'

        CREATE_TOC_COMMAND = [TOC_COMMAND, AUTO_COMMAND]
        CREATE_SCHEDULE_COMMAND = [SCHEDULE_COMMAND]


        # toc+schedules 한 번에 명령어
        parser_auto = subparsers.add_parser(AUTO_COMMAND, help='강의 목차 추출 & 수강 일정 계산 & 파일 저장')
        parser_auto.add_argument('url', type=str, help='강의 URL')
        parser_auto.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILENAME, help='설정 파일 경로')
        parser_auto.add_argument('-o', '--out', type=str, help='수강 일정 파일명')

        # 강의 목차 추출 및 저장 명령어
        parser_toc = subparsers.add_parser(TOC_COMMAND, help='강의 목차 추출 및 저장')
        parser_toc.add_argument('url', type=str, help='강의 URL')
        parser_toc.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILENAME, help='설정 파일 경로')
        parser_toc.add_argument('-o', '--out', type=str, help='강의 목차 파일명')

        # 수강 일정 계산 및 저장 명령어
        parser_schedule = subparsers.add_parser(SCHEDULE_COMMAND, help='수강 일정 계산 및 저장')
        parser_schedule.add_argument('filename', type=str, help='강의 목차 파일명')
        parser_schedule.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILENAME, help='설정 파일 경로')
        parser_schedule.add_argument('-o', '--out', type=str, help='수강 일정 파일명')

        args = parser.parse_args()
        config = Config(args.config)
        formatter = Formatter(config)
        exporter = Exporter(formatter)

        output_filename = args.out

        print(f"{args.command} 작업을 시작합니다...")

        if args.command in CREATE_TOC_COMMAND:
            if not output_filename:
                output_filename = config.get_config_value(TOC_OUTPUT)
            course = fetch_course_with_lessons(args.url)
            exporter.save(course.name, course.lessons, output_filename)

        if args.command in CREATE_SCHEDULE_COMMAND:
            if not output_filename:
                output_filename = config.get_config_value(SCHEDULE_OUTPUT)
            course = read_course(config, args.filename)
            schedules = extract_schedules(config, course)
            exporter.save(course.name, schedules, output_filename)

        if (args.command not in CREATE_TOC_COMMAND) and (args.command not in CREATE_SCHEDULE_COMMAND):
            parser.print_help()

        print("작업을 종료합니다...")
    except SystemExit as e:
        print("작업을 중단합니다...")

if __name__ == '__main__':
    main()
