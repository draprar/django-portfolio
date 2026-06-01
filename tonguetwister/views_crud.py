from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ArticulatorForm,
    ExerciseForm,
    FunfactForm,
    OldPolishForm,
    TriviaForm,
    TwisterForm,
)
from .models import Articulator, Exercise, Funfact, OldPolish, Trivia, Twister


def is_admin(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin)
def articulator_list(request):
    articulators = Articulator.objects.all()
    return render(request, "tonguetwister/articulators/articulator_list.html", {"articulators": articulators})


@user_passes_test(is_admin)
def articulator_add(request):
    if request.method == "POST":
        form = ArticulatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("articulator_list")
    else:
        form = ArticulatorForm()
    return render(request, "tonguetwister/articulators/articulator_form.html", {"form": form})


@user_passes_test(is_admin)
def articulator_edit(request, pk):
    articulator = get_object_or_404(Articulator, pk=pk)
    if request.method == "POST":
        form = ArticulatorForm(request.POST, instance=articulator)
        if form.is_valid():
            form.save()
            return redirect("articulator_list")
    else:
        form = ArticulatorForm(instance=articulator)
    return render(request, "tonguetwister/articulators/articulator_form.html", {"form": form})


@user_passes_test(is_admin)
def articulator_delete(request, pk):
    articulator = get_object_or_404(Articulator, pk=pk)
    if request.method == "POST":
        articulator.delete()
        return redirect("articulator_list")
    return render(request, "tonguetwister/articulators/articulator_confirm_delete.html", {"articulator": articulator})


@user_passes_test(is_admin)
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, "tonguetwister/exercises/exercise_list.html", {"exercises": exercises})


@user_passes_test(is_admin)
def exercise_add(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exercise_list")
    else:
        form = ExerciseForm()
    return render(request, "tonguetwister/exercises/exercise_form.html", {"form": form})


@user_passes_test(is_admin)
def exercise_edit(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == "POST":
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect("exercise_list")
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, "tonguetwister/exercises/exercise_form.html", {"form": form})


@user_passes_test(is_admin)
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == "POST":
        exercise.delete()
        return redirect("exercise_list")
    return render(request, "tonguetwister/exercises/exercise_confirm_delete.html", {"exercise": exercise})


@user_passes_test(is_admin)
def twister_list(request):
    twisters = Twister.objects.all()
    return render(request, "tonguetwister/twisters/twister_list.html", {"twisters": twisters})


@user_passes_test(is_admin)
def twister_add(request):
    if request.method == "POST":
        form = TwisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("twister_list")
    else:
        form = TwisterForm()
    return render(request, "tonguetwister/twisters/twister_form.html", {"form": form})


@user_passes_test(is_admin)
def twister_edit(request, pk):
    twister = get_object_or_404(Twister, pk=pk)
    if request.method == "POST":
        form = TwisterForm(request.POST, instance=twister)
        if form.is_valid():
            form.save()
            return redirect("twister_list")
    else:
        form = TwisterForm(instance=twister)
    return render(request, "tonguetwister/twisters/twister_form.html", {"form": form})


@user_passes_test(is_admin)
def twister_delete(request, pk):
    twister = get_object_or_404(Twister, pk=pk)
    if request.method == "POST":
        twister.delete()
        return redirect("twister_list")
    return render(request, "tonguetwister/twisters/twister_confirm_delete.html", {"twister": twister})


@user_passes_test(is_admin)
def trivia_list(request):
    trivia = Trivia.objects.all()
    return render(request, "tonguetwister/trivia/trivia_list.html", {"trivia": trivia})


@user_passes_test(is_admin)
def trivia_add(request):
    if request.method == "POST":
        form = TriviaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("trivia_list")
    else:
        form = TriviaForm()
    return render(request, "tonguetwister/trivia/trivia_form.html", {"form": form})


@user_passes_test(is_admin)
def trivia_edit(request, pk):
    trivia = get_object_or_404(Trivia, pk=pk)
    if request.method == "POST":
        form = TriviaForm(request.POST, instance=trivia)
        if form.is_valid():
            form.save()
            return redirect("trivia_list")
    else:
        form = TriviaForm(instance=trivia)
    return render(request, "tonguetwister/trivia/trivia_form.html", {"form": form})


@user_passes_test(is_admin)
def trivia_delete(request, pk):
    t = get_object_or_404(Trivia, pk=pk)
    if request.method == "POST":
        t.delete()
        return redirect("trivia_list")
    return render(request, "tonguetwister/trivia/trivia_confirm_delete.html", {"t": t})


@user_passes_test(is_admin)
def funfact_list(request):
    funfacts = Funfact.objects.all()
    return render(request, "tonguetwister/funfacts/funfact_list.html", {"funfacts": funfacts})


@user_passes_test(is_admin)
def funfact_add(request):
    if request.method == "POST":
        form = FunfactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("funfact_list")
    else:
        form = FunfactForm()
    return render(request, "tonguetwister/funfacts/funfact_form.html", {"form": form})


@user_passes_test(is_admin)
def funfact_edit(request, pk):
    funfact = get_object_or_404(Funfact, pk=pk)
    if request.method == "POST":
        form = FunfactForm(request.POST, instance=funfact)
        if form.is_valid():
            form.save()
            return redirect("funfact_list")
    else:
        form = FunfactForm(instance=funfact)
    return render(request, "tonguetwister/funfacts/funfact_form.html", {"form": form})


@user_passes_test(is_admin)
def funfact_delete(request, pk):
    funfact = get_object_or_404(Funfact, pk=pk)
    if request.method == "POST":
        funfact.delete()
        return redirect("funfact_list")
    return render(request, "tonguetwister/funfacts/funfact_confirm_delete.html", {"funfact": funfact})


@user_passes_test(is_admin)
def oldpolish_list(request):
    oldpolishs = OldPolish.objects.all()
    return render(request, "tonguetwister/oldpolishs/oldpolish_list.html", {"oldpolishs": oldpolishs})


@user_passes_test(is_admin)
def oldpolish_add(request):
    if request.method == "POST":
        form = OldPolishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("oldpolish_list")
    else:
        form = OldPolishForm()
    return render(request, "tonguetwister/oldpolishs/oldpolish_form.html", {"form": form})


@user_passes_test(is_admin)
def oldpolish_edit(request, pk):
    oldpolish = get_object_or_404(OldPolish, pk=pk)
    if request.method == "POST":
        form = OldPolishForm(request.POST, instance=oldpolish)
        if form.is_valid():
            form.save()
            return redirect("oldpolish_list")
    else:
        form = OldPolishForm(instance=oldpolish)
    return render(request, "tonguetwister/oldpolishs/oldpolish_form.html", {"form": form})


@user_passes_test(is_admin)
def oldpolish_delete(request, pk):
    oldpolish = get_object_or_404(OldPolish, pk=pk)
    if request.method == "POST":
        oldpolish.delete()
        return redirect("oldpolish_list")
    return render(request, "tonguetwister/oldpolishs/oldpolish_confirm_delete.html", {"oldpolish": oldpolish})

