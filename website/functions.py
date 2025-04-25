import re
from math import log

from website.models import AnalyzedWords, UploadedFile

# анализируем текст, функция возврашает библиотеку в форме{'слово': tf}
def analyzing_tf(text) -> dict:
    words: list = re.findall(r'\b\w+\b', text.lower()) # список слов, без знаков препинания
    word_counts: dict = {}
    text_length: int = len(words)
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    for word in word_counts:
        word_counts[word] = word_counts[word] / text_length #преобразуем частоту слова в тексте в tf

    return word_counts

# функция для внесения изменений в базу данных
def update_model(word_counts, file_id) -> None:
    words_list = AnalyzedWords.objects.values_list('word', flat=True) # список слов в базе данных
    for key, value in word_counts.items():
        if key in words_list: # если слово уже есть в базе данных то вносим изменения в tf, current_file и частоту слова
            word = AnalyzedWords.objects.get(word=key)
            word.tf = value
            word.current_file = UploadedFile.objects.get(id=file_id)
            word.frequency += 1
        else: # если слова нет, то вносим его в базу данных
            word = AnalyzedWords(word=key, tf=value, current_file=UploadedFile.objects.get(id=file_id))
        word.save()

# функция возврашает лист с нужными слова, лист позже используется в context для создания таблицы на сайте
def get_words(file_id) -> list:
    words = AnalyzedWords.objects.filter(current_file=file_id) # список объектов принадлежащих текущему файлу
    word_dicts = []
    for word in words:
        word_dicts.append({'word': word.word, 'tf': word.tf, 'idf': (log(file_id, word.frequency))})
    return word_dicts[:50]
