import io

from django.shortcuts import render
from django.http import FileResponse, Http404



def index(request):
    return render(request, "app/index.html")


def convert(request):
    try:
        return FileResponse(io.BytesIO(b"123"), content_type="application/pdf")
    except FileNotFoundError:
        raise Http404()
