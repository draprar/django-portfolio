import json

from django.shortcuts import get_object_or_404, render

from analytics.utils import count_visit

from .models import Swieto


@count_visit
def wyraj_lista(request):
    # Fetch all festivals with related bibliographic sources.
    swieta = Swieto.objects.prefetch_related("zrodla").order_by("kolejnosc", "tytul_pl")

    # Data for the Wheel of the Year SVG.
    # podtytul_* included so the JS panel can show a subtitle per node.
    kolo_data = json.dumps(
        [
            {
                "slug":        s.slug,
                "tytul_pl":    s.tytul_pl,
                "tytul_en":    s.tytul_en,
                "podtytul_pl": s.podtytul_pl,
                "podtytul_en": s.podtytul_en,
                "kat":         s.kolo_kat,
                "kolor":       s.kolo_kolor,
                "dzien_roku":  s.dzien_roku,
                "dzien_roku_koniec": s.dzien_roku_koniec,  # None for ordinary single-day feasts
                "url":         f"/wyraj/{s.slug}/",
                "obraz":       s.obraz.url if s.obraz else "",
            }
            for s in swieta
        ],
        ensure_ascii=False,
    )

    return render(
        request,
        "bies/wyraj/lista.html",
        {
            "swieta":    swieta,
            "kolo_data": kolo_data,
        },
    )


@count_visit
def wyraj_detail(request, slug):
    # Fetch single festival with related sources, or return 404.
    swieto = get_object_or_404(
        Swieto.objects.prefetch_related("zrodla"),
        slug=slug,
    )

    return render(
        request,
        "bies/wyraj/detail.html",
        {
            "swieto":       swieto,
            "prev":         swieto.get_prev(),
            "next":         swieto.get_next(),
            # Pre-split deity lists for each language so the template
            # doesn't have to call get_duchy_list() with a lang argument.
            "duchy_pl_list": swieto.get_duchy_list("pl"),
            "duchy_en_list": swieto.get_duchy_list("en"),
        },
    )