from django.contrib import admin

from website.models import AnalyzedWords

@admin.register(AnalyzedWords)
class AnalyzedWordsAdmin(admin.ModelAdmin):
    list_display = ('word', 'tf', 'frequency')
