COURSE = """목차"""

MINUTES_PER_DAY = 80
SCHEDULE_FORMAT = "섹션 {}-{} ({})"

TIME_PER_DAY = str(MINUTES_PER_DAY) + ":00"

schedules = []


def add_schedule(start_range, end_range, sum_time):
    schedules.append(SCHEDULE_FORMAT.format(start_range, end_range, sum_time))


def add_time(base_time, additional_time):
    base_minutes, base_seconds = map(int, base_time.split(':'))
    additional_minutes, additional_seconds = map(int, additional_time.split(':'))
    total_minutes = base_minutes + additional_minutes
    total_seconds = base_seconds + additional_seconds
    if total_seconds >= 60:
        total_minutes += total_seconds // 60
        total_seconds = total_seconds % 60
    formatted_time = f"{total_minutes:02d}:{total_seconds:02d}"
    return formatted_time


def is_same_or_longer_than(time1, time2):
    minutes1, seconds1 = map(int, time1.split(':'))
    minutes2, seconds2 = map(int, time2.split(':'))

    if minutes1 < minutes2 or (minutes1 == minutes2 and seconds1 < seconds2):
        return False
    elif minutes1 > minutes2 or (minutes1 == minutes2 and seconds1 > seconds2):
        return True
    else:
        return True


def get_diff_seconds(base, time):
    base_minutes, base_seconds = map(int, base.split(':'))
    minutes, seconds = map(int, time.split(':'))

    total_base_seconds = base_minutes * 60 + base_seconds
    total_seconds = minutes * 60 + seconds
    return total_seconds - total_base_seconds


categories_meta = COURSE.split("\n")

categories = list(filter(lambda x: not (len(x) <= 1 or "강 ∙ " in x or "미리보기" == x), categories_meta))

idx = 0
sub_sec = 0
sec = 0
toc = []

while idx < len(categories):
    if categories[idx].startswith("섹션"):
        sec += 1
        idx += 1
        sub_sec = 0
    elif ":" in categories[idx] and len(categories[idx]) == 5:
        toc[-1] = (toc[-1][0], categories[idx])
        idx += 1
    else:
        sub_sec += 1
        toc.append(("{:02d}.{:02d} {}".format(sec, sub_sec, categories[idx]), None))
        idx += 1

days = 1

next_idx = 0
start_range = ""
end_range = ""
schedules = []

today_time = "00:00"
total_time = "00:00"
calculated_time = "00:00"

while next_idx < len(toc) - 1:

    next_time = add_time(today_time, toc[next_idx][1])

    today_seconds = abs(get_diff_seconds(TIME_PER_DAY, today_time))
    next_seconds = abs(get_diff_seconds(TIME_PER_DAY, next_time))

    if not start_range:
        start_range = toc[next_idx][0].split(" ")[0]

    if today_seconds < next_seconds:
        end_range = toc[next_idx - 1][0].split(" ")[0]
        add_schedule(start_range, end_range, today_time)
        calculated_time = add_time(calculated_time, today_time)
        days += 1
        today_time = "00:00"
        end_range = ""
        start_range = ""
    else:
        today_time = next_time
        next_idx += 1

if not (is_same_or_longer_than(total_time, calculated_time)):
    end_range = toc[-1][0].split(" ")[0]
    rest_time = add_time(today_time, toc[-1][1])
    add_schedule(start_range, end_range, rest_time)

print("\n".join(schedules))

for (sc_title, sc_time) in toc:
    total_time = add_time(sc_time, total_time)

t_meta = total_time.split(":")
total_time = "{:02d}:{:02d}:{:02d}".format(int(t_meta[0]) // 60, int(t_meta[0]) % 60, int(t_meta[1]))
print("총 {}".format(total_time, total_time))
