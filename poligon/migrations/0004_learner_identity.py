import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def attach_existing_progress(apps, schema_editor):
    """Move session-keyed rows onto a LearnerState row, so progress outlives the session."""
    LearnerState = apps.get_model("poligon", "LearnerState")
    states = {}
    for state in LearnerState.objects.all():
        state.guest_token = uuid.uuid4()
        state.save(update_fields=["guest_token"])
        states[state.session_key] = state

    for name in ("Submission", "Review", "StudyEvent"):
        model = apps.get_model("poligon", name)
        for row in model.objects.all().iterator():
            state = states.get(row.session_key)
            if state is None:
                state = LearnerState.objects.create(session_key=row.session_key, guest_token=uuid.uuid4())
                states[row.session_key] = state
            row.learner = state
            row.save(update_fields=["learner"])


def detach_progress(apps, schema_editor):
    """Put the session key back on the rows that still have a state to read it from."""
    for name in ("Submission", "Review", "StudyEvent"):
        model = apps.get_model("poligon", name)
        for row in model.objects.select_related("learner").iterator():
            row.session_key = row.learner.session_key
            row.save(update_fields=["session_key"])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("poligon", "0003_practice_level_and_exercise_provenance"),
    ]

    operations = [
        migrations.AddField(
            model_name="learnerstate",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="poligon_state",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="learnerstate",
            name="guest_token",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name="submission",
            name="learner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to="poligon.learnerstate",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="learner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="poligon.learnerstate",
            ),
        ),
        migrations.AddField(
            model_name="studyevent",
            name="learner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="poligon.learnerstate",
            ),
        ),
        migrations.RunPython(attach_existing_progress, detach_progress),
        migrations.RemoveConstraint(
            model_name="review",
            name="poligon_review_session_item_uniq",
        ),
        migrations.AlterField(
            model_name="learnerstate",
            name="guest_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="submission",
            name="learner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to="poligon.learnerstate",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="learner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="poligon.learnerstate",
            ),
        ),
        migrations.AlterField(
            model_name="studyevent",
            name="learner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="poligon.learnerstate",
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(fields=("learner", "item"), name="poligon_review_learner_item_uniq"),
        ),
        migrations.RemoveField(model_name="submission", name="session_key"),
        migrations.RemoveField(model_name="review", name="session_key"),
        migrations.RemoveField(model_name="studyevent", name="session_key"),
        migrations.RemoveField(model_name="learnerstate", name="session_key"),
    ]
