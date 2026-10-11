from django.shortcuts import render

from rugby.content import page_context


def home(request):
    ctx = page_context()
    return render(request, "rugby/home.html", ctx)
