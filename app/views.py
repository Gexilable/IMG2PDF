from django.contrib import messages as msg

from django.shortcuts import render, redirect
from django.http import FileResponse

from converter import PdfConverter
from converter.exceptions import ConvertImageError


def index(request):
    return render(request, "app/index.html")


def convert(request):
    images = request.FILES.getlist("images", [])
    if not images:
        msg.error(request, "No file was selected")
        return redirect("app:index")
    try:
        pdf = PdfConverter(images).convert()
        return FileResponse(pdf, content_type="application/pdf")
    except ConvertImageError:
        msg.error(request, "Invalid File")
        return redirect("app:index")
