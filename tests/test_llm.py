from unittest.mock import Mock, patch

import pytest

from app.common.custom_exception import CustomException
from app.components.llm import load_llm


def test_load_llm_requires_repository():
    with pytest.raises(
        CustomException,
        match="repository ID is required",
    ):
        load_llm(
            huggingface_repo_id="",
            hf_token="token",
        )


def test_load_llm_requires_token():
    with pytest.raises(
        CustomException,
        match="HF_TOKEN is required",
    ):
        load_llm(
            huggingface_repo_id="repo",
            hf_token=None,
        )


@patch("app.components.llm.HuggingFaceEndpoint")
def test_load_llm_success(mock_endpoint):
    llm = Mock()
    mock_endpoint.return_value = llm

    result = load_llm(
        huggingface_repo_id="repo",
        hf_token="token",
    )

    assert result is llm

    mock_endpoint.assert_called_once_with(
        repo_id="repo",
        huggingfacehub_api_token="token",
        temperature=0.3,
        max_new_tokens=256,
        return_full_text=False,
    )
