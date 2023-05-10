from django.db import migrations
from django.contrib.auth.models import User
from faker import Faker
import random


def populate_words(apps, schema_editor):
    Word = apps.get_model("cards", "Word")
    fake = Faker()

    for user in User.objects.all():
        # generate 20 random words and definitions for each user
        for i in range(10):
            word = fake.word()
            definition = fake.sentence(nb_words=10)
            # create and save a new `Word` object with the random data
            Word.objects.create(
                user_id=user.id,
                word=word,
                definition=definition,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("cards", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_words),
    ]
