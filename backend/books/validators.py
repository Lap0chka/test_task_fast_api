from datetime import datetime


def clean_empty_values(value):
    if isinstance(value, list) and not value:
        raise ValueError("non-empty string")
    if isinstance(value, list) and value:
        return value
    v = value.strip()
    if not v:
        raise ValueError("non-empty string")
    return v


def clean_date(value):
    current_year = datetime.now().year
    if value is None:
        raise ValueError(f"published_year must be between 1800 and {current_year}")
    if value < 1800 or value > current_year:
        raise ValueError(f"published_year must be between 1800 and {current_year}")
    return value
