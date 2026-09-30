from rest_framework import serializers

from walczak.models import Fact, Source, Style, StyleType, Tag


class StyleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleType
        fields = ["code", "name_pl", "name_en"]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["title", "url", "author", "source_type", "license", "license_url", "attribution"]


class StyleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ["slug", "name_pl", "name_en", "family", "region"]


class StyleDetailSerializer(serializers.ModelSerializer):
    style_types = StyleTypeSerializer(many=True)
    sources = SourceSerializer(many=True)

    class Meta:
        model = Style
        fields = [
            "slug",
            "name_pl",
            "name_en",
            "family",
            "origin_pl",
            "origin_en",
            "region",
            "period_pl",
            "period_en",
            "summary_pl",
            "summary_en",
            "history_pl",
            "history_en",
            "practice_pl",
            "practice_en",
            "style_types",
            "sources",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["slug", "name_pl", "name_en"]


class FactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = ["text_pl", "text_en", "is_legend"]
