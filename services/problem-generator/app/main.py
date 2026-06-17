from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.generators import (
    UnsupportedSubjectError,
    generate_problem,
    supported_subjects,
)

Tier = Literal["easy", "medium", "hard", "exam"]

app = FastAPI(
    title="Learning Platform Problem Generator",
    version="0.1.0",
)


class GenerateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    subject: str = Field(min_length=1)
    tier: Tier


class GenerateResponse(BaseModel):
    subject: str
    tier: Tier
    problem: str
    solution: str


class HealthResponse(BaseModel):
    status: str
    supported_subjects: list[str]


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", supported_subjects=supported_subjects())


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        generated = generate_problem(request.subject, request.tier)
    except UnsupportedSubjectError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "message": str(exc),
                "supported_subjects": supported_subjects(),
            },
        ) from exc

    return GenerateResponse(
        subject=generated.subject,
        tier=generated.tier,
        problem=generated.problem,
        solution=generated.solution,
    )
