import io
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages


class TestConvertView(TestCase):
    def setUp(self) -> None:
        self.url = reverse("app:convert")
        self.invalid_image = self._get_invalid_image()
        self.image_count = 0

    def test_send_without_files_return_page_with_error(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertMessageIn("No file was selected", response)

    def test_send_empty_form_return_page_with_error(self):
        response = self.client.post(self.url, {"images": []})
        self.assertEqual(response.status_code, 302)
        self.assertMessageIn("No file was selected", response)

    def test_send_invalid_file_return_page_with_error(self):
        response = self.client.post(self.url, {"images": self.invalid_image})
        self.assertEqual(response.status_code, 302)
        self.assertMessageIn("Invalid File", response)

    def test_form_with_wrong_input_name(self):
        response = self.client.post(self.url, {"INVALID": self.invalid_image})
        self.assertEqual(response.status_code, 302)
        self.assertMessageIn("No file was selected", response)

    def test_send_valid_file_return_pdf_file(self):
        response = self.client.post(self.url, {"images": self._get_image()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")

    def test_send_multiple_files_return_pdf_file_with_multiple_pages(self):
        response = self.client.post(self.url, {"images": [self._get_image(), self._get_image()]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")

    def assertMessageIn(self, message, response):
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(message, messages)

    def _get_image(self, name: str = "test_img.png"):
        folder = Path(__file__).parent
        with open(folder / "tests" / name, "rb") as img:
            self.image_count += 1
            return SimpleUploadedFile(
                f"{self.image_count}.png", img.read(), content_type="application/png"
            )

    def _get_invalid_image(self):
        return SimpleUploadedFile(
            "test_image.png", b"image", content_type="application/png"
        )
