# Course Scheduler

__KO__ | [EN](README-en.md)

## Introduction

> **학습 도우미 with 인프런**  
> : 인프런 강의 목차 추출 / 목표 시간 기반 수강 범위 계산 / 출력 커스텀

## Key Features
- **인프런 전용** 강의 목차 추출
  - 커리큘럼 크롤링
  - 단원별 수업 영상 인덱싱
  - 단원, 수업 인덱스, 수업명, 수업 시간 포함
- 학습 계획
  - 목표 학습 시간 설정
  - 목표 시간 기준으로 강의 범위 분류
  - 학습 일마다 (강의 범위 인덱스 + 시작/마지막 수업명 + 학습 시간) 계산
  - 완강 예상 일수 계산
- 사용자 정의 형식 출력
  - 마크다운 형식 파일로 저장
  - 카운트, 인덱스, 수업명, 학습 시간 등 커스텀 기능

## Requirements

- Python 3.7+
- [requirements.txt](requirements.txt)


## How to Use

### 1. Installation

```bash
$ git clone https://github.com/dadahee/course-scheduler.git
$ cd course-scheduler
$ pip install -r requirements.txt
```

### 2. Configuration

출력 형식 수정: `config.json`

```json
{
    "include_course_name_header": true, // 강의 제목(h1) 포함 여부
    "average_minutes_per_count": 60, // 회차별 수강 시간
    "count_settings": {
        "include_count": true, // 수강 일정에 카운트 포함 여부
        "format": "[{count}일차]" // 카운트 문자열 형식
    },
    "range_settings": {
        "include_start_lesson_title": true, // 수강 일정 시작 범위 강의명 포함 여부
        "include_end_lesson_title": true, // 수강 일정에 마지막 강의명 포함 여부
        "lesson_index_format": "{section:0>2}.{number:0>2}", // 섹션 내 수업 인덱스들의 표현 형식 (section: 0부터, number: 1부터 시작)
        "section_index_format": "{section:0>2}.", // 섹션 인덱스 표현 형식
        "range_separator_format": "~" // [시작 범위] (중간에 들어갈 문자열 형식) [종료 범위]
    },
    "duration_settings": {
        "include_duration": true, // 수강 일정에 일자별 강의 합산 시간 표시 여부
        "format": "({hh:0>2}:{mm:0>2}:{ss:0>2})" // 수강 일정별 강의 시간 포함
    },
    "toc_output": "outputs/toc.md", // 추출한 강의 목차를 저장할 파일
    "schedule_output": "outputs/schedule.md" // 추출한 수강 일정을 저장할 파일
}
```

### 3. Execution

지원 명령어:

| Command    | Description                |
|------------|----------------------------|
| `auto`     | 강의 목차 추출 & 일자별 수강 범위 계산    |
| `toc`      | 강의 목차 추출                   |
| `schedule` | (강의 목차 파일 기반) 일자별 수강 범위 계산 |


#### auto

- = `toc` + `schedule`
- 입력한 강의 URL의 커리큘럼 정보를 크롤링 -> 강의 목차를 markdown 파일로 저장 -> 일자별 수강 범위 계산 -> 수강 일정을 markdown 파일로 저장

```bash
$ python main.py auto [-h] [-c CONFIG] [-o OUT] url
```

Positional arguments:
- `url`: 강의 URL
  - `https://www.inflearn.com/course/{value}` 형식만 가능

Optional arguments:
- `-h`, `--help`: 도움말
- `-c CONFIG`, `--config CONFIG`: 설정 파일 (default: `config.json`)
- `-o OUT`, `--out OUT`: 저장할 파일 (default: `outputs/schedule.md`)


#### toc

입력한 강의 URL의 커리큘럼 정보를 크롤링하고 markdown 파일로 저장

```bash
$ python main.py toc [-h] [-c CONFIG] [-o OUT] url
```
Positional arguments:
- `url`: 강의 URL
  - `https://www.inflearn.com/course/{value}` 형식만 가능

Optional arguments:
- `-h`, `--help`: 도움말
- `-c CONFIG`, `--config CONFIG`: 설정 파일 (default: `config.json`)
- `-o OUT`, `--out OUT`: 추출한 목차를 저장할 파일 (`outputs/toc.md`)


#### schedule

강의 목차 파일을 읽고 일자별 수강 범위를 계산하여 markdown 파일로 저장

```bash
$ python main.py schedule [-h] [-c CONFIG] [-o OUT] filename
```

Positional arguments:
- `filename`: 강의 목차 파일

Optional arguments:
- `-h`, `--help`: 도움말
- `-c CONFIG`, `--config CONFIG`: 설정 파일
- `-o OUT`, `--out OUT`: 저장할 파일 (default: `outputs/schedule.md`)

Additional information: 
- 강의 목차(default: `outputs/toc.md`) 형식 == `config.json` 형식인 모든 플랫폼 강의에 사용할 수 있습니다.
  ```markdown
  # [Course Title]
    
  ## [Section Index Format] [Section Title]
  - [Lesson Index Format] [Lesson Title] [Duration Format]
  - [Lesson Index Format] [Lesson Title] [Duration Format]
  - [Lesson Index Format] [Lesson Title] [Duration Format]
  ... (생략)
  ```

---

## Example

### Use Case (1)

강의: [김영한의 실전 자바 - 고급 1편, 멀티스레드와 동시성](https://www.inflearn.com/course/%EA%B9%80%EC%98%81%ED%95%9C%EC%9D%98-%EC%8B%A4%EC%A0%84-%EC%9E%90%EB%B0%94-%EA%B3%A0%EA%B8%89-1)

- `config.json`
    ```json
    {
        "include_course_name_header": true,
        "average_minutes_per_count": 60,
        "count_settings": {
            "include_count": true,
            "format": "[{count}일차]"
        },
        "range_settings": {
            "include_start_lesson_title": true,
            "include_end_lesson_title": true,
            "lesson_index_format": "{section:0>2}.{number:0>2}",
            "section_index_format": "{section:0>2}.",
            "range_separator_format": "~"
        },
        "duration_settings": {
            "include_duration": true,
            "format": "({hh:0>2}:{mm:0>2}:{ss:0>2})"
        },
        "toc_output": "outputs/toc.md",
        "schedule_output": "outputs/schedule.md"
    }
    ```
- 실행 명령어
    ```bash
    $ python main.py auto [강의 URL (생략)]
    ```
- 실행 결과
  - `outputs/toc.md`
    ```markdown
    # 김영한의 실전 자바 - 고급 1편, 멀티스레드와 동시성
  
    ## 00. 강의 소개와 자료
    - 00.01 강의 소개 (00:02:28)  
  
    ## 01. 프로세스와 스레드 소개
    - 01.01 멀티태스킹과 멀티프로세싱 (00:12:15)  
    - 01.02 프로세스와 스레드 (00:10:24)  
    - 01.03 스레드와 스케줄링 (00:08:55)  
    - 01.04 컨텍스트 스위칭 (00:21:37)  
    ... (생략)
    ```
  - `outputs/schedule.md`
    ```markdown
    # 김영한의 실전 자바 - 고급 1편, 멀티스레드와 동시성
    
    - [1일차] 00.01 강의 소개 ~ 02.01 프로젝트 환경 구성 (00:58:44)  
    - [2일차] 02.02 스레드 시작1 ~ 02.08 Runnable을 만드는 다양한 방법 (00:57:39)  
    - [3일차] 02.09 문제와 풀이 ~ 03.03 스레드의 생명 주기 - 코드 (00:52:39)
    ... (생략)
    ```


### Use Case (2)

강의: [토비의 스프링 6 - 이해와 원리](https://www.inflearn.com/course/%ED%86%A0%EB%B9%84%EC%9D%98-%EC%8A%A4%ED%94%84%EB%A7%816-%EC%9D%B4%ED%95%B4%EC%99%80-%EC%9B%90%EB%A6%AC)

- `config.json`
    ```json
    {
        "include_course_name_header": false,
        "average_minutes_per_count": 180,
        "count_settings": {
            "include_count": true,
            "format": "{count}주차 |"
        },
        "range_settings": {
            "include_start_lesson_title": false,
            "include_end_lesson_title": true,
            "lesson_index_format": "{section:0>2}단원 {number:0>2}강",
            "section_index_format": "{section:0>2}단원.",
            "range_separator_format": "->"
        },
        "duration_settings": {
            "include_duration": true,
            "format": "({hh:0>2}시간 {mm:0>2}분 {ss:0>2}초)"
        },
        "toc_output": "outputs/toc.md",
        "schedule_output": "outputs/schedule.md"
    }
    ```
- 실행 명령어
    ```bash
    $ python main.py auto [강의 URL (생략)]
    ```
- 실행 결과
  - `outputs/toc.md`
      ```markdown
      ## 00단원. 강의 소개
      - 00단원 01강 강의 소개 (00시간 02분 52초)  
      - 00단원 02강 강사 소개 (00시간 00분 53초)  
      - 00단원 03강 학습 방법 (00시간 02분 53초)  
    
      ## 01단원. 스프링 개발 시작하기
      - 01단원 01강 개발환경 준비 (00시간 18분 40초)  
      - 01단원 02강 HelloSpring 프로젝트 생성 (00시간 14분 38초)  
      - 01단원 03강 PaymentService 요구사항 (00시간 07분 04초)  
      - 01단원 04강 PaymentService 개발 (1) (00시간 11분 03초)  
      - 01단원 05강 PaymentService 개발 (2) (00시간 17분 38초)  
      - 01단원 06강 PaymentService 개발 (3) (00시간 20분 07초)  
      ... (생략)
      ```
  - `outputs/schedule.md` 
    ```markdown
    - 1주차 | 00단원 01강 -> 02단원 07강 오브젝트 팩토리 (02시간 52분 58초)  
    - 2주차 | 02단원 08강 -> 03단원 06강 테스트와 DI (2) (02시간 56분 49초)  
    - 3주차 | 03단원 07강 -> 04단원 11강 스프링이 제공하는 템플릿 (02시간 44분 03초)  
    - 4주차 | 05단원 01강 -> 06단원 06강 JDBC 데이터 액세스 기술 (02시간 44분 55초)  
    - 5주차 | 06단원 07강 -> 07단원 01강 스프링을 어떻게 공부할 것인가? (01시간 08분 33초)
    ```


### Use Case (3)

강의: [토비의 스프링 6 - 이해와 원리](https://www.inflearn.com/course/%ED%86%A0%EB%B9%84%EC%9D%98-%EC%8A%A4%ED%94%84%EB%A7%816-%EC%9D%B4%ED%95%B4%EC%99%80-%EC%9B%90%EB%A6%AC)

- `config.json`
    ```json
    {
        "include_course_name_header": false,
        "average_minutes_per_count": 180,
        "count_settings": {
            "include_count": false,
            "format": "{count}주차 |"
        },
        "range_settings": {
            "include_start_lesson_title": false,
            "include_end_lesson_title": false,
            "lesson_index_format": "{section:0>2}단원 {number:0>2}강",
            "section_index_format": "{section:0>2}단원.",
            "range_separator_format": "->"
        },
        "duration_settings": {
            "include_duration": false,
            "format": "({hh:0>2}시간 {mm:0>2}분 {ss:0>2}초)"
        },
        "toc_output": "outputs/toc.md",
        "schedule_output": "outputs/schedule.md"
    }
    ```
- `outputs/toc.md`: Use case (2) 산출물과 동일 
- 실행 명령어
    ```bash
    $ python main.py schedule outputs/toc.md
    ```
- 실행 결과
  - `outputs/schedule.md` 
    ```markdown
    - 00단원 01강 -> 02단원 07강  
    - 02단원 08강 -> 03단원 06강  
    - 03단원 07강 -> 04단원 11강  
    - 05단원 01강 -> 06단원 06강  
    - 06단원 07강 -> 07단원 01강  
    ```

---

## Contribution

If you'd like to contribute to this project, please fork the repository and make your changes. Pull requests are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

