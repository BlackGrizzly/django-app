from django.urls import path
from .views import handle_upload_file

app_name = "requestapp"

urlpatterns = [
    path("upload/", handle_upload_file, name="handle-upload-file"),
]