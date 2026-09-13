from django.views.generic import TemplateView


class WybierzView(TemplateView):
    """
    Crossroads landing — tiles into gallery, Wyraj, LingwoŁamki and kodzillin'.

    On jedzien.pl this is also the site root.
    """

    template_name = "rozdroze/wybierz.html"
