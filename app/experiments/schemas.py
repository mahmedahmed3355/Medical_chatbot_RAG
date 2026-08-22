from pydantic import BaseModel, Field, field_validator


class BenchmarkCase(BaseModel):
    """A single retrieval benchmark case."""

    id: str = Field(
        min_length=1,
    )
    relevant_documents: list[str] = Field(
        min_length=1,
    )

    @field_validator(
        "id",
        mode="after",
    )
    @classmethod
    def validate_case_id(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Benchmark case id must not be blank")

        return value

    @field_validator(
        "relevant_documents",
    )
    @classmethod
    def validate_relevant_documents(
        cls,
        value: list[str],
    ) -> list[str]:
        normalized_documents: list[str] = []

        for document in value:
            normalized_document = document.strip()

            if not normalized_document:
                raise ValueError("Relevant document identifiers must not be blank")

            normalized_documents.append(normalized_document)

        return normalized_documents


class BenchmarkDataset(BaseModel):
    """Validated retrieval benchmark dataset."""

    dataset_name: str = Field(
        min_length=1,
    )
    version: str = Field(
        min_length=1,
    )
    cases: list[BenchmarkCase] = Field(
        min_length=1,
    )

    @field_validator(
        "dataset_name",
        "version",
        mode="after",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Benchmark text fields must not be blank")

        return value

    @field_validator(
        "cases",
    )
    @classmethod
    def validate_unique_case_ids(
        cls,
        value: list[BenchmarkCase],
    ) -> list[BenchmarkCase]:
        case_ids = [case.id for case in value]

        if len(case_ids) != len(set(case_ids)):
            raise ValueError("Benchmark case ids must be unique")

        return value
