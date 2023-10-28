import pydantic
import typing


class CreateAd(pydantic.BaseModel):
    header: str
    description: str
    owner: str

    @pydantic.validator('header')
    def character_count(cls, value):
        if len(value) > 50:
            raise ValueError('headline is too long')
        return value


class UpdateAd(pydantic.BaseModel):
    header: typing.Optional[str]
    description: typing.Optional[str]
    creation_date: typing.Optional[str]
    owner: typing.Optional[str]

    @pydantic.validator('header')
    def character_count(cls, value):
        if len(value) > 50:
            raise ValueError('headline is too long')
        return value
