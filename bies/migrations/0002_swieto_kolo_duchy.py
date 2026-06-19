from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="swieto",
            name="kolo_kat",
            field=models.SmallIntegerField(
                default=0,
                verbose_name="Kąt na Kole Roku (stopnie)",
                help_text=(
                    "Pozycja święta na okręgu. 0° = szczyt (przesilenie zimowe), "
                    "dalej zgodnie z ruchem wskazówek."
                ),
            ),
        ),
        migrations.AddField(
            model_name="swieto",
            name="kolo_kolor",
            field=models.CharField(
                default="#c4922a",
                max_length=20,
                verbose_name="Kolor węzła na kole",
                help_text="Hex, np. '#a3c47a' dla wiosennych, '#c4922a' dla złotych.",
            ),
        ),
        migrations.AddField(
            model_name="swieto",
            name="duchy_pl",
            field=models.CharField(
                blank=True, max_length=300,
                verbose_name="Duchy / bóstwa (PL)",
                help_text="Np. 'Jaryło, Marzanna'. Oddzielone przecinkami.",
            ),
        ),
        migrations.AddField(
            model_name="swieto",
            name="duchy_en",
            field=models.CharField(
                blank=True, max_length=300,
                verbose_name="Duchy / bóstwa (EN)",
                help_text="Np. 'Jaryło, Marzanna'. Oddzielone przecinkami.",
            ),
        ),
    ]
