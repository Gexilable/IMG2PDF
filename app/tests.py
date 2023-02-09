import io
from pathlib import Path

from django.contrib.auth import login
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from pypdf import PdfReader

from app.models import GeneratedFile


class ConvertTestCase(TestCase):
    def setUp(self) -> None:
        self.url = reverse("app:convert")
        self.invalid_image = self._get_invalid_image()
        self.image_count = 0

    def assertMessageIn(self, message, response):
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(message, messages)

    def assertPdfPages(self, number_of_pages, response):
        pdf = PdfReader(io.BytesIO(response.getvalue()))
        self.assertEqual(len(pdf.pages), number_of_pages)

    def _get_image(self, imagename: str = None, filename: str = "test_img.png"):
        folder = Path(__file__).parent
        with open(folder / "tests" / filename, "rb") as img:
            self.image_count += 1
            return SimpleUploadedFile(
                imagename or f"{self.image_count}.png",
                img.read(),
                content_type="application/png",
            )

    def _get_invalid_image(self):
        return SimpleUploadedFile(
            "test_image.png", b"image", content_type="application/png"
        )


class LoggedInConvertTestCase(ConvertTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_user(username="test", password="test")
        self.client.login(username="test", password="test")


class TestConvertView(ConvertTestCase):
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
        self.assertPdfPages(1, response)

    def test_send_multiple_files_return_pdf_file_with_multiple_pages(self):
        response = self.client.post(
            self.url, {"images": [self._get_image(), self._get_image()]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        self.assertPdfPages(2, response)


class TestConvertViewLoggedIn(LoggedInConvertTestCase, TestConvertView):
    pass


class TestConvertGeneratedFile(LoggedInConvertTestCase):
    def test_send_valid_file_create_generated_file(self):
        count_files_before = GeneratedFile.objects.count()
        self.client.post(self.url, {"images": self._get_image()})
        count_files_after = GeneratedFile.objects.count()
        count_files = count_files_after - count_files_before
        self.assertEqual(count_files, 1)

    def test_generated_file_has_correct_filename(self):
        self.client.post(self.url, {"images": self._get_image(imagename="test.png")})
        generated = GeneratedFile.objects.first()
        self.assertEqual(generated.filename, "test.pdf")

    def test_given_file_without_extension_return_correct_pdf_name(self):
        self.client.post(self.url, {"images": self._get_image(imagename="test")})
        generated = GeneratedFile.objects.first()
        self.assertEqual(generated.filename, "test.pdf")

    def test_given_file_with_2_dots_return_correct_pdf_name(self):
        self.client.post(
            self.url, {"images": self._get_image(imagename="test.ext.png")}
        )
        generated = GeneratedFile.objects.first()
        self.assertEqual(generated.filename, "test.ext.pdf")


class TestHistory(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_anonymous_user_does_not_have_history(self):
        GeneratedFile.objects.create(value=b"123", user=self.user)
        anonymous_user = AnonymousUser()
        history = GeneratedFile.get_history(anonymous_user)
        self.assertEqual(history, [])

    def test_logged_in_user_does_not_have_history(self):
        history = GeneratedFile.get_history(self.user)
        self.assertEqual(history, [])

    def test_logged_in_user_has_own_history(self):
        file = GeneratedFile.objects.create(value=b"123", user=self.user)
        history = GeneratedFile.get_history(self.user)
        self.assertIn(file, history)

    def test_user_has_not_another_user_history(self):
        self.user2 = User.objects.create_user(username="test2", password="test2")
        file1 = GeneratedFile.objects.create(value=b"123", user=self.user)
        file2 = GeneratedFile.objects.create(value=b"123", user=self.user2)
        history1 = GeneratedFile.get_history(self.user)
        self.assertIn(file1, history1)
        self.assertNotIn(file2, history1)
