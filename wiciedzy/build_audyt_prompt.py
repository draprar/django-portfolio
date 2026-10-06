"""One-off: build prompt-audyt-chatgpt.md from export + katalog + quiz."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

HEADER = """# Prompt audytu wiciędze (ChatGPT) — stan po drugim przejściu korekcyjnym

Wklej **cały ten plik** do ChatGPT (lub załącz jako plik). Model ma przeprowadzić audyt jak na początku projektu, ale na **aktualnym** materiale.

---

## Kontekst techniczny (nie oceniaj kodu Django, tylko treść i spójność)

- Aplikacja: **wiciędze** (`/wiciedze/`), katalog **46** aktywnych stylów w bazie (36 core + 10 golden). Import: `CORE` + `GOLDEN` z `styles.py`, pola About/History/Practice **nadpisuje** `PROSE` z `prose.py`.
- **Lustro redakcyjne:** `katalog-opisy.md` ma **46** opisów stylów + sekcje „Do sprawdzenia” i meta; katalog w `styles.py` powinien być zgodny z bazą (sprawdź `validate_wiciedzy_content`).
- **Fakty** i **relacje** między kartami są w `styles.py` (import: `FACTS`, `RELATIONS`). Po imporcie w bazie powinno być **22** relacji, m.in. catch → zapasy (subset).
- **5 kart** ma flagę `sources_disagree` (baner: źródła niejasne): taekwondo, wushu, hapkido, hema, kalaripayattu.
- Parasole (umbrella): karate, wushu, arnis, jujutsu, silat, taijiquan.
- Quiz dopasowania: preferencje + profile 22 osi (nie pokazywane użytkowniku jako liczby). Osobny plik quizu poniżej.
- Język: pary **EN nad PL** w katalogu MD; na stronie domyślnie PL z `data-en` / `data-pl`. Nie proponuj profilu 1–5 ani „niski/średni/wysoki” w opisach kart.

---

## Zadanie — przeprowadź pełny audyt (wszystkie aspekty)

### I. Katalog stylów (priorytet: sekcja B = MD; sekcja A = co faktycznie widzi użytkownik)

1. **Wiarygodność merytoryczna.** Przy każdej uwadze: karta (nazwa PL), zdanie lub teza, co jest słabe, **źródło** (federacja, UNESCO, regulamin, encyklopedia). Oznacz też zdania poprawne (bez cytowania całych akapitów). Sprawdź m.in. ostatnie poprawki: PERSILAT 2026 (Tanding/Jurus), WT/ITF, zapasy olimpijskie (kobiety = freestyle), lethwei (owijki vs rękawice), bökh (lokalne zasady końca), brak „seni” jako kategorii nadrzędnej.
2. **Granice kart i parasole.** Co słusznie w jednej karcie, co zdublowane, co jedna nazwa a wiele regulaminów. Odnieś się do 40 vs 46: czy 6 kart „tylko MD” powinno wejść do aplikacji, czy zostać w MD.
3. **Braki.** Propozycje sportów/sztuk których nie ma — odmiana istniejącej karty vs nowa karta. Bez inflacji nazw szkół.
4. **PL wobec EN.** Gdzie polski gubi, zaostrza lub przekręca angielski. Nie wygładzaj stylu jeśli sens się zgadza.
5. **Głos i forma.** Krótkie zdania sprawdzalne; bez żartów w opisach kart; bez ocen „jak bardzo kontaktowe”.
6. **Źródła i „Do sprawdzenia”.** Czy drugie źródło to discovery; czy fakty mają sensowne URL; czy sekcja „Do sprawdzenia” w B jest aktualna (arnis + RA 9850, lethwei Unified Ruleset SOURCE GAP, itd.).
7. **Spójność warstw.** Różnice między **A (eksport UI)** a **B (katalog-opisy.md)** dla tych samych slugów — czy PROSE/import zgadza się z lustrem redakcyjnym.
8. **Fakty i relacje (sekcja D).** Czy 6 faktów i 4 relacje są trafne; czego brakuje (np. catch przy zapasach); czy `is_legend` jest używane uczciwie.

### II. Quizopasowanie (sekcja C)

Wykonaj **dokładnie** polecenie z nagłówka pliku quizu (4 punkty: mechanizm, jakość pytań i zdań wyniku, PL/EN, rozszerzenia tylko gdy zmieniają listę). Nie przepisuj quizu. Nie dodawaj testu osobowości ani skali skuteczności.

### III. Teksty UI poza kartami (sekcja A — home, spis, test, dopasowanie, porównaj, 404)

9. **UI i obietnice.** Czy home/quiz/katalog nie obiecują więcej niż mechanizm daje; ton PL (np. „se poklikaj”, tagline); dostępność sensu bez kontekstu kodu.
10. **Porównanie i dopasowanie.** Czy copy przy legendzie, „do poczytania”, brak psychometrii — spójne i uczciwe.

### IV. Humor / IPIP (jeśli występują w eksportie A)

11. Jeśli eksport zawiera pytania IPIP lub humor — krótko: czy nie mylą się z quizem dopasowania i czy PL/EN jest spójne. Jeśli brak w eksportcie — pomiń.

---

## Format odpowiedzi ChatGPT

Pogrupuj:

1. **Błędy merytoryczne** (karta → problem → źródło lub SOURCE GAP)
2. **Sporne granice kart / 40 vs 46**
3. **Rozjazdy PL/EN**
4. **Niespójność A (UI) vs B (MD) vs D (fakty/relacje)**
5. **Quiz — błędy mechanizmu / słabe pytania / propozycje**
6. **UI i obietnice**
7. **Propozycje braków** (odmiana vs nowa karta)
8. **Co jest w porządku** (krótko)
9. **Nie dało się sprawdzić** (lista)

Nie przepisuj całego katalogu. Nie dodawaj profilu liczbowego 1–5 do opisów.

---

# DANE DO AUDYTU

"""

def main() -> None:
    styles = (ROOT / "data" / "styles.py").read_text(encoding="utf-8")
    relations_facts = "RELATIONS:" + styles.split("RELATIONS:", 1)[1].split("UMBRELLAS", 1)[0]

    chunks = [
        HEADER,
        "## Sekcja D — fakty i relacje (import)\n\n```python\n",
        relations_facts.strip(),
        "\n```\n\n",
        "## Sekcja A — eksport tekstów widocznych pod /wiciedze/ (UI + 46 kart po PROSE)\n\n",
        (ROOT / "teksty-audyt-eksport.md").read_text(encoding="utf-8"),
        "\n\n## Sekcja B — katalog-opisy.md (lustro redakcyjne, 46 stylów)\n\n",
        (ROOT / "katalog-opisy.md").read_text(encoding="utf-8"),
        "\n\n## Sekcja C — quizopasowanie.md\n\n",
        (ROOT / "quizopasowanie.md").read_text(encoding="utf-8"),
    ]
    out = ROOT / "prompt-audyt-chatgpt.md"
    out.write_text("".join(chunks), encoding="utf-8-sig")
    lines = out.read_text(encoding="utf-8-sig").count("\n") + 1
    print(f"Wrote {out} ({lines} lines)")


if __name__ == "__main__":
    main()
