from django import forms
from .models import UploadedFile
# форма для закрузки файла
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']