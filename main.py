import argparse
from config import Config
from crawler import Crawler
from scheduler import Scheduler
from file import Exporter, Loader

def main():
    parser = argparse.ArgumentParser(description='Inflearn Course Scheduler')
    subparsers = parser.add_subparsers(dest='command')

    DEFAULT_CONFIG_FILENAME = 'config.json'

    TOC_OUTPUT = 'toc_output'
    SCHEDULE_OUTPUT = 'schedule_output'

    # toc+schedule 한 번에 명령어
    parser_auto = subparsers.add_parser('auto', help='강의 목차 추출 & 수강 일정 계산 & 파일 저장')
    parser_auto.add_argument('url', type=str, help='강의 URL')
    parser_auto.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILENAME, help='설정 파일 경로')
    parser_auto.add_argument('-o', '--out', type=str, help='수강 일정 파일명')

    # 강의 목차 추출 및 저장 명령어
    parser_toc = subparsers.add_parser('toc', help='강의 목차 추출 및 저장')
    parser_toc.add_argument('url', type=str, help='강의 URL')
    parser_toc.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILENAME, help='설정 파일 경로')
    parser_toc.add_argument('-o', '--out', type=str, help='강의 목차 파일명')

    # 수강 일정 계산 및 저장 명령어
    parser_schedule = subparsers.add_parser('schedule', help='수강 일정 계산 및 저장')
    parser_schedule.add_argument('filename', type=str, help='강의 목차 파일명')
    parser_schedule.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILENAME, help='설정 파일 경로')
    parser_schedule.add_argument('-o', '--out', type=str, help='수강 일정 파일명')

    args = parser.parse_args()
    config = Config(args.config)
    exporter = Exporter(config)

    if args.command == 'schedule':
        output_file = args.out if args.out else config.get_config_value(SCHEDULE_OUTPUT)
        toc_file = args.filename if args.filename else config.get_config_value(TOC_OUTPUT)
        loader = Loader()
        toc = loader.read_course_data(toc_file)
        scheduler = Scheduler(config, toc)
        schedules = scheduler.calculate_schedules()
        exporter.save_schedules(schedules, output_file)
    elif args.command == 'toc':
        output_file = args.out if args.out else config.get_config_value(TOC_OUTPUT)
        crawler = Crawler(args.url)
        toc = crawler.crawl_and_extract_curriculum()
        exporter.save_lessons(toc, output_file)
    elif args.command == 'auto':
        toc_output_file = config.get_config_value('toc_output')
        schedule_output_file = args.out if args.out else config.get_config_value('schedule_output')
        # toc
        crawler = Crawler(args.url)
        toc = crawler.crawl_and_extract_curriculum()
        exporter.save_lessons(toc, toc_output_file)
        # schedule
        scheduler = Scheduler(config, toc)
        schedule = scheduler.calculate_schedules()
        exporter.save_schedules(schedule, schedule_output_file)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
