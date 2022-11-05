from datetime import datetime, timezone, timedelta
from typing import Literal


def get_date(day: str, timezone_: timezone) -> tuple[datetime, datetime]:
    now_date = datetime.now(tz=timezone_)
    if day == "어제":
        return now_date, now_date - timedelta(days=1)
    elif day == "오늘":
        return now_date, now_date
    elif day == "내일":
        return now_date, now_date + timedelta(days=1)
    elif day == "모레":
        return now_date, now_date + timedelta(days=2)
    else:
        try:
            return now_date, datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            raise ValueError("잘못된 날짜 형식입니다.")


def get_meal_code(meal_name: str) -> Literal["1", "2", "3"]:
    if meal_name in ["아침", "조식"]:
        return "1"
    elif meal_name in ["점심", "중식"]:
        return "2"
    elif meal_name in ["저녁", "석식"]:
        return "3"
    else:
        raise ValueError("잘못된 식사 이름입니다.")


def get_school_year_date(school_year: str, timezone_: timezone) -> tuple[datetime, datetime, datetime]:
    now_date = datetime.now(tz=timezone_)

    if school_year == "작년":
        from_date = now_date.replace(year=now_date.year - 1, month=3)
        to_date = now_date.replace(year=now_date.year, month=3)
    elif school_year == '올해':
        from_date = now_date.replace(year=now_date.year, month=3)
        to_date = now_date.replace(year=now_date.year + 1, month=3)
    elif school_year == '내년':
        from_date = now_date.replace(year=now_date.year + 1, month=3)
        to_date = now_date.replace(year=now_date.year + 2, month=3)
    else:
        try:
            date = datetime.strptime(school_year, "%Y")
        except ValueError:
            raise ValueError("잘못된 연도 형식입니다.")
        
        from_date = date.replace(month=3)
        to_date = date.replace(year=date.year + 1, month=3)
    return now_date, from_date, to_date
