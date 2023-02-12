from django.urls import path

from app import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("convert", views.convert, name="convert"),
    path("pdf/<int:id>", views.get_pdf, name="pdf"),
    path("pdf/delete/<int:id>", views.delete_file, name="delete_pdf"),
]
