import django.core.validators
from django.db import migrations, models

import tonguetwister.models


class Migration(migrations.Migration):

    dependencies = [
        ("tonguetwister", "0002_audit_phase2_constraints"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                help_text="Allowed: jpg, jpeg, png, gif. Max 2 MB.",
                null=True,
                upload_to="avatars/%Y/%m/%d/",
                validators=[
                    django.core.validators.FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"]),
                    tonguetwister.models.validate_avatar_size,
                ],
            ),
        ),
    ]
