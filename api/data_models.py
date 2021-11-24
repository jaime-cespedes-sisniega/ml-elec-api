from pydantic import BaseModel


class Request(BaseModel):
    """Request class

    Ensures that every feature has
    the correct data type.
    """

    day: int
    period: float
    nswprice: float
    nswdemand: float
    vicprice: float
    vicdemand: float
    transfer: float


class Response(BaseModel):
    """Response class

    Ensures that the return has
    the defined format.
    """

    timestamp: str
    class_pred: str
