import pytest
from pydantic import ValidationError

from app.schemas.prompt import PromptRequest


def test_valid_prompt_is_accepted():
    request = PromptRequest(prompt="What are the symptoms of diabetes?")

    assert request.prompt == "What are the symptoms of diabetes?"


def test_prompt_whitespace_is_trimmed():
    request = PromptRequest(prompt="  What is hypertension?  ")

    assert request.prompt == "What is hypertension?"


@pytest.mark.parametrize(
    "prompt",
    [
        "",
        " ",
        "   ",
        "\n",
        "\t",
    ],
)
def test_empty_prompt_is_rejected(prompt):
    with pytest.raises(ValidationError):
        PromptRequest(prompt=prompt)


def test_prompt_over_2000_characters_is_rejected():
    with pytest.raises(ValidationError):
        PromptRequest(prompt="a" * 2001)


def test_prompt_with_exactly_2000_characters_is_accepted():
    request = PromptRequest(prompt="a" * 2000)

    assert len(request.prompt) == 2000
