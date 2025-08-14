from fastapi import HTTPException


class AuthorNotExistException(HTTPException):
    """Custom exception for when wrong authors name."""

    def __init__(self) -> None:
        """Initialize the wrong authors name with status 404."""
        super().__init__(
            status_code=404,
            detail='Author with this names can not be found',
        )



class BookNotFoundByIdException(HTTPException):
    """Course cannot be found by id."""

    def __init__(self) -> None:
        """Initialize the CourseNotFoundByIdException with status 404."""
        super().__init__(
            status_code=404,
            detail='Active course cannot be not found.',
        )

class ForgottenParametersException(HTTPException):
    """Custom exception for when a forgotten parameter is missing."""

    def __init__(self) -> None:
        """Initialize the ForgottenParametersException with status 422."""
        super().__init__(
            status_code=422,
            detail='Not all parameters was filled',
        )
