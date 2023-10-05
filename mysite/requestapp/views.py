from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import UploadFileForm

def handle_upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.cleaned_data("file-name")
            fs = FileSystemStorage()
            file_name= fs.save(new_file.name, new_file)
            print(file_name, 'is save')
    else:
        form = UploadFileForm()
    context = {
        "form": form,
    }
    return render(request, "requestapp/request-upload-file.html", context=context)