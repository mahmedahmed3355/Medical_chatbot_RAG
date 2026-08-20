from app.common.custom_exception import CustomException


def test_custom_exception_without_detail():
    error = CustomException("Something failed")

    assert str(error) == "Something failed"


def test_custom_exception_with_detail():
    try:
        raise ValueError("original failure")
    except ValueError as exc:
        error = CustomException(
            "Operation failed",
            exc,
        )

    assert "Operation failed" in str(error)
    assert "original failure" in str(error)
    assert "File:" in str(error)
    assert "Line:" in str(error)
