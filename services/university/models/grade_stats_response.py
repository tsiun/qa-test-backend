from pydantic import ConfigDict, BaseModel, Field

from services.university.models.base_grade import MAX_GRADE, MIN_GRADE


class GradeStatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int = Field(ge=MIN_GRADE)
    min: int | None = Field(default=None, ge=MIN_GRADE, le=MAX_GRADE)
    max: int | None = Field(default=None, ge=MIN_GRADE, le=MAX_GRADE)
    avg: float | None = Field(default=None, ge=MIN_GRADE, le=MAX_GRADE)
