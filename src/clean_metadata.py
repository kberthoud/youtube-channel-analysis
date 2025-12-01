import re
from datetime import datetime

def parse_iso8601_duration(duration_str:str) -> int:
  '''The metadata column for duration is in the format "PTxxHxxMxxS" with each letter corresponding to
  hours minutes or seconds. Note: all or none of those letters may be present in each row. 
  Output is total duration in seconds.'''
  
  hours = minutes = seconds = 0

  match_hours = re.search(r'(\d+)H',duration_str)
  match_minutes = re.search(r'(\d+)M',duration_str)
  match_seconds = re.search(r'(\d+)S',duration_str)

  if match_hours:
    hours = int(match_hours.group(1))
  if match_minutes:
    minutes = int(match_minutes.group(1))
  if match_seconds:
    seconds = int(match_seconds.group(1))

  total_seconds = hours*60*60 + minutes*60 + seconds

  return total_seconds
  
def parse_pubish_date(value):
  '''Converts the youtube date format into a python date string format.
  Youtube format is like: YYYY-MM-DD hh:mm:ssZ.
  Should also account for blank values if publish date is missing.'''
  
  if not value:
    return None
  
  try:
    return datetime.strptime(value,"%Y-%m-%dT%H:%M:%SZ")
  except Exception:
    return None

def parse_int(value):
    """
    Convert integer stored as strings to Python int.
    Returns None on blank or invalid.
    """
    if value is None or value == "":
        return None

    try:
        return int(value)
    except ValueError:
        return None
