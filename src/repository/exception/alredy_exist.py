import re

from sqlalchemy.exc import IntegrityError


def check_already_exists(error: IntegrityError) -> bool:
    pattern = re.compile(
        r"KEY \(.*\)=[^\(]*(\(.*\))[^\)]*already exists", re.IGNORECASE
    )
    return bool(pattern.search(str(error.orig)))


class AlredyExistError(Exception):
    pass
