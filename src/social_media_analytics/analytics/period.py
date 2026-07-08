from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_previous_months(target_date):
    current = target_date.replace(day=1)

    previous = current - relativedelta(months=1)
    before_previous = current - relativedelta(months=2)

    return previous, before_previous
