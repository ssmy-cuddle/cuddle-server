from fastapi import HTTPException, status
from enum import Enum

class ErrorCode(Enum):
    ALREADY_EXISTS = (
        status.HTTP_409_CONFLICT,
        "ALREADY_EXISTS",
        "존재하는 계정입니다.",
    )
    INVALID_LENGTH = (
        status.HTTP_400_BAD_REQUEST,
        "INVALID_LENGTH",
        "ID의 길이가 50자를 초과했습니다.",
    )
    USER_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "USER_NOT_FOUND",
        "User not found.",
    )

    def __new__(cls, status_code: int, error_code: str, msg: str):
        obj = object.__new__(cls)
        obj.status_code = status_code
        obj.error_code = error_code
        obj.msg = msg

        return obj

def raise_error(error_code: ErrorCode):
    """
    * method:   raise_error
    * purpose:  에러코드 재사용
    """
    
    raise HTTPException(
        status_code=error_code.status_code,
        detail={
            "code": error_code.error_code,
            "message": error_code.msg
        }
    )