from typing import Optional


class CustomException(Exception):
    def __init__(
        self,
        message: str,
        error_detail: Optional[BaseException] = None,
    ):
        self.message = message
        self.error_detail = error_detail
        self.error_message = self._build_error_message()
        super().__init__(self.error_message)

    def _build_error_message(self) -> str:
        if self.error_detail is None:
            return self.message

        traceback = self.error_detail.__traceback__

        if traceback is None:
            return f"{self.message} | Error: {self.error_detail}"

        while traceback.tb_next is not None:
            traceback = traceback.tb_next

        file_name = traceback.tb_frame.f_code.co_filename
        line_number = traceback.tb_lineno

        return (
            f"{self.message} | Error: {self.error_detail} | File: {file_name} | Line: {line_number}"
        )

    def __str__(self):
        return self.error_message
