from pydantic import BaseModel, field_validator

from libs.config import statistic_valid_keys


class StatisticReqDTO(BaseModel):
    key: str
    value: str

    @field_validator('key')
    @classmethod
    def validate_cursor(cls, value):
        if value not in statistic_valid_keys:
            raise ValueError('key is not valid')
        return value

    @field_validator('key', 'value')
    @classmethod
    def check_not_empty(cls, value):
        if not value:
            raise ValueError('`key` and `value` cannot be empty')
        return value


class StatisticResDTO:
    key: str
    value: str

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
