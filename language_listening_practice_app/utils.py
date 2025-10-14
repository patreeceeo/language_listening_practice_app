from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def loose_str_compare(a: str, b: str) -> bool:
    """Compare two strings loosely, ignoring case and whitespace and punctuation."""
    return ''.join(e for e in a if e.isalnum()).lower() == ''.join(e for e in b if e.isalnum()).lower()

# Take the same kwargs as datetime.timedelta
def relative_datetime(**kwargs: int) -> datetime:
    """Get a datetime relative to now."""
    return datetime.now(ZoneInfo("UTC")) + timedelta(**kwargs)
