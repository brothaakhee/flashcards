from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Word
from .serializers import WordSerializer
from ..utils import get_next_review_time


class WordListCreateView(generics.ListCreateAPIView):
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.filter(user=self.request.user)


class ReviewWordView(generics.GenericAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        user_words = Word.objects.filter(user=user).exclude(
            bin_number__in=[Word.HARD_TO_REMEMBER, Word.NEVER_REVIEW_AGAIN]
        )

        # Get words that are due for review
        words_due = user_words.filter(next_review__lte=timezone.now()).order_by(
            "-bin_number"
        )

        # If there are no words due for review, check bin 0
        if not words_due:
            bin_zero_words = user_words.filter(bin_number=0)

            if not bin_zero_words:
                if user_words.exists():
                    response = Response(
                        {
                            "message": "You are temporarily done! Please come back later to review more words."
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    response = Response(
                        {
                            "message": "You have no more words to review. You are permanently done!"
                        },
                        status=status.HTTP_200_OK,
                    )
                return response

            word = bin_zero_words.first()
        else:
            word = words_due.first()

        serializer = self.get_serializer(word)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        word_id = request.data.get("word_id")
        is_correct = request.data.get("is_correct")

        if word_id is None or is_correct is None:
            return Response(
                {"message": "word_id and is_correct are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        word = self.get_queryset().get(id=word_id)

        if is_correct:
            word.bin_number = min(Word.NEVER_REVIEW_AGAIN, word.bin_number + 1)
        else:
            word.bin_number = max(1, word.bin_number)
            word.wrong_attempts += 1

        if word.wrong_attempts >= 10:
            word.bin_number = Word.HARD_TO_REMEMBER
            word.next_review = None
        else:
            word.next_review = get_next_review_time(word.bin_number)

        word.save()
        serializer = self.get_serializer(word)
        return Response(serializer.data)
