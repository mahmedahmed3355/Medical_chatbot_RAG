from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ExperimentMetrics(BaseModel):
    """Validated retrieval metrics produced by an experiment."""

    hit_rate_at_k: float = Field(
        ge=0.0,
        le=1.0,
    )
    recall_at_k: float = Field(
        ge=0.0,
        le=1.0,
    )
    mrr: float = Field(
        ge=0.0,
        le=1.0,
    )


class ExperimentMetadata(BaseModel):
    """Metadata required to identify and reproduce an experiment."""

    experiment_id: str = Field(
        min_length=1,
    )
    benchmark_name: str = Field(
        min_length=1,
    )
    benchmark_version: str = Field(
        min_length=1,
    )
    created_at: datetime
    configuration: dict[str, Any] = Field(
        default_factory=dict,
    )
    reproducibility: dict[str, Any] = Field(
        default_factory=dict,
    )

    @field_validator(
        "experiment_id",
        "benchmark_name",
        "benchmark_version",
        mode="after",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Experiment metadata text fields must not be blank")

        return normalized_value


class ExperimentResult(BaseModel):
    """Complete validated result produced by a retrieval experiment."""

    metadata: ExperimentMetadata
    metrics: ExperimentMetrics
    error_summary: dict[str, int] = Field(
        default_factory=dict,
    )

    @field_validator(
        "error_summary",
    )
    @classmethod
    def validate_error_summary(
        cls,
        value: dict[str, int],
    ) -> dict[str, int]:
        for error_type, count in value.items():
            if not error_type.strip():
                raise ValueError("Error summary keys must not be blank")

            if count < 0:
                raise ValueError("Error summary counts must not be negative")

        return value
