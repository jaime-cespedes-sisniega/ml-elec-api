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


request_examples = {
    "example": {
        "summary": "Example",
        "value": {
            "day": 7,
            "period": 0.978723,
            "nswprice": 0.066651,
            "nswdemand": 0.329366,
            "vicprice": 0.00463,
            "vicdemand": 0.345417,
            "transfer": 0.206579
        }
    }
}


class Response(BaseModel):
    """Response class

    Ensures that the return has
    the defined format.
    """

    timestamp: str
    class_pred: str


response_examples = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "example": {
                        "summary": "Example",
                        "value": {"timestamp": "2021-11-30T08:01:32.415845",
                                  "class_pred": "UP"}
                    },
                }
            }
        }
    },
}
