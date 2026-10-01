from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("poligon", "0011_placement_bank"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercise",
            name="delivery",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="exercise_type",
            field=models.CharField(
                choices=[
                    ("mcq", "Multiple choice"),
                    ("listening", "Listening"),
                    ("speaking", "Speaking"),
                    ("writing", "Writing"),
                    ("true_false", "True or false"),
                ],
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="ProductEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=40)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "learner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_events",
                        to="poligon.learnerstate",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product event",
                "verbose_name_plural": "Product events",
                "ordering": ["-created_at"],
            },
        ),
    ]
