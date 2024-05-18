from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from pydantic.generics import GenericModel

M = TypeVar("M", bound=BaseModel)


class Paging(BaseModel):
    limit: int
    skip: int
    total: int


class DataWithPagination(GenericModel, Generic[M]):
    data: List[M]
    paging: Paging


class ResponseModelSingleItem(GenericModel, Generic[M]):
    data: M
    status_code: Optional[int] = 200


class ResponseModelListItem(GenericModel, Generic[M]):
    data: List[M]
    message: Optional[str]
    status_code: Optional[int] = 200


class ResponseModelListItemWithPagination(GenericModel, Generic[M]):
    data: DataWithPagination
    message: Optional[str]
    status_code: Optional[int] = 200


class ValidatorErrorResponse(BaseModel):
    message: str


class BadRequestResponseModel(BaseModel):
    status_code: int = 400
    message: str = "Bad Request"


class NotFoundResponseModel(BadRequestResponseModel):
    status_code: int = 404
    message: str = "Not found !"
