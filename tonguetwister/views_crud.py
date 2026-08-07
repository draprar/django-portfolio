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


admin_required = user_passes_test(is_admin)


def make_crud_views(*, model, form_class, template_dir, list_context_name, delete_context_name, list_url_name):
    """
    Builds the standard list/add/edit/delete view quartet for a simple
    admin-managed "text" model (Articulator, Exercise, Twister, Trivia,
    Funfact, OldPolish all follow this exact same shape).

    This replaces ~24 hand-written, near-identical view functions with one
    factory + a small config table below, while keeping every URL name,
    template path, context variable name, and redirect target byte-for-byte
    identical to the views it replaces — existing templates and urls.py
    keep working completely unchanged.
    """
    template_prefix = model.__name__.lower()

    @admin_required
    def list_view(request):
        objects = model.objects.all()
        return render(
            request,
            f"tonguetwister/{template_dir}/{template_prefix}_list.html",
            {list_context_name: objects},
        )

    @admin_required
    def add_view(request):
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(list_url_name)
        else:
            form = form_class()
        return render(request, f"tonguetwister/{template_dir}/{template_prefix}_form.html", {"form": form})

    @admin_required
    def edit_view(request, pk):
        instance = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            form = form_class(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect(list_url_name)
        else:
            form = form_class(instance=instance)
        return render(request, f"tonguetwister/{template_dir}/{template_prefix}_form.html", {"form": form})

    @admin_required
    def delete_view(request, pk):
        instance = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            instance.delete()
            return redirect(list_url_name)
        return render(
            request,
            f"tonguetwister/{template_dir}/{template_prefix}_confirm_delete.html",
            {delete_context_name: instance},
        )

    return list_view, add_view, edit_view, delete_view


articulator_list, articulator_add, articulator_edit, articulator_delete = make_crud_views(
    model=Articulator,
    form_class=ArticulatorForm,
    template_dir="articulators",
    list_context_name="articulators",
    delete_context_name="articulator",
    list_url_name="articulator_list",
)

exercise_list, exercise_add, exercise_edit, exercise_delete = make_crud_views(
    model=Exercise,
    form_class=ExerciseForm,
    template_dir="exercises",
    list_context_name="exercises",
    delete_context_name="exercise",
    list_url_name="exercise_list",
)

twister_list, twister_add, twister_edit, twister_delete = make_crud_views(
    model=Twister,
    form_class=TwisterForm,
    template_dir="twisters",
    list_context_name="twisters",
    delete_context_name="twister",
    list_url_name="twister_list",
)

trivia_list, trivia_add, trivia_edit, trivia_delete = make_crud_views(
    model=Trivia,
    form_class=TriviaForm,
    template_dir="trivia",
    list_context_name="trivia",
    # NOTE: kept as "t" (not "trivia") to match the pre-existing
    # trivia_confirm_delete.html template, which references {{ t }}.
    delete_context_name="t",
    list_url_name="trivia_list",
)

funfact_list, funfact_add, funfact_edit, funfact_delete = make_crud_views(
    model=Funfact,
    form_class=FunfactForm,
    template_dir="funfacts",
    list_context_name="funfacts",
    delete_context_name="funfact",
    list_url_name="funfact_list",
)

oldpolish_list, oldpolish_add, oldpolish_edit, oldpolish_delete = make_crud_views(
    model=OldPolish,
    form_class=OldPolishForm,
    template_dir="oldpolishs",
    list_context_name="oldpolishs",
    delete_context_name="oldpolish",
    list_url_name="oldpolish_list",
)
