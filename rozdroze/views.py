from django.views.generic import TemplateView


class WybierzView(TemplateView):
    """
    A single "crossroads" landing page — the one link you'd put in an
    Instagram bio — that lets a visitor pick between the two separate
    apps living in this project (the bazgrollin' gallery and Wyraj).

    kodzillin' (/code/) is the fourth tile — still a local experiment
    until the GIF and copy are signed off.
    """

    template_name = "rozdroze/wybierz.html"
