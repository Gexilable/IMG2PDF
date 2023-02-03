from pathlib import Path
from io import BytesIO

import pytest

from converter import PdfConverter
from converter.exceptions import ConvertImageError


class TestConverter:
    @pytest.fixture(autouse=True)
    def setup(self):
        folder = Path(__file__).parent
        with open(folder / "test_img.png", "rb") as file:
            self.real_image = BytesIO(file.read())

    def test_convert_empty_list(self):
        with pytest.raises(ConvertImageError):
            PdfConverter([]).convert()

    def test_convert_empty_bytes(self):
        with pytest.raises(ConvertImageError):
            PdfConverter([BytesIO(b"")]).convert()

    def test_convert_valid_bytes(self):
        pdf = PdfConverter([self.real_image]).convert()
        body = pdf.read()
        assert body
        assert b"PDF" in body

    def test_convert_invalid_bytes(self):
        with pytest.raises(ConvertImageError):
            PdfConverter([BytesIO(b"123")]).convert()
