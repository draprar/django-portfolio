from django.shortcuts import render

from analytics.utils import count_visit


@count_visit
def wyraj_lista(request):
    return render(request, "bies/wyraj/lista.html")


@count_visit
def wyraj_swietowit_letni(request):
    return render(request, "bies/wyraj/swietowit-letni/index.html")