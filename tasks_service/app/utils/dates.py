from datetime import datetime


def get_last_quarter() -> tuple[int, int]:
    """
    Возвращает номер последнего квартала и год на основе текущей даты.
    Если текущий квартал только начался, берём предыдущий.
    """
    now = datetime.now()
    year = now.year
    month = now.month
    if month in [1, 2, 3]:
        quarter = 4
        year -= 1
    elif month in [4, 5, 6]:
        quarter = 1
    elif month in [7, 8, 9]:
        quarter = 2
    else:  # [10, 11, 12]
        quarter = 3
    return quarter, year


def get_quarter_dates(quarter: int, year: int) -> tuple[datetime, datetime]:
    """
    Возвращает даты начала и конца квартала.
    """
    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Invalid quarter")
    start_month = {1: 1, 2: 4, 3: 7, 4: 10}
    end_month = {1: 4, 2: 7, 3: 10, 4: 1}
    start_date = datetime(year, start_month[quarter], 1)
    end_year = year + 1 if quarter == 4 else year
    end_date = datetime(end_year, end_month[quarter], 1)
    return start_date, end_date
