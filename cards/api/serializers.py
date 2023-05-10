from rest_framework import serializers
from ..models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id',
            'user',
            'word',
            'definition',
            'bin_number',
            'next_review',
            'wrong_attempts',
        ]
        read_only_fields = [
            'id',
            'user',
            'bin_number',
            'next_review',
            'wrong_attempts',
        ]

