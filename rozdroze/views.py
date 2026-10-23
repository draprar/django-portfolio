from django.views.generic import TemplateView


class WybierzView(TemplateView):
    """
    Crossroads landing — tiles into codillin', bazgrollin', Wyraj, LingwoŁamki, wiciędze and iaio.

    On jedzien.pl this is also the site root.
    """

    template_name = "rozdroze/wybierz.html"
