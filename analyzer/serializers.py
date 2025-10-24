from rest_framework import serializers
from .models import AnalyzedString
from .utils import analyze_string

class AnalyzedStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedString
        fields = '__all__'
        read_only_fields = [
            'length',
            'is_palindrome',
            'unique_characters',
            'word_count',
            'sha256_hash',
            'character_frequency_map',
        ]

    def create(self, validated_data):
        text = validated_data['text']
        analyzed_data = analyze_string(text)
        return AnalyzedString.objects.create(**validated_data, **analyzed_data)
