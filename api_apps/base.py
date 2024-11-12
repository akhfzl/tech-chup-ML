from pydantic import BaseModel

class PredictionRequest(BaseModel):
    arrival_time: str
    start_time: str
    queue_length: int