from pydantic import BaseModel, ConfigDict


class BaseTeacher(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    subject: str
