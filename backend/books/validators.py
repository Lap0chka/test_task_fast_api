import logging
from datetime import datetime
from typing import Union, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_empty_values(value: Union[str, List]) -> Union[str, List]:
    """
    Validate and clean empty string or list values.

    Args:
        value (Union[str, List]): The value to check.

    Returns:
        Union[str, List]: The cleaned value.

    Raises:
        ValueError: If the value is empty or unsupported type.
    """
    if isinstance(value, list):
        if not value:
            logger.error("List is empty.")
            raise ValueError("List must not be empty")
        logger.info("List value validated successfully.")
        return value

    if isinstance(value, str):
        v = value.strip()
        if not v:
            logger.error("String is empty after stripping.")
            raise ValueError("String must not be empty")
        logger.info("String value validated successfully.")
        return v




def clean_date(value: Union[str, int, None]) -> int:
    """
    Validate and clean a published year value.
    """
    current_year = datetime.now().year
    min_year = 1800

    if value is None:
        logger.error("Published year is None.")
        raise ValueError(f"published_year must be between {min_year} and {current_year}")

    try:
        year = int(value)
    except (TypeError, ValueError):
        logger.error("Published year is not a valid integer.")
        raise ValueError("published_year must be an integer")

    if not (min_year <= year <= current_year):
        logger.error(f"Published year {year} is out of range.")
        raise ValueError(f"published_year must be between {min_year} and {current_year}")

    return year