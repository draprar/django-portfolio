from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from walczak.models import Fact, Style, Tag
from walczak.serializers import FactSerializer, StyleDetailSerializer, StyleListSerializer, TagSerializer


@method_decorator(cache_control(public=True, max_age=300), name="dispatch")
class MartialArtListView(generics.ListAPIView):
    queryset = Style.objects.filter(active=True).order_by("sort_order", "slug")
    serializer_class = StyleListSerializer
    pagination_class = None


@method_decorator(cache_control(public=True, max_age=300), name="dispatch")
class MartialArtDetailView(generics.RetrieveAPIView):
    queryset = Style.objects.filter(active=True).prefetch_related("style_types", "sources")
    serializer_class = StyleDetailSerializer
    lookup_field = "slug"


@method_decorator(cache_control(public=True, max_age=300), name="dispatch")
class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


@method_decorator(cache_control(private=True, no_store=True), name="dispatch")
class RandomFactView(generics.GenericAPIView):
    serializer_class = FactSerializer

    def get(self, request: Request) -> Response:
        fact = Fact.objects.order_by("?").first()
        if fact is None:
            return Response({"text_pl": "", "text_en": "", "is_legend": False})
        return Response(FactSerializer(fact).data)
