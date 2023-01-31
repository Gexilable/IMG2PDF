import io

from PIL import Image


class PdfConverter:
    def __init__(self, images: list[bytes]):
        self.images = images

    def convert(self) -> bytes | None:
        try:
            images = self._open_images()
            data = self._get_pdf(images)
            return data
        except:
            return None

    def _get_pdf(self, images):
        output = io.BytesIO()
        images[0].save(output, "pdf", save_all=True, append_images=images[1:])
        output.seek(0)
        data = output.read()
        return data

    def _open_images(self):
        return [
            Image.open(io.BytesIO(image)).convert("RGB")
            for image in self.images
            if image
        ]
