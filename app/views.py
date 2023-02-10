import io

from django.contrib import messages as msg
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse

from converter import PdfConverter
from converter.exceptions import ConvertImageError

from .models import GeneratedFile


def index(request):
    history = GeneratedFile.get_history(request.user)
    return render(request, "app/index.html", context={"history": history})


def convert(request):
    images = request.FILES.getlist("images", [])
    if not images:
        msg.error(request, "No file was selected")
        return redirect("app:index")
    try:
        pdf = PdfConverter(images).convert()
        if not request.user.is_anonymous:
            imagename = get_name_of_first_image(images)
            GeneratedFile.objects.create(
                filename=f"{imagename}.pdf",
                value=pdf.getvalue(),
                user=request.user,
            )
        return FileResponse(pdf, content_type="application/pdf")
    except ConvertImageError:
        msg.error(request, "Invalid File")
        return redirect("app:index")


def get_name_of_first_image(images: list):
    if not images:
        return ""
    return images[0].name.rsplit(".", 1)[0]


def get_pdf(request, id):
    try:
        pdf = GeneratedFile.objects.get(id=id, user=request.user.id).value
        return FileResponse(io.BytesIO(pdf), content_type="application/pdf")
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
