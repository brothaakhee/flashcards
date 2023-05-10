from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    HARD_TO_REMEMBER = 12
    NEVER_REVIEW_AGAIN = 11

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    definition = models.TextField()
    bin_number = models.PositiveIntegerField(default=0)
    wrong_attempts = models.PositiveIntegerField(default=0)
    next_review = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "word")

    def __str__(self):
        return f"{self.word}"
