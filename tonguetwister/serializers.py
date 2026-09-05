from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Articulator, Exercise, Funfact, OldPolish, Trivia, Twister
from .services import is_email_confirmed


class OldPolishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldPolish
        fields = ["id", "old_text", "new_text"]


class ArticulatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulator
        fields = ["id", "text"]


class FunfactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funfact
        fields = ["id", "text"]


class TwisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twister
        fields = ["id", "text"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "text"]


class TriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = ["id", "text"]


class EmailConfirmedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not is_email_confirmed(self.user):
            raise serializers.ValidationError("Potwierdź adres e-mail, zanim się zalogujesz.")
        return data
