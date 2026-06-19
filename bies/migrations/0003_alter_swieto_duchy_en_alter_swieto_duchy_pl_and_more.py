from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bies", "0002_swieto_kolo_duchy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="swieto",
            name="duchy_en",
            field=models.CharField(
                blank=True,
                help_text="Np. 'Jaryło, Marzanna, Spring'. Oddzielone przecinkami.",
                max_length=300,
                verbose_name="Duchy / bóstwa (EN)",
            ),
        ),
        migrations.AlterField(
            model_name="swieto",
            name="duchy_pl",
            field=models.CharField(
                blank=True,
                help_text="Np. 'Jaryło, Marzanna, Wiosna'. Oddzielone przecinkami.",
                max_length=300,
                verbose_name="Duchy / bóstwa (PL)",
            ),
        ),
        migrations.AlterField(
            model_name="swieto",
            name="kolejnosc",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="Kolejność na liście i pozycja na Kole Roku (1–12, rosnąco).",
            ),
        ),
        migrations.AlterField(
            model_name="swieto",
            name="kolo_kat",
            field=models.SmallIntegerField(
                default=0,
                help_text=(
                    "Pozycja święta na okręgu. 0° = szczyt (przesilenie zimowe), "
                    "dalej zgodnie z ruchem wskazówek. Np. równonoc wiosenna ≈ 90°."
                ),
                verbose_name="Kąt na Kole Roku (stopnie)",
            ),
        ),
        migrations.AlterField(
            model_name="zrodlobibliograficzne",
            name="autor",
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name="Autor",
            ),
        ),
        migrations.AlterField(
            model_name="zrodlobibliograficzne",
            name="kolejnosc",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="zrodlobibliograficzne",
            name="tytul",
            field=models.CharField(
                max_length=400,
                verbose_name="Tytuł dzieła",
            ),
        ),
        migrations.AlterField(
            model_name="zrodlobibliograficzne",
            name="url",
            field=models.URLField(
                blank=True,
                verbose_name="Link (opcjonalnie)",
            ),
        ),
        migrations.AlterField(
            model_name="zrodlobibliograficzne",
            name="url_etykieta",
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name="Etykieta linka",
            ),
        ),
        migrations.AlterField(
            model_name="zrodlobibliograficzne",
            name="wydawca_rok",
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name="Wydawca / rok",
            ),
        ),
    ]
