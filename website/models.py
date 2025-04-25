from django.db import models
from django.db.models import Model

# модель для файлов
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# модель для слов использованных во всех файдах
class AnalyzedWords(models.Model):
    word = models.CharField(max_length=200, unique=True)
    tf = models.FloatField()
    frequency = models.IntegerField(default=2) # количество файлов содержащих слово, оно начинаеться с 2, чтобы избежать ситуации логарифма с основанием 1
    current_file = models.ForeignKey(UploadedFile, related_name='words', on_delete=models.SET_NULL, null=True)  # принадлежность слова к текущему файлу

    class Meta:
        ordering = ['frequency']
