from datetime import datetime

from main import main

if __name__ == '__main__':

    start_time = datetime.now()
    main()
    end_time = datetime.now()

    count = 0
    results = []

    while count < 5:
        count += 1
        start_time = datetime.now()
        main()
        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        results.append(total_seconds)

    average_seconds = sum(results) / count
    print("============ 명령어 테스트 완료 ============")
    for i in range(len(results)):
        print(f"[{i + 1}차] 명령어 소요 시간: {results[i]}초")
    print(f"5회 평균 소요 시간: {average_seconds}초")
