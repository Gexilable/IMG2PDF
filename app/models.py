from django.conf import settings
from django.db import models


class GeneratedFile(models.Model):
    filename = models.CharField(max_length=256)
    value = models.BinaryField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

