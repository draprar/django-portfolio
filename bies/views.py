from django.shortcuts import render

from analytics.utils import count_visit


@count_visit
def wyraj_lista(request):
    return render(request, "bies/wyraj/lista.html")


@count_visit
def wyraj_swietowit_letni(request):
    return render(request, "bies/wyraj/swietowit-letni/index.html")

@count_visit
def wyraj_gaik(request):
    return render(request, "bies/wyraj/gaik/index.html")

@count_visit
def wyraj_radonica(request):
    return render(request, "bies/wyraj/radonica/index.html")

@count_visit
def wyraj_smigus_dyngus(request):
    return render(request, "bies/wyraj/smigus-dyngus/index.html")

@count_visit
def wyraj_jare_gody(request):
    return render(request, "bies/wyraj/jare-gody/index.html")

@count_visit
def wyraj_miesopust(request):
    return render(request, "bies/wyraj/miesopust/index.html")

@count_visit
def wyraj_szczodre_gody(request):
    return render(request, "bies/wyraj/szczodre-gody/index.html")
