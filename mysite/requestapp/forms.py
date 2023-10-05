from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

def validate_file(file: InMemoryUploadedFile) -> None:
    if file.size > 1048576:
        raise ValidationError("Размер файла больше 1Мб")

class UploadFileForm(forms.Form):
    file_name = forms.FileField(label="Имя файла:", validators=[validate_file])