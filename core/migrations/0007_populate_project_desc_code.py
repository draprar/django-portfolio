# Data migration: populate desc_code_* with short kodzillin'-style blurbs
# Matched by title_en from admin; CV descriptions (desc_*) stay unchanged.

from django.db import migrations

PROJECT_CODE = {
    "Django Document Diff": {
        "desc_code_pl": (
            "Porównuje DOCX, XLSX i TXT z pomocą spaCy — akapity, tabele, obrazy. "
            "Raport interaktywny z dark mode i eksportem JSON."
        ),
        "desc_code_en": (
            "Compares DOCX, XLSX, TXT with spaCy — paragraphs, tables, images. "
            "Interactive report with dark mode and JSON export."
        ),
    },
    "ML Training Intensity Prediction": {
        "desc_code_pl": (
            "Pipeline ML ze scikit i FastAPI — Garmin + Random Forest (R²≈0.93). "
            "Podasz tętno, dystans, typ → dostajesz kalorie/min."
        ),
        "desc_code_en": (
            "ML pipeline with scikit and FastAPI — Garmin + Random Forest (R²≈0.93). "
            "Input heart rate, distance, type → get calories/min."
        ),
    },
    "Pandas Tabular Convert": {
        "desc_code_pl": (
            "CLI do konwersji CSV, Excel, JSON, Pickle i Parquet. "
            "Podgląd, czyszczenie, eksport — wszystko przez DataFrame."
        ),
        "desc_code_en": (
            "CLI for converting CSV, Excel, JSON, Pickle, Parquet. "
            "Preview, clean, export — all via DataFrame."
        ),
    },
    "Django Art Gallery": {
        "desc_code_pl": (
            "Portfolio do obrazów z podziałem na kategorie i integracją z Instagramem. "
            "Responsywny interfejs, żywe demo."
        ),
        "desc_code_en": (
            "Image portfolio with categories and Instagram integration. "
            "Responsive UI, live demo."
        ),
    },
    "Python - Text Similarity Analysis": {
        "desc_code_pl": (
            "TF-IDF + cosine similarity — porównuje dokument główny z resztą. "
            "Szybko wychwyci podobieństwa w dużym zbiorze."
        ),
        "desc_code_en": (
            "TF-IDF + cosine similarity — compares main doc with others. "
            "Quick similarity detection across large sets."
        ),
    },
    "Django Tongue Twister": {
        "desc_code_pl": (
            "Ćwiczenia wymowy i łamańce językowe z nagrywaniem głosu, kamerą i śledzeniem serii. "
            "Django + interactive UI."
        ),
        "desc_code_en": (
            "Pronunciation drills and tongue twisters with voice recording, camera, and streak tracking. "
            "Django + interactive UI."
        ),
    },
    "Data Analysis & ML Projects": {
        "desc_code_pl": (
            "Zbiór projektów ML i analiz w Power BI, Excel, Python i R — różne datasety, różne modele."
        ),
        "desc_code_en": (
            "Collection of ML projects and analyses in Power BI, Excel, Python, R — various datasets and models."
        ),
    },
    "Windows Registry Tweaks": {
        "desc_code_pl": (
            "Poprawki .reg dla Win10 — menu kontekstowe, telemetria, animacje. "
            "Każda zmiana ma plik przywracający oryginał."
        ),
        "desc_code_en": (
            "Registry .reg tweaks for Win10 — context menu, telemetry, animations. "
            "Each change includes restore file."
        ),
    },
    "Pygame Alien Shooter": {
        "desc_code_pl": (
            "Retro arcade — fale najeźdźców, strzały, uniki. "
            "Wybierz postać, trudność rośnie z każdą rundą."
        ),
        "desc_code_en": (
            "Retro arcade — waves of invaders, shoot, dodge. "
            "Pick character, difficulty scales each round."
        ),
    },
    "Tkinter Utility Tools": {
        "desc_code_pl": (
            "Zestaw narzędzi: generator kluczy, wyszukiwarka duplikatów, detektor ścieżek >260 znaków. "
            "GUI w Tkinter."
        ),
        "desc_code_en": (
            "Utility set: key generator, duplicate finder, path detector >260 chars. "
            "Tkinter GUI."
        ),
    },
    "Tkinter Tesseract OCR": {
        "desc_code_pl": (
            "Wczytaj obraz, zaznacz myszką obszar, wyciągnij tekst. "
            "Tesseract + Tkinter, lekkie i szybkie."
        ),
        "desc_code_en": (
            "Load image, select area with mouse, extract text. "
            "Tesseract + Tkinter, lightweight and fast."
        ),
    },
    "Tkinter Document Viewer": {
        "desc_code_pl": (
            "Przeglądarka PDF, EPUB i MOBI z powiększaniem, wyszukiwaniem i trybem pełnoekranowym. "
            "Python + Tkinter."
        ),
        "desc_code_en": (
            "PDF, EPUB, MOBI viewer with zoom, search, fullscreen mode. "
            "Python + Tkinter."
        ),
    },
    "Flask PDF Tools": {
        "desc_code_pl": (
            "Łączenie i podział PDF-ów przez przeglądarkę — z CAPTCHA i kontrolą bezpieczeństwa. "
            "Flask backend."
        ),
        "desc_code_en": (
            "Merge and split PDFs via browser — with CAPTCHA and security controls. "
            "Flask backend."
        ),
    },
    "OpenCV Sketch Effects": {
        "desc_code_pl": (
            "Zdjęcie → szkic/kontur/szablon pod tatuaż. "
            "Efekty ołówkowe, binarne, szarości. Tkinter + OpenCV."
        ),
        "desc_code_en": (
            "Photo → sketch/outline/tattoo template. "
            "Pencil, binary, grayscale effects. Tkinter + OpenCV."
        ),
    },
    "Folium City Visits": {
        "desc_code_pl": (
            "Mapa Polski z markerami miast — dane z SQLite, wizualizacja w Folium. "
            "Eksport do HTML."
        ),
        "desc_code_en": (
            "Poland map with city markers — SQLite data, Folium visualization. "
            "Export to HTML."
        ),
    },
    "Tkinter File Organizer": {
        "desc_code_pl": (
            "Porządkuje pliki w foldery (obrazy, dokumenty, wideo, audio) z deduplikacją SHA-256. "
            "Tryb podglądu i datowane katalogi."
        ),
        "desc_code_en": (
            "Organizes files into folders (images, docs, video, audio) with SHA-256 deduplication. "
            "Preview mode and dated directories."
        ),
    },
    "Django Rugby Gizycko": {
        "desc_code_pl": (
            "Archiwum klubu AFC Rugby przerobione na Django — backend, baza danych, responsywny frontend."
        ),
        "desc_code_en": (
            "AFC Rugby club archive rebuilt in Django — backend, database, responsive frontend."
        ),
    },
}


TITLE_ALIASES = {
    "Python - Analiza podobieństwa tekstu": "Python - Text Similarity Analysis",
    "Projekty analizy danych i ML": "Data Analysis & ML Projects",
    "Django Rugby Giżycko": "Django Rugby Gizycko",
}


def populate_desc_code(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    for title_en, blurbs in PROJECT_CODE.items():
        titles = [title_en]
        for alias, canonical in TITLE_ALIASES.items():
            if canonical == title_en:
                titles.append(alias)
        Project.objects.filter(title_en__in=titles).update(
            desc_code_en=blurbs["desc_code_en"],
            desc_code_pl=blurbs["desc_code_pl"],
        )


def clear_desc_code(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    titles = list(PROJECT_CODE) + list(TITLE_ALIASES)
    Project.objects.filter(title_en__in=titles).update(desc_code_en="", desc_code_pl="")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_project_desc_code"),
    ]

    operations = [
        migrations.RunPython(populate_desc_code, clear_desc_code),
    ]
