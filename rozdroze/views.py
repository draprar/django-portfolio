from django.views.generic import TemplateView


class WybierzView(TemplateView):
    """
    A single "crossroads" landing page — the one link you'd put in an
    Instagram bio — that lets a visitor pick between the two separate
    apps living in this project (the bazgrollin' gallery and Wyraj).

    No model, no context needed: the two destinations are just hardcoded
    links in the template. If a third destination ever shows up, this is
    the place to turn `panels` into real context data instead.
    """

    template_name = "rozdroze/wybierz.html"
