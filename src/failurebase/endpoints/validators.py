"""Common validators module."""

import json
from typing import Annotated
from fastapi import HTTPException, Query


class RequestValidationError(HTTPException):
    """Validation error of query params."""

    def __init__(self, loc, msg, typ):
        super().__init__(422, [{'loc': loc, 'msg': msg, 'type': typ}])


def validate_test_marks(
    test_marks: Annotated[
        str | None, Query(title='Test marks', description='Test mark list in JSON format, e.g.: ["CRT", "CIT"]')
    ] = None
) -> list[str] | None:
    """Validates if received query parameter has expected JSON format."""

    if test_marks is not None:

        try:
            data = json.loads(test_marks)
        except json.decoder.JSONDecodeError:
            raise_error = True
        else:
            raise_error = not isinstance(data, list) or not all(isinstance(item, str) for item in data)

        if raise_error:
            raise RequestValidationError(
                ('path', 'test_marks'),
                'string does not match format: ["<tag>","<tag>",...]',
                "value_error.test_marks.format"
            )

        return data
