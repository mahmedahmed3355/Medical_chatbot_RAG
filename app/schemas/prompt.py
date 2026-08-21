from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    """Validation schema for user prompts."""

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Prompt must not be empty.")

        return value
