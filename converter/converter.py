from io import BytesIO

from PIL import Image

from converter.exceptions import ConvertImageError


class PdfConverter:
    def __init__(self, images: list[BytesIO]):
        self.images = images

    def convert(self) -> BytesIO:
        try:
            images = self._open_images()
            data = self._get_pdf(images)
            return data
        except Exception as ex:
            raise ConvertImageError from ex

    def _get_pdf(self, images: list[Image]):
        output = BytesIO()
        images[0].save(output, "pdf", save_all=True, append_images=images[1:])
        output.seek(0)
        return output

    def _open_images(self):
        return [Image.open(image).convert("RGB") for image in self.images if image]
