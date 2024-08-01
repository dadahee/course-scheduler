import datetime
import re
from typing import List

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from data import Lesson, Section


class Crawler:

    def __init__(self, url: str):
        self.driver = None
        self.lessons = []
        self.url = url
        self.init_driver()

    def init_driver(self):
        # ChromeDriver 자동 설치
        chromedriver_autoinstaller.install()
        # Selenium WebDriver 설정
        options = Options()
        options.headless = True
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    def crawl_and_extract_curriculum(self):
        print("크롤링을 시작합니다...")
        start_time = datetime.datetime.now()
        attached_contents = 0
        course_title = "unknown"

        try:
            # 페이지 열기
            self.driver.get(self.url)

            # 강의 제목 크롤링
            course_title_element = self.driver.find_element(By.CSS_SELECTOR, 'h1.mantine-Title-root')
            course_title = course_title_element.text

            print(f"<{course_title}> 강의를 불러옵니다...")

            wait = WebDriverWait(self.driver, 3)

            try:
                print("목차를 불러옵니다...")

                # "모두 펼치기" 버튼 찾기
                expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="모두 펼치기"]]')))
                attempts = 0
                while attempts < 5:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expand_button)
                        time.sleep(0.5)  # 잠시 대기
                        expand_button.click()
                        break
                    except:
                        attempts += 1
                        time.sleep(0.5)
            except Exception:
                # "모두 접기" 버튼 찾기
                collapse_button = self.driver.find_element(By.XPATH, '//button[.//span[text()="모두 접기"]]')
                if collapse_button:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", collapse_button)
            finally:
                # 커리큘럼 로딩 대기
                wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "mantine-Accordion-item")]')))

                # 커리큘럼 정보 추출
                sections = self.driver.find_elements(By.XPATH, '//div[contains(@class, "mantine-Accordion-item")]')
                section_pattern = r"섹션 (\d+)\. (.+)"

                for section in sections:
                    section_title_element = section.find_element(By.XPATH,
                                                                 './/button[contains(@class, "mantine-Accordion-control")]/span/div/p')
                    section_title_element_text = section_title_element.text.strip()
                    match = re.search(section_pattern, section_title_element_text)

                    section_info = None

                    if match:
                        section_number = match.group(1)
                        section_title = match.group(2)
                        section_info = Section(section_number, section_title)

                    lessons = section.find_elements(By.XPATH, './/ul/li')

                    for number, lesson in enumerate(lessons):
                        lesson_title = ""
                        lesson_duration = "00:00:00"

                        try:
                            lesson_title_element = lesson.find_element(By.XPATH,
                                                                         './/div[contains(@class, "mantine-Group-root")]/a/p')
                            lesson_title = lesson_title_element.text.strip()
                            lesson_duration_element = lesson.find_element(By.XPATH,
                                                                            './/div[contains(@class, "mantine-Group-root")]/p')
                            lesson_duration = lesson_duration_element.text.strip()
                        except Exception as e:
                            # 강의 영상이 아닌 경우
                            attached_contents += 1
                            # print(f"Error in crawling {number + 1} lesson in section {section_number}: {e}")
                        finally:
                            lesson = Lesson(section_info, number + 1, lesson_title, lesson_duration)
                            self.lessons.append(lesson)
            end_time = datetime.datetime.now()
            print(f"영상이 아닌 자료 {attached_contents}개가 목차에서 제외되었습니다.")
            print(f"소요 시간: {end_time - start_time}")
            print(f"강의 목차 크롤링이 완료되었습니다!")
            print("======================================================")
            self.driver.quit()
            return self.lessons
        except Exception as e:
            print("강의 정보를 찾을 수 없습니다.")
            exit()

    def get_lessons(self) -> List[Lesson]:
        return self.lessons
