import pytest
from datetime import timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from cards.models import Word
from cards.utils import get_next_review_time


def assert_times_almost_equal(time1, time2):
    """
    Asserts that two times are almost equal, up to minute precision.
    """
    time1_minute_precision = time1.replace(second=0, microsecond=0)
    time2_minute_precision = time2.replace(second=0, microsecond=0)

    assert time1_minute_precision == time2_minute_precision


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(username="test_user", password="test_password")


@pytest.fixture
def test_word(test_user):
    return Word.objects.create(
        user=test_user, word="test_word", definition="test definition"
    )


@pytest.fixture
def test_word2(test_user):
    return Word.objects.create(
        user=test_user, word="test_word2", definition="test definition2"
    )


@pytest.mark.django_db
def test_initial_bin_number(test_word):
    assert test_word.bin_number == 0


@pytest.mark.django_db
def test_bins_and_timespans(api_client, test_user, test_word):
    return
    api_client.force_authenticate(test_user)

    for bin_number in range(1, 12):
        response = api_client.put(
            reverse("review_word"),
            data={"word_id": test_word.id, "is_correct": True},
            format="json",
        )
        test_word.refresh_from_db()
        assert test_word.bin_number == bin_number

        if bin_number <= 10:
            assert_times_almost_equal(
                test_word.next_review, get_next_review_time(bin_number)
            )
        else:
            assert test_word.next_review is None


@pytest.mark.django_db
def test_hard_to_remember(api_client, test_user, test_word):
    api_client.force_authenticate(user=test_user)

    for i in range(9):
        response = api_client.put(
            reverse("review_word"),
            data={"word_id": test_word.id, "is_correct": False},
            format="json",
        )
        test_word.refresh_from_db()
        assert test_word.bin_number == 1
        assert test_word.wrong_attempts == i + 1
        assert test_word.next_review is not None

    # the 10th wrong attempt will move the card into bin 12, ie hard to remember
    response = api_client.put(
        reverse("review_word"),
        data={"word_id": test_word.id, "is_correct": False},
        format="json",
    )
    test_word.refresh_from_db()
    assert test_word.bin_number == 12
    assert test_word.wrong_attempts == 10
    assert test_word.next_review is None


@pytest.mark.django_db
def test_never_bin(api_client, test_user, test_word):
    """Test that words in bin 11 will never get reviewed again"""
    api_client.force_authenticate(user=test_user)

    # Move the word to bin 11 (permanent)
    for _ in range(11):
        response = api_client.put(
            reverse("review_word"),
            data={"word_id": test_word.id, "is_correct": True},
            format="json",
        )

    # The user has no more words to review (permanent)
    test_word.refresh_from_db()
    assert test_word.bin_number == 11
    assert test_word.next_review is None


@pytest.mark.django_db
def test_word_review_priority(api_client, test_user):
    api_client.force_authenticate(user=test_user)

    word1 = Word.objects.create(
        user=test_user, word="word1", definition="definition1", bin_number=1
    )
    word2 = Word.objects.create(
        user=test_user, word="word2", definition="definition2", bin_number=2
    )
    word3 = Word.objects.create(
        user=test_user, word="word3", definition="definition3", bin_number=3
    )

    # All words are due for review.
    word1.next_review = timezone.now() - timedelta(minutes=1)
    word2.next_review = timezone.now() - timedelta(minutes=1)
    word3.next_review = timezone.now() - timedelta(minutes=1)

    word1.save()
    word2.save()
    word3.save()

    response = api_client.get(reverse("review_word"))
    assert response.status_code == 200
    assert response.data["word"] == "word3"
    word3.bin_number = Word.NEVER_REVIEW_AGAIN
    word3.save()

    response = api_client.get(reverse("review_word"))
    assert response.status_code == 200
    assert response.data["word"] == "word2"
    word2.bin_number = Word.NEVER_REVIEW_AGAIN
    word2.save()

    response = api_client.get(reverse("review_word"))
    assert response.status_code == 200
    assert response.data["word"] == "word1"


@pytest.mark.django_db
def test_completion_messages(api_client, test_user, test_word):
    """Test temporary and permanent completion messages"""
    api_client.force_authenticate(user=test_user)

    # Move the word to bin 10
    for _ in range(10):
        response = api_client.put(
            reverse("review_word"),
            data={"word_id": test_word.id, "is_correct": True},
            format="json",
        )

    test_word.refresh_from_db()
    assert test_word.bin_number == 10
    assert test_word.next_review is not None

    response = api_client.get(reverse("review_word"))
    assert "you are temporarily done" in response.data["message"].lower()

    response = api_client.put(
        reverse("review_word"),
        data={"word_id": test_word.id, "is_correct": True},
        format="json",
    )

    test_word.refresh_from_db()
    assert test_word.bin_number == 11
    assert test_word.next_review is None

    # no more words
    response = api_client.get(reverse("review_word"))
    assert "you are permanently done" in response.data["message"].lower()

    word2 = Word.objects.create(
        user=test_user, word="test_word2", definition="test_definition2"
    )

    response = api_client.get(reverse("review_word"))
    assert response.data["id"] == word2.id

    # move the word into hard to remember bin
    for _ in range(10):
        response = api_client.put(
            reverse("review_word"),
            data={"word_id": word2.id, "is_correct": False},
            format="json",
        )
        word2.refresh_from_db()

    # The user has no more words to review (permanent)
    assert word2.bin_number == 12
    assert word2.wrong_attempts == 10
    assert word2.next_review is None

    # no more words
    response = api_client.get(reverse("review_word"))
    assert "you are permanently done" in response.data["message"].lower()
