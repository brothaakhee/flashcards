from datetime import timedelta
from django.utils import timezone


def get_next_review_time(bin_number):
    timespans = [
        timedelta(seconds=5),
        timedelta(seconds=25),
        timedelta(minutes=2),
        timedelta(minutes=10),
        timedelta(hours=1),
        timedelta(hours=5),
        timedelta(days=1),
        timedelta(days=5),
        timedelta(days=25),
        timedelta(days=120),
    ]

    if bin_number >= 1 and bin_number <= 10:
        return timezone.now() + timespans[bin_number - 1]

    return None
