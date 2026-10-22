import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from rugby.models import Post


@pytest.mark.django_db
class TestPostListView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse("post_list")

    def test_post_list_ok(self):
        assert self.client.get(self.url).status_code == 200

    def test_three_accounts_in_context(self):
        response = self.client.get(self.url)
        assert len(response.context["accounts"]) == 3

    def test_pesel_post_not_in_html(self):
        user = User.objects.create(username="peseluser")
        Post.objects.create(
            author=user,
            title_pl="Ukryty",
            text_pl="Proszę o numer PESEL i adres.",
            published_date=timezone.now(),
        )
        html = self.client.get(self.url).content.decode()
        assert "PESEL" not in html

    def test_farewell_once(self):
        html = self.client.get(self.url).content.decode()
        assert html.count('id="afc-farewell"') == 1

    def test_no_recruitment_card_copy(self):
        html = self.client.get(self.url).content.decode()
        assert "Nabór do drużyny trwał" not in html
        assert "160–185" not in html
        assert "pierwsza drużyna na mazurach" not in html.lower()
        assert "14 osób" not in html

    def test_scoring_values(self):
        html = self.client.get(self.url).content.decode()
        assert html.count('class="scoring-btn"') == 5
        assert 'data-scoring="try"' in html
        assert 'data-scoring="conversion"' in html
        assert 'data-scoring="penalty_try"' in html
        assert 'data-scoring="penalty_goal"' in html
        assert 'data-scoring="drop_goal"' in html
        assert 'aria-describedby="scoring-desc-try"' in html
        assert "Przyłożenie piłki do ziemi w polu punktowym przeciwnika." in html
        assert "Celny kop na bramkę z rzutu karnego." in html
        assert "Grounding the ball on the ground in the opponents’ in-goal area." in html
        assert "A successful kick at goal from a penalty." in html
        assert "po odbiciu piłki od ziemi" in html

    def test_six_trace_cards(self):
        html = self.client.get(self.url).content.decode()
        assert html.count("trace-card") >= 6

    def test_map_section_present(self):
        html = self.client.get(self.url).content.decode()
        assert 'id="rugby-map"' in html
        assert "map-europe.svg" in html
        assert "Kluby rugby w Polsce — ostatnia dekada" in html

    def test_no_map_club_list(self):
        html = self.client.get(self.url).content.decode()
        assert "Kluby z mapy" not in html
        assert "map-club-section" not in html

    def test_no_map_era_layer(self):
        html = self.client.get(self.url).content.decode()
        assert 'data-map-era="archive"' not in html
        assert ">2008–2010<" not in html

    def test_nav_minimal_lang_only(self):
        html = self.client.get(self.url).content.decode()
        assert 'class="rugby-lang-toolbar' in html
        assert 'data-lang="pl"' in html
        assert 'data-lang="en"' in html
        assert 'rugby-brand-text' not in html
        assert 'navbar-nav' not in html
        assert 'data-pl="Archiwum"' not in html
        assert 'data-pl="Pigułka"' not in html

    def test_pitch_controls(self):
        html = self.client.get(self.url).content.decode()
        assert 'id="phase-prev"' in html
        assert 'id="phase-next"' in html
        assert "Poza tą akcją" not in html

    def test_accounts_metadata(self):
        html = self.client.get(self.url).content.decode()
        assert "Mecz: 5 lipca 2008 · Miejsce: Gągławki" in html
        assert "Wpis opublikowany: 10 listopada 2008 · Miejsce: Giżycko" in html
        assert "Trening z zawodnikiem Skry Warszawa" in html

    def test_footer_photo_only(self):
        html = self.client.get(self.url).content.decode()
        assert "Kontakt przez portfolio" not in html
        assert "Jeśli rozpoznajesz siebie na zdjęciu" not in html
        assert "footer-photo-wrap" in html

    def test_gold_link_rules_present(self):
        css = open("rugby/static/rugby/css/style.css", encoding="utf-8").read()
        assert ".page-section a:visited" in css
        assert ".page-section a:focus-visible" in css
        assert ".page-section a:active" in css

    def test_map_data_coverage_note(self):
        html = self.client.get(self.url).content.decode()
        assert "Nie jest to pełny wykaz klubów" in html
        assert "AFC Rugby Giżycko (2008–2010)" in html
        assert "not a complete list of clubs" in html
        assert "repozytorium" not in html.lower()

    def test_map_legend_and_hints(self):
        html = self.client.get(self.url).content.decode()
        assert "Klub ujęty w obu zestawieniach" in html
        assert "Polska Liga Rugby 7 (PLR7)" in html
        assert "Ctrl/Cmd + kółko zmienia skalę mapy" in html
        assert "Jak korzystać z mapy?" in html
        assert "dotknij skupiska" in html
        assert "Niektóre kluby (np. AFC)" not in html

    def test_warsaw_combined_marker_label(self):
        html = self.client.get(self.url).content.decode()
        assert "wspólny punkt na mapie" in html
        assert "combined map marker" in html

    def test_doctype_and_main(self):
        html = self.client.get(self.url).content.decode()
        assert html.lstrip().startswith("<!DOCTYPE html>")
        assert '<main id="main-content">' in html
        assert "sr-only" not in html

    def test_skip_link(self):
        html = self.client.get(self.url).content.decode()
        assert 'class="skip-link' in html
        assert 'href="#main-content"' in html

    def test_pitch_posts_on_try_line(self):
        html = self.client.get(self.url).content.decode()
        assert 'x1="124"' in html
        assert 'x1="876"' in html
        assert 'x1="62"' not in html
        assert "#phase-scrum" not in html
        assert "#phase-maul" not in html

    def test_map_projection_script(self):
        html = self.client.get(self.url).content.decode()
        assert 'id="rugby-map-projection"' in html

    def test_farewell_blockquote(self):
        html = self.client.get(self.url).content.decode()
        assert 'class="farewell-quote' in html

    def test_archive_section_no_lead_paragraph(self):
        html = self.client.get(self.url).content.decode()
        assert "Wybrane relacje" in html
        assert "Z zachowanych wpisów wybraliśmy trzy" not in html

    def test_no_background_attachment_fixed(self):
        css = open("rugby/static/rugby/css/style.css", encoding="utf-8").read()
        assert "background-attachment: fixed" not in css

    def test_hand_pass_copy(self):
        js = open("rugby/static/rugby/js/pitch.js", encoding="utf-8").read()
        assert "Pozycja partnera nie decyduje" in js
        assert "celny kop na bramkę z rzutu karnego" in js
        assert "bounces off the ground" in js
        assert "korzystniejszej pozycji" in js

    def test_basics_editorial_copy(self):
        html = self.client.get(self.url).content.decode()
        assert 'data-pl="Czym jest rugby"' in html
        assert "lokalne inicjatywy związane z rugby 7" in html
        assert "local rugby sevens initiatives also existed" in html
        assert "popularyzowały" not in html

    def test_info_editorial_copy(self):
        html = self.client.get(self.url).content.decode()
        assert "AFC Rugby Giżycko w skrócie" in html
        assert 'data-pl="Treningi"' in html
        assert "Współpraca z WMPD PUDiZ Olsztyn" in html
        assert "Działalność w latach 2008–2010" in html
        assert "W zachowanych materiałach pojawiają się także nazwa MTS Rugby Giżycko" in html
        assert "Serce drużyny" not in html
        assert "niezapomniane" not in html

    def test_about_editorial_copy(self):
        html = self.client.get(self.url).content.decode()
        assert "W zachowanych materiałach nie ma wyniku meczu" in html
        assert "energia tamtych lat" not in html
        assert "fajny sposób" not in html

    def test_media_poster_alts(self):
        html = self.client.get(self.url).content.decode()
        assert "Plakat czarno-biały: napis RUGBY, data i godzina spotkania 6.06.2008 w GCK" in html
        assert "Plakat czarno-biały z nagłówkiem Ogłaszamy nabór" in html
        assert "Wycinek prasowy dotyczący środowiska rugby w Olsztynie." in html

    def test_map_card_close_icon(self):
        html = self.client.get(self.url).content.decode()
        assert "map-card-close-icon" in html
        assert 'class="map-card-close" aria-label="Zamknij informacje o klubie"' in html

    def test_afc_farewell_anchor(self):
        html = self.client.get(self.url).content.decode()
        assert 'id="afc-farewell"' in html
        assert 'data-internal="#afc-farewell"' in html or 'internal_href' not in html
        assert "#afc-farewell" in html

    def test_english_data_attributes(self):
        html = self.client.get(self.url).content.decode()
        assert 'data-en="Rugby in a nutshell"' in html
        assert 'data-en="Our first friendly in Gągławki"' in html
        assert 'data-en="Training with a Skra Warszawa player"' in html
