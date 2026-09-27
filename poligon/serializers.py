from rest_framework import serializers


class ProgressSerializer(serializers.Serializer):
    target_profile = serializers.CharField()
    scores = serializers.DictField(child=serializers.IntegerField())
    submissions = serializers.IntegerField()
    due_reviews = serializers.IntegerField()
