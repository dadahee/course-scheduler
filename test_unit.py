from datetime import datetime

from main import fetch_course_with_lessons

def crawl_course(course_url: str) -> (float, bool):
    # 크롤링
    fail_cases = 0
    start_time = datetime.now()
    course_with_lessons = fetch_course_with_lessons(course_url)
    end_time = datetime.now()
    crawl_seconds = (end_time - start_time).total_seconds()

    if not course_with_lessons.lessons or not course_with_lessons.name:
        fail_cases += 1
    else:
        total_course_minutes = sum([lesson.duration.total_seconds() for lesson in course_with_lessons.lessons]) // 60
        print(f"{course_with_lessons.name} (총 수업 시간 = {int(total_course_minutes // 60)}h {int(total_course_minutes % 60)}m, 수업 수 = {len(course_with_lessons.lessons)}개) / 크롤링 소요 시간 = {crawl_seconds}s")
    return crawl_seconds, fail_cases == 0

if __name__ == '__main__':
    # (평균 길이 강의) 단건 크롤링 성능 테스트
    COURSE_URL = "https://www.inflearn.com/course/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D-%EC%A0%84%EC%B2%98%EB%A6%AC-%ED%8C%90%EB%8B%A4%EC%8A%A4-%EC%8B%9C%EA%B0%81%ED%99%94#curriculum"
    count = 0
    results = []

    while count < 5:
        count += 1
        required_seconds, successful = crawl_course(COURSE_URL)

        if successful:
            results.append(required_seconds)

    average_seconds = sum(results) / count
    print("============ 크롤러 실행 완료 ============")
    success_percent = (len(results) / count) * 100
    print(f"성공률: {success_percent}%")
    for i in range(len(results)):
        print(f"[{i + 1}차] 소요 시간: {results[i]}초")
    print(f"5회 평균 소요 시간: {average_seconds}초")
