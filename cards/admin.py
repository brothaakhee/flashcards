from django.contrib import admin
from .models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "word",
        "definition",
        "bin_number",
        "next_review",
        "wrong_attempts",
    )


admin.site.register(Word, WordAdmin)
