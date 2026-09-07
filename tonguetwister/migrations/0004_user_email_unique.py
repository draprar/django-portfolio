from django.db import migrations, models
from django.db.models import Count, Q
from django.db.models.functions import Lower


EMAIL_UNIQUE_CONSTRAINT = models.UniqueConstraint(
    Lower("email"),
    name="uniq_auth_user_email_lower",
    condition=~Q(email=""),
)


def forwards_add_email_constraint(apps, schema_editor):
    user_model = apps.get_model("auth", "User")
    duplicates = list(
        user_model.objects.exclude(email="")
        .annotate(email_lower=Lower("email"))
        .values("email_lower")
        .annotate(total=Count("id"))
        .filter(total__gt=1)
        .values_list("email_lower", flat=True)
    )
    if duplicates:
        listed = ", ".join(sorted(duplicates))
        raise RuntimeError(f"Cannot add unique email constraint; duplicate emails exist: {listed}")
    schema_editor.add_constraint(user_model, EMAIL_UNIQUE_CONSTRAINT)


def backwards_remove_email_constraint(apps, schema_editor):
    user_model = apps.get_model("auth", "User")
    schema_editor.remove_constraint(user_model, EMAIL_UNIQUE_CONSTRAINT)


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("tonguetwister", "0003_avatar_validators"),
    ]

    operations = [
        migrations.RunPython(forwards_add_email_constraint, backwards_remove_email_constraint),
    ]
