from datetime import datetime, timedelta
import pytz
from surrealdb import Surreal


def convert_et_to_utc(et_time_str):
    # define the month mapping dictionary
    month_map = {
        "Jan.": "January",
        "Feb.": "February",
        "March": "March",
        "April": "April",
        "May": "May",
        "June": "June",
        "July": "July",
        "Aug.": "August",
        "Sept.": "September",
        "Oct.": "October",
        "Nov.": "November",
        "Dec.": "December",
    }

    # get current date and time in ET
    et_tz = pytz.timezone("US/Eastern")
    now = datetime.now(et_tz)

    # handle "Today" and "Yesterday"
    if et_time_str.startswith("Today"):
        time_str = et_time_str.replace("Today ", "")
        et_time = now.replace(
            hour=int(time_str[:2]),
            minute=int(time_str[3:5]),
            second=int(time_str[6:8]),
            microsecond=0,
        )
    elif et_time_str.startswith("Yesterday"):
        time_str = et_time_str.replace("Yesterday ", "")
        et_time = (now - timedelta(days=1)).replace(
            hour=int(time_str[:2]),
            minute=int(time_str[3:5]),
            second=int(time_str[6:8]),
            microsecond=0,
        )
    else:
        # replace abbreviated month names with full names
        for short, full in month_map.items():
            if short in et_time_str:
                et_time_str = et_time_str.replace(short, full)
                break
        # parse the date string
        et_time = datetime.strptime(et_time_str, "%B %d, %Y %H:%M:%S")
        et_time = et_tz.localize(et_time)

    # convert the ET time to UTC
    utc_time = et_time.astimezone(pytz.utc)

    # return the UTC time as an ISO 8601 formatted string
    return utc_time.isoformat()


async def relate(db: Surreal, id_1: str, id_2: str, table: str):
    """Runs ``RELATE id_1->table->id_2`` for you. You're welcome."""

    return await db.query(f"RELATE {id_1}->{table}->{id_2}")
