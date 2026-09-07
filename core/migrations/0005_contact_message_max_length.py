from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_contact_options_alter_contact_submitted_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="message",
            field=models.TextField(max_length=5000),
        ),
    ]
