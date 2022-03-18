import datetime


def create_datetime_link_and_expiration(delay):
    values = datetime.datetime.utcnow()

    year = values.year

    if values.month < 10:
        month = "0" + str(values.month)
    else:
        month = str(values.month)

    if values.day < 10:
        day = "0" + str(values.day)
    else:
        day = str(values.day)

    if values.hour < 10:
        hour = "0" + str(values.hour)
    else:
        hour = str(values.hour)

    if values.minute < 10:
        minute = "0" + str(values.minute)
    else:
        minute = str(values.minute)

    if values.second < 10:
        second = "0" + str(values.second)
    else:
        second = str(values.second)

    datetime_link = ":%s-%s-%s-%s-%s-%s-UTC" % (year, month, day, hour, minute, second)

    values = values + datetime.timedelta(minutes=delay)
    datetime_expiration = list(str(values))
    datetime_expiration[10] = "T"
    datetime_expiration = datetime_expiration[0:19]
    datetime_expiration = "".join(datetime_expiration)
    datetime_expiration += "+00:00"

    return datetime_link, datetime_expiration
