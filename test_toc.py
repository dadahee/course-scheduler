from datetime import datetime

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from main import fetch_course_with_lessons


def load_courses() -> list[str]:
    print("강의 목록을 불러옵니다...")
    COURSE_LIST_VIEW = "https://www.inflearn.com/courses?types=ONLINE"
    course_urls = []

    try:
        # 웹 드라이버 설정 (Chrome 사용)
        chromedriver_autoinstaller.install()

        # Selenium WebDriver 설정
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)


        # 인프런 강의 목록 페이지 열기
        driver.get(COURSE_LIST_VIEW)

        # 강의 목록이 로딩될 때까지 대기
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > main > section:nth-child(4) > ul > li')))

        # 모든 강의 카드 요소를 가져오기
        course_elements = driver.find_elements(By.CSS_SELECTOR, '#__next > main > section:nth-child(4) > ul > li')
        # 강의 URL 추출
        for course in course_elements:
            link_element = course.find_element(By.TAG_NAME, 'a')
            course_url = link_element.get_attribute('href')
            course_urls.append(course_url)

        # 브라우저 닫기
        driver.quit()
    finally:
        return course_urls


def crawl_course_urls_and_get_durations(urls: list) -> list:
    # 크롤링
    crawl_times = []
    crawl_result = []
    count_lessons = 0
    sum_course_minutes = 0
    fail_cases = 0
    for i in range(len(urls)):
        start_time = datetime.now()
        course_with_lessons = fetch_course_with_lessons(urls[i])
        end_time = datetime.now()
        crawl_seconds = (end_time - start_time).total_seconds()
        if not course_with_lessons.lessons or not course_with_lessons.name:
            fail_cases += 1
        else:
            total_course_minutes = sum([lesson.duration.total_seconds() for lesson in course_with_lessons.lessons]) // 60
            crawl_result.append(f"{i}. {course_with_lessons.name} (총 수업 시간 = {int(total_course_minutes // 60)}h {int(total_course_minutes % 60)}m, 수업 수 = {len(course_with_lessons.lessons)}개) / 크롤링 소요 시간 = {crawl_seconds}s")

            count_lessons += len(course_with_lessons.lessons)
            sum_course_minutes += total_course_minutes

        crawl_times.append(crawl_seconds)

    print("============= 크롤링 결과 =============")
    print("\n".join(crawl_result))

    if len(crawl_times) > 1:
        average_course_minutes = sum_course_minutes / (len(crawl_times) - fail_cases)
        average_lessons_count = count_lessons / len(crawl_times) - fail_cases

        print("============ 강의 분석 결과 ============")
        print(f"크롤링 실패: {fail_cases}건")
        print(f"평균 수업 수: {average_lessons_count}개")
        print(f"평균 강의 시간: {int(average_course_minutes // 60)}h {int(average_course_minutes % 60)}m")
    return crawl_times

def save_course_urls(course_urls: list, file_name: str) -> None:
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            for course_url in course_urls:
                f.write(f"{course_url}\n")
    except Exception:
        print("강의 URL 목록이 저장에 실패 했습니다.")
        exit()
    else:
        print("강의 URL 목록 저장이 완료 되었습니다.")

def load_course_urls(file_name: str) -> list:
    course_urls = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                content = line.strip()
                if content:
                    course_urls.append(content)
    except Exception as e:
        print("강의 URL 목록을 로드하는 데 실패했습니다.")
        print(e)
        exit()
    else:
        print("강의 URL 목록을 성공적으로 로드하였습니다.")
        return course_urls


if __name__ == '__main__':
    FILE_NAME = "outputs/sample.md"

    # 강의 URL 목록 크롤링
    # course_list = load_courses()
    # save_course_urls(course_list, FILE_NAME)

    # 강의 URL 목록 파일 이용
    course_urls = load_course_urls(FILE_NAME)

    total_times = crawl_course_urls_and_get_durations(course_urls)

    if len(total_times) > 0:
        total_times.sort()
        average_total_seconds = sum(total_times) / len(total_times)
        median_total_seconds = total_times[len(total_times) // 2] if len(total_times) % 2 != 0 else (total_times[len(total_times) // 2] + total_times[len(total_times) // 2 - 1]) / 2
        print("============ 크롤링 소요 시간 ============")
        print("크롤링 강의 수:", len(total_times))
        print("평균:", average_total_seconds)
        print("중위값:", median_total_seconds)
