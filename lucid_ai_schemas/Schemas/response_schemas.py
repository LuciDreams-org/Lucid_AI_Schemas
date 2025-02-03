from typing import List

from pydantic import BaseModel


class Plot(BaseModel):
    name: str
    type: str
    time_period: str
    formulas: List[int]


class PlotCollectionResponse(BaseModel):
    plots: List[Plot]
