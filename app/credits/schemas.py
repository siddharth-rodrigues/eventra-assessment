from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreditBalanceResponse(BaseModel):
    credits: int
    plan_type: str
    last_reset_at: datetime

    model_config = ConfigDict(from_attributes=True)
