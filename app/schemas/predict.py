from typing import List

from pydantic import BaseModel


class DataInput(BaseModel):
    """Data input class

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


class MultipleDataInputs(BaseModel):
    """Multiple data input class"""

    inputs: List[DataInput]

    class Config:
        """Multiple data input class config"""

        schema_extra = {
            'example': {
                'inputs': [
                    {
                        "day": 7,
                        "period": 0.978723,
                        "nswprice": 0.066651,
                        "nswdemand": 0.329366,
                        "vicprice": 0.00463,
                        "vicdemand": 0.345417,
                        "transfer": 0.206579
                    }
                ]
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response class

    Ensures that the response has
    the defined format.
    """

    timestamp: str
    predictions: List[str]

    class Config:
        """Prediction response class config"""

        schema_extra = {
            'example': {
                "timestamp": "2021-11-30T08:01:32.415845",
                "predictions": ["UP"]
            }
        }
