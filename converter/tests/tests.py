from pathlib import Path

import pytest

from converter import PdfConverter



class TestConverter:



    @pytest.fixture(autouse=True)
    def setup(self):
        folder = Path(__file__).parent
        with open(folder/"test_img.png", "rb") as file:
            self.real_image = file.read()

    def test_convert_empty_list(self):
        pdf = PdfConverter([]).convert()
        assert pdf == None

    def test_convert_empty_bytes(self):
        pdf = PdfConverter([b""]).convert()
        assert pdf == None

    def test_convert_valid_bytes(self):
        pdf = PdfConverter([self.real_image]).convert()
        assert pdf != None

    def test_convert_invalid_bytes(self):
        pdf = PdfConverter([b"123"]).convert()
        assert pdf == None

    def test_convert_return_pdf(self):
        pdf = PdfConverter([self.real_image]).convert()
        assert b"PDF" in pdf
