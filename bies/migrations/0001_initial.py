from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Swieto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=80, unique=True, help_text="Część URL-a, np. 'gaik', 'jare-gody'. Wypełnia się automatycznie.")),
                ("kolejnosc", models.PositiveSmallIntegerField(default=0, help_text="Kolejność wyświetlania na liście (rosnąco).")),
                ("tytul_pl", models.CharField(max_length=120, verbose_name="Tytuł (PL)")),
                ("tytul_en", models.CharField(max_length=120, verbose_name="Tytuł (EN)")),
                ("podtytul_pl", models.CharField(blank=True, max_length=220, verbose_name="Podtytuł (PL)")),
                ("podtytul_en", models.CharField(blank=True, max_length=220, verbose_name="Podtytuł (EN)")),
                ("meta_opis_pl", models.CharField(blank=True, max_length=300, verbose_name="Meta opis (PL)")),
                ("meta_opis_en", models.CharField(blank=True, max_length=300, verbose_name="Meta opis (EN)")),
                ("obraz", models.ImageField(blank=True, help_text="Zalecany format: PNG lub JPG, min. 1200×800 px.", null=True, upload_to="bies/swieta/", verbose_name="Obrazek")),
                ("o_swiecie_pl", models.TextField(blank=True, verbose_name="O święcie (PL)")),
                ("o_swiecie_en", models.TextField(blank=True, verbose_name="O święcie (EN)")),
                ("obrzedy_pl", models.TextField(blank=True, verbose_name="Obrzędy (PL)")),
                ("obrzedy_en", models.TextField(blank=True, verbose_name="Obrzędy (EN)")),
                ("symbolika_pl", models.TextField(blank=True, verbose_name="Symbolika (PL)")),
                ("symbolika_en", models.TextField(blank=True, verbose_name="Symbolika (EN)")),
                ("utworzone", models.DateTimeField(auto_now_add=True)),
                ("zaktualizowane", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Święto",
                "verbose_name_plural": "Święta",
                "ordering": ["kolejnosc", "tytul_pl"],
            },
        ),
        migrations.CreateModel(
            name="ZrodloBibliograficzne",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("swieto", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="zrodla", to="bies.swieto", verbose_name="Święto")),
                ("kolejnosc", models.PositiveSmallIntegerField(default=0, help_text="Kolejność na liście źródeł.")),
                ("autor", models.CharField(blank=True, help_text="Np. 'Oskar Kolberg'", max_length=200, verbose_name="Autor")),
                ("tytul", models.CharField(help_text="Np. 'Pieśni ludu obrzędowe: kogutek, gaik, okrężne'", max_length=400, verbose_name="Tytuł dzieła")),
                ("wydawca_rok", models.CharField(blank=True, help_text="Np. 'WAM, 2003' lub '(1848)'", max_length=200, verbose_name="Wydawca / rok")),
                ("url", models.URLField(blank=True, help_text="Np. link do Wikipedii lub skanów.", verbose_name="Link (opcjonalnie)")),
                ("url_etykieta", models.CharField(blank=True, help_text="Np. 'Wikipedia — Gaik'. Wypełnij tylko jeśli podano URL.", max_length=200, verbose_name="Etykieta linka")),
            ],
            options={
                "verbose_name": "Źródło bibliograficzne",
                "verbose_name_plural": "Źródła bibliograficzne",
                "ordering": ["kolejnosc"],
            },
        ),
    ]
