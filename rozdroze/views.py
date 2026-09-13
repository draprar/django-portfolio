from django.views.generic import TemplateView

from core.forms import portal_contact_form


class WybierzView(TemplateView):
    """
    Crossroads landing — tiles into gallery, Wyraj, LingwoŁamki and kodzillin'.

    On jedzien.pl this is also the site root. Contact sits under the tiles.
    """

    template_name = "rozdroze/wybierz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = portal_contact_form(bilingual=False)
        return context
