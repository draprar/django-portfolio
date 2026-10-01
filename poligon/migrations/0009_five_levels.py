import json
from pathlib import Path

import django.core.validators
from django.db import migrations, models

ACTIVE_SLUGS_PATH = Path(__file__).resolve().parents[1] / "data" / "active_slugs.json"


def lift_level_zero(apps, schema_editor):
    """Move the old floor onto level 1 and switch on only the curated queue.

    Level 0 and level 1 are not kept apart: a reverse migration cannot tell
    which rows used to be the floor. History stays, because submissions and
    reviews point at the row, not at the number.
    """
    learner_state = apps.get_model("poligon", "LearnerState")
    for state in learner_state.objects.filter(practice_level=0):
        state.practice_level = 1
        state.target_profile = "1111"
        state.save(update_fields=["practice_level", "target_profile"])
    for state in learner_state.objects.all():
        profile = state.target_profile or ""
        if "0" in profile:
            state.target_profile = profile.replace("0", "1")
            state.save(update_fields=["target_profile"])

    exercise = apps.get_model("poligon", "Exercise")
    exercise.objects.filter(level=0).update(level=1)
    apps.get_model("poligon", "VocabularyItem").objects.filter(level=0).update(level=1)

    keep = set(json.loads(ACTIVE_SLUGS_PATH.read_text(encoding="utf-8")))
    exercise.objects.exclude(slug__in=keep).update(active=False)
    exercise.objects.filter(slug__in=keep).update(active=True)


class Migration(migrations.Migration):
    # PostgreSQL cannot ALTER TABLE in the same transaction as the updates above.
    atomic = False

    dependencies = [("poligon", "0008_trim_the_active_pool")]

    operations = [
        migrations.RunPython(lift_level_zero, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="learnerstate",
            name="practice_level",
            field=models.PositiveSmallIntegerField(
                default=2,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="learnerstate",
            constraint=models.CheckConstraint(
                condition=models.Q(("practice_level__gte", 1), ("practice_level__lte", 5)),
                name="poligon_learner_level_1_5",
            ),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="level",
            field=models.PositiveSmallIntegerField(
                default=2,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="exercise",
            constraint=models.CheckConstraint(
                condition=models.Q(("level__gte", 1), ("level__lte", 5)),
                name="poligon_exercise_level_1_5",
            ),
        ),
        migrations.AlterField(
            model_name="vocabularyitem",
            name="level",
            field=models.PositiveSmallIntegerField(
                default=2,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="vocabularyitem",
            constraint=models.CheckConstraint(
                condition=models.Q(("level__gte", 1), ("level__lte", 5)),
                name="poligon_vocab_level_1_5",
            ),
        ),
    ]
