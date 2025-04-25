# views.py
from django.shortcuts import render
from .forms import UploadFileForm
from .functions import analyzing_tf, update_model, get_words
from .models import UploadedFile


def  index_view(request):
    word_dicts = []
    try:
        file_id = UploadedFile.objects.last().id  # id текущего файла
    except:
        file_id = 0

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save() #сохраняем файл
            file_path = uploaded_file.file.path
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            file_id = uploaded_file.id
            words = analyzing_tf(text) # вычисляем tf для каждого слова
            update_model(words, file_id) # вносим изменения в базу данных
            word_dicts = get_words(file_id)

    return render(request, 'index.html', {'last_file':file_id, 'word_dicts': word_dicts})
