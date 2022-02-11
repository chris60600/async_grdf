import datetime

GRDF_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Convert GRDF datetime string to datetime
def date_from_grdf(date_grdf) -> datetime:

    if date_grdf == None: return None
    else:
        _date_s = date_grdf[0:19].replace('T',' ')
        return datetime.datetime.strptime(_date_s,GRDF_DATETIME_FORMAT)
