from django.shortcuts import get_object_or_404, render

from analytics.utils import count_visit

from .models import Swieto


@count_visit
def wyraj_lista(request):
    """Lista wszystkich świąt Koła Roku."""
    swieta = Swieto.objects.prefetch_related("zrodla").order_by("kolejnosc", "tytul_pl")
    return render(request, "bies/wyraj/lista.html", {"swieta": swieta})


@count_visit
def wyraj_detail(request, slug):
    """
    Uniwersalny widok szczegółowy dla dowolnego święta.
    Zastępuje 7 osobnych widoków (wyraj_gaik, wyraj_radonica, itd.).
    """
    swieto = get_object_or_404(
        Swieto.objects.prefetch_related("zrodla"), slug=slug
    )
    return render(request, "bies/wyraj/detail.html", {"swieto": swieto})
