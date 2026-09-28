from django.db import migrations

ACTIVE_PER_LEVEL_SKILL = 5


def trim_active_pool(apps, schema_editor):
    """Leave a handful of exercises per level and skill switched on.

    The catalog is much wider than anyone works through, and a queue that never
    ends is a queue nobody finishes. The rest of the rows stay in place, only
    inactive, so ``seed_poligon --full-catalog`` can bring them back.

    A database seeded after this migration lands already gets the same trim
    from the seed command. This is for the ones seeded before it.
    """
    exercise = apps.get_model("poligon", "Exercise")
    keep: list[int] = []
    for level, skill in exercise.objects.order_by().values_list("level", "skill").distinct():
        keep += list(
            exercise.objects.filter(level=level, skill=skill)
            .order_by("id")
            .values_list("id", flat=True)[:ACTIVE_PER_LEVEL_SKILL]
        )
    exercise.objects.exclude(id__in=keep).update(active=False)
    exercise.objects.filter(id__in=keep).update(active=True)


def activate_everything(apps, schema_editor):
    apps.get_model("poligon", "Exercise").objects.update(active=True)


class Migration(migrations.Migration):
    dependencies = [("poligon", "0007_learner_state_needs_an_account")]

    operations = [migrations.RunPython(trim_active_pool, activate_everything)]
