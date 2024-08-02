# Course Scheduler

[KO](README.md) | __EN__  

## Introduction

A Python program that
- Extracts course outlines from [Inflearn](https://www.inflearn.com/)
- Organizes and formats study schedules with customizable outputs

## Key Features

- Extracts the course outline from a given Inflearn course URL (currently supports only Inflearn)
- Calculates the total number of days needed to complete the course
- Divides the course lessons into study segments based on the specified learning time
- Outputs the study schedule in a custom Markdown format

## Requirements

- Python 3.7+
- [requirements.txt](requirements.txt)

## How to Use

### 1. Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/dadahee/course-scheduler.git
cd course-scheduler
pip install -r requirements.txt
```

### 2. Configuration

Edit the `config.json` file to set your desired output format:

```json
{
    "include_course_name_header": true, // include a course name in the header (h1) if true
    "average_minutes_per_count": 60, // the total time of the lessons in each schedule
    "count_settings": {
        "include_count": true, // specify a counter in each schedule if true
        "format": "[{count}일차]" // count string format
    },
    "range_settings": {
        "include_start_lesson_title": true, // specify the first lesson title in each schedule if true
        "include_end_lesson_title": true, // specify the last lesson title in each schedule if true
        "lesson_index_format": "{section:0>2}.{number:0>2}", // lesson index format (with section starting from 0, lesson number starting from 1)
        "section_index_format": "{section:0>2}.", // section index format
        "range_separator_format": "~" // [first lesson] [** separator text here **] [last lesson]
    },
    "duration_settings": {
        "include_duration": true, // specify the total time of lessons in each schedule if true
        "duration_format": "({hh:0>2}:{mm:0>2}:{ss:0>2})" // duration formats
    },
    "toc_output": "outputs/toc.md", // file path for the course TOC
    "schedule_output": "outputs/schedule.md" // file path for the course schedules
}
```

### 3. Execution

Runnable Commands:

| Command    | Description                                               |
|------------|-----------------------------------------------------------|
| `auto`     | Extracts course outline and organizes course lessons      |
| `toc`      | Extracts course outline                                   |
| `schedule` | Organizes course lessons based on the course outline file |

#### auto

Combines `toc` and `schedule` commands:

```bash
python main.py auto [-h] [-c CONFIG] [-o OUT] url
```

Positional arguments:
- `url`: Course URL 

Optional arguments:
- `-h`, `--help`
- `-c CONFIG`, `--config CONFIG`: Config file path (default: `config.json`)
- `-o OUT`, `--out OUT`: File path for the output (default: `outputs/schedule.md`)

#### toc

Crawls the curriculum information from the provided course URL, formats it, and saves it as a Markdown file:

```bash
python main.py toc [-h] [-c CONFIG] [-o OUT] url
```

Positional arguments:
- `url`: Course URL

Optional arguments:
- `-h`, `--help`
- `-c CONFIG`, `--config CONFIG`: Config file path (default: `config.json`)
- `-o OUT`, `--out OUT`: File path for the output (default: `outputs/toc.md`)

#### schedule

Reads the specified course outline file, divides course lessons into study segments based on the specified learning time, and writes to a markdown file:

```bash
python main.py schedule [-h] [-c CONFIG] [-o OUT] filename
```

Positional arguments:
- `filename`: File path of the course outline

Optional arguments:
- `-h`, `--help`
- `-c CONFIG`, `--config CONFIG`: Config file path
- `-o OUT`, `--out OUT`: File path for the output (default: `outputs/schedule.md`)

Additional information: 
- available for **any** platform courses
- if the course TOC (default: `outputs/toc.md`) follows the format specified in `config.json`
- for example:
  ```markdown
  # [Course Title]
    
  ## [Section Index Format] [Section Title]
  - [Lesson Index Format] [Lesson Title] [Duration Format]
  - [Lesson Index Format] [Lesson Title] [Duration Format]
  - [Lesson Index Format] [Lesson Title] [Duration Format]
  ... (omitted)
  ```

---

## Example

### Use Case (1)

Lecture: [김영한의 실전 자바 - 고급 1편, 멀티스레드와 동시성](https://www.inflearn.com/course/%EA%B9%80%EC%98%81%ED%95%9C%EC%9D%98-%EC%8B%A4%EC%A0%84-%EC%9E%90%EB%B0%94-%EA%B3%A0%EA%B8%89-1)

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
- Executed command
    ```bash
    $ python main.py auto [강의 URL (생략)]
    ```
- Output
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
    ... (omitted)
    ```
  - `outputs/schedule.md`
    ```markdown
    # 김영한의 실전 자바 - 고급 1편, 멀티스레드와 동시성
    
    - [1일차] 00.01 강의 소개 ~ 02.01 프로젝트 환경 구성 (00:58:44)  
    - [2일차] 02.02 스레드 시작1 ~ 02.08 Runnable을 만드는 다양한 방법 (00:57:39)  
    - [3일차] 02.09 문제와 풀이 ~ 03.03 스레드의 생명 주기 - 코드 (00:52:39)
    ... (omitted)
    ```


### Use Case (2)

Lecture: [토비의 스프링 6 - 이해와 원리](https://www.inflearn.com/course/%ED%86%A0%EB%B9%84%EC%9D%98-%EC%8A%A4%ED%94%84%EB%A7%816-%EC%9D%B4%ED%95%B4%EC%99%80-%EC%9B%90%EB%A6%AC)

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
- Executed command
    ```bash
    $ python main.py auto [강의 URL (생략)]
    ```
- Output
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
      ... (omitted)
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

Lecture: [토비의 스프링 6 - 이해와 원리](https://www.inflearn.com/course/%ED%86%A0%EB%B9%84%EC%9D%98-%EC%8A%A4%ED%94%84%EB%A7%816-%EC%9D%B4%ED%95%B4%EC%99%80-%EC%9B%90%EB%A6%AC)

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
- `outputs/toc.md`: same with use case (2) output  
- Executed command
    ```bash
    $ python main.py schedule outputs/toc.md
    ```
- Output
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
