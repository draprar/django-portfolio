import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_wybierz_renders_crossroads(client):
    response = client.get(reverse("rozdroze:wybierz"))

    assert response.status_code == 200
    content = response.content.decode()
    assert ">click tudzież swipe</h1>" in content
    assert "se klikaj" not in content
    assert "Se klikaj" not in content
    assert ">wyraj</h2>" in content
    assert content.count('class="panel-import"') == 5
    assert 'panel-code"' in content
    code_panel, carousel = content.split('class="carousel"', 1)
    assert "panel-import" not in code_panel
    assert ">bazgrollin'</h2>" in content
    assert ">lingwołamki</h2>" in content
    assert "Se wybierz" not in content
    assert "/gallery/" in content
    assert "panel-bazgr" in content
    assert 'data-panel="bazgr" data-slot="hidden"' in content
    assert "bazgrollin-bg.png" in content
    assert "/wyraj/" in content
    assert 'data-panel="wyraj" data-slot="active"' in content
    assert 'data-panel="lingwo" data-slot="next"' in content
    assert 'data-panel="wiciedzy" data-slot="prev"' in content
    assert "/tonguetwister/" in content
    assert "/codillin/" in content
    assert "/wiciedze/" in content
    assert "/rugby/" in content
    assert "panel-iaio" in content
    assert 'data-panel="iaio" data-slot="hidden"' in content
    assert ">iaio</h2>" in content
    assert "iaio-bg.jpg" in content
    assert "codillin'" in content
    assert ">wiciędze</h2>" in content
    assert "code-terminal" in content
    assert "wiciedzy-bg.jpg" in content
    assert 'panel-code' in content
    assert 'panel-wiciedzy' in content
    assert 'stage-stack' in content
    assert 'class="carousel"' in content
    assert "carousel-stage" in content
    assert content.count("panel-turn") == 5
    assert "Wejdź" not in content
    assert 'class="cta-arrow"' not in content
    assert 'panel-cta' not in content
    assert "Komputerek" not in content
    assert 'id="contact-form"' not in content
    assert "rozdroze/js/wybierz.js" in content
    assert "{% static" not in content
    assert "no-cache" in response["Cache-Control"]


@pytest.mark.django_db
def test_wybierz_is_polish_only(client):
    """The hub ships without the language switcher, so nothing can flip it to EN."""
    response = client.get(reverse("rozdroze:wybierz"))
    content = response.content.decode()

    assert 'class="lang-btn"' not in content
    assert "lang-switcher" not in content
    assert "core/js/lang.js" not in content
    assert "data-en=" not in content
