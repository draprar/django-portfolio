"""
Apply PZR season tables to rugby/data/club-history.json.
Run: python -m rugby.data.sync_club_seasons
"""
from __future__ import annotations

import json
import re
import unicodedata
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "club-history.json"

PLR7_POZNAN_2022 = "https://polskie.rugby/artykul/8892/plr7-v-turniej-w-poznaniu"
WINDOW_CUTOFF = "2026-10-21"

PARSER_EVIDENCE: dict[str, str] = {
    "tabela": "final_table",
    "klasyfikacja": "final_table",
    "tabela_w_toku": "snapshot",
}

SEASON_PAGES: list[dict] = [
    {
        "league": "ekstraliga",
        "season": "2022/23",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/1/ekstraliga-rugby-20222023",
        "parser": "tabela",
    },
    {
        "league": "ekstraliga",
        "season": "2023/24",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/9/ekstraliga-rugby-20232024",
        "parser": "tabela",
    },
    {
        "league": "ekstraliga",
        "season": "2024/25",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/23/ekstraliga-rugby-20242025",
        "parser": "tabela",
    },
    {
        "league": "ekstraliga",
        "season": "2025/26",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/32/ekstraliga-rugby-20252026",
        "parser": "tabela",
    },
    {
        "league": "ekstraliga",
        "season": "2026/27",
        "status": "w_toku",
        "url": "https://polskie.rugby/sezon/39/ekstraliga-rugby-20262027",
        "parser": "tabela_w_toku",
        "evidence_type": "snapshot",
    },
    {
        "league": "sevens",
        "season": "2022/23",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/5/polska-liga-rugby-7-20222023",
        "parser": "klasyfikacja",
        "supplemental_urls": [PLR7_POZNAN_2022],
    },
    {
        "league": "sevens",
        "season": "2023/24",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/12/polska-liga-rugby-7-20232024",
        "parser": "tabela",
    },
    {
        "league": "sevens",
        "season": "2024/25",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/sezon/27/polska-liga-rugby-7-20242025",
        "parser": "tabela",
    },
]

LEGACY_SEASON_SPECS: list[dict] = [
    {
        "league": "ekstraliga",
        "season": "2016/17",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/artykul/2302/ekstraliga-rozgrywki-2016-2017",
        "parser": "static_teams",
        "evidence_type": "group_roster",
        "teams": [
            "Budowlani Łódź SA",
            "Arka Gdynia",
            "Pogoń Siedlce",
            "Budowlani Lublin",
            "Lechia Gdańsk",
            "Ogniwo Sopot",
            "Orkan Sochaczew",
            "Juvenia Kraków",
        ],
    },
    {
        "league": "ekstraliga",
        "season": "2018",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/artykul/4359/ekstraliga-kalendarz-fazy-ii",
        "parser": "article_div",
        "evidence_type": "snapshot",
    },
    {
        "league": "ekstraliga",
        "season": "2019",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/artykul/5118/ekstraliga-ogniwo-mistrzem-polski",
        "supplemental_urls": [
            "https://polskie.rugby/artykul/5004/ekstraliga-aktualna-tabela",
        ],
        "parser": "pzrugby_table",
        "parser_url": "http://pzrugby.pl/tabele/Tabelawynikiterminarz,52",
        "evidence_type": "final_table",
    },
    {
        "league": "sevens",
        "season": "2021",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/artykul/7136/plr7-viii-turniej-w-poznaniu",
        "parser": "plr7_snapshot",
        "evidence_type": "snapshot",
    },
    {
        "league": "ekstraliga",
        "season": "2020/21",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/storage/files/Ekstraliga%202021.pdf",
        "parser": "pdf_standings",
        "evidence_type": "final_table",
    },
    {
        "league": "ekstraliga",
        "season": "2021/22",
        "status": "potwierdzony",
        "url": "https://polskie.rugby/storage/files/Ekstraliga%20Rugby%20-%20Wiosna%202022.pdf",
        "parser": "pdf_standings",
        "evidence_type": "final_table",
    },
]

# (club_id, substring patterns — normalized ASCII-ish matching)
CLUB_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("warszawa-ligi", ("azs awf warszawa", "skra warszawa", "legia warszawa", "up fitness skra")),
    ("gdansk", ("rc lechia gdańsk", "lechia gdańsk", "lechia gdansk", "zielono-czarni lechia", "drew pal 2 rc lechia")),
    ("sopot", ("ogniwo sopot", "mks ogniwo", "politechnika gdańska ogniwo", "pg ogniwo", "energa ogniwo")),
    ("gdynia", ("arka gdynia", "rc arka")),
    ("sochaczew", ("orkan sochaczew", "orlen orkan")),
    ("siedlce", ("pogoń siedlce", "awenta pogoń")),
    ("lodz", ("budowlani łódź", "wizjamed grot budowlani", "ks budowlani wizjamed", "budo 2011")),
    ("lublin", ("budowlani lublin", "edach budowlani lublin", "pge edach budowlani")),
    ("krakow", ("juvenia kraków", "rzyks juvenia")),
    ("jarocin", ("sparta jarocin", "rk sparta")),
    ("bialystok", ("rugby białystok", "budmex rugby")),
    ("koszalin", ("ksrc koszalin",)),
    ("gniezno", ("tytan gniezno", "gkr tytan")),
    ("szczecin", ("kaskada szczecin",)),
    ("unislaw", ("rugby klub unisław", "rugby unisław", "rk unisław")),
    ("bytom", ("czarni bytom",)),
    ("czestochowa", ("rc częstochowa", "rugby club częstochowa", "rugby częstochowa")),
    ("bielsko", ("rc bielsko", "bielsko-biała", "bielsko biała")),
    ("katowice", ("piraci katowice",)),
    ("poznan", ("posnania poznań",)),
    ("pruszcz", ("zielono-czarni pruszcz", "pruszcz gdański")),
    ("boleslawiec", ("bolesławiec rugby",)),
    ("bydgoszcz", ("alfa bydgoszcz",)),
    ("wroclaw", ("rugby wrocław",)),
    ("ruda", ("rugby ruda", "ruda śląska")),
    ("ciechanow", ("ciechan ciechanów",)),
    ("nowy-sacz", ("biało-czarni nowy sącz", "nowy sącz")),
    ("biesal", ("rugby biesal",)),
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AFC-Rugby-sync/1.0)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AFC-Rugby-sync/1.0)"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"\s+", " ", text)
    return text


def short_names_from_html(fragment: str) -> list[str]:
    names = re.findall(
        r'<span class="make-short-name[^"]*">\s*([^<]+?)\s*</span>',
        fragment,
        flags=re.I,
    )
    out: list[str] = []
    seen: set[str] = set()
    for raw in names:
        name = re.sub(r"\s+", " ", raw).strip()
        name = re.sub(r"\*+$", "", name).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def teams_tabela(html: str) -> list[str]:
    block = re.search(r"<h2>Tabela</h2>.*?<tbody>(.*?)</tbody>", html, flags=re.I | re.S)
    if not block:
        return []
    return short_names_from_html(block.group(1))


def teams_article_div_rows(html: str) -> list[str]:
    teams: list[str] = []
    for match in re.finditer(r">\s*\d+\s+([^<]{4,80}?)\s+&nbsp;", html):
        name = unescape(re.sub(r"\s+", " ", match.group(1)).strip())
        name = re.sub(r"\s+&nbsp;.*$", "", name)
        if name and name not in teams:
            teams.append(name)
    if teams:
        return teams
    for match in re.finditer(
        r"<span[^>]*>\s*(\d+)\.\s*</span>\s*<span[^>]*>([^<]{3,80})</span>",
        html,
        flags=re.I,
    ):
        name = unescape(re.sub(r"\s+", " ", match.group(2)).strip())
        if name and name not in teams:
            teams.append(name)
    return teams


def teams_legacy_table_rows(html: str) -> list[str]:
    teams: list[str] = []
    for match in re.finditer(r"<tr><td>\d{2}</td><td>([^<]+)</td>", html, flags=re.I):
        name = unescape(re.sub(r"\s+", " ", match.group(1)).strip())
        if name and name not in teams:
            teams.append(name)
    return teams


def teams_plr7_snapshot(html: str) -> list[str]:
    teams = re.findall(r"\d+\.\s*([^<\-\u2013]+?)\s*[\-\u2013]\s*\d+\s*pkt", html, flags=re.I)
    out: list[str] = []
    for raw in teams:
        name = re.sub(r"\s+", " ", raw).strip()
        if name and name not in out:
            out.append(name)
    return out


def teams_pdf_standings(text: str) -> list[str]:
    teams: list[str] = []
    pattern = re.compile(
        r"([A-Za-zÀ-ž][^\n\d]{2,48}?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+:\d+)",
    )
    for match in pattern.finditer(text):
        name = re.sub(r"\s+", " ", match.group(1)).strip()
        if not name or len(name) < 4:
            continue
        if any(skip in name.lower() for skip in ("przewodnik", "ekstraliga", "sezon", "runda")):
            continue
        if name not in teams:
            teams.append(name)
    return teams


def pdf_text(url: str) -> str:
    try:
        from io import BytesIO

        import pypdf
    except ImportError:
        return ""
    data = fetch_bytes(url)
    reader = pypdf.PdfReader(BytesIO(data))
    return "".join((page.extract_text() or "") for page in reader.pages)


def teams_klasyfikacja(html: str) -> list[str]:
    block = re.search(
        r"Klasyfikacja końcowa[^<]*</strong>\s*<br\s*/>\s*(.*?)</p>",
        html,
        flags=re.I | re.S,
    )
    if not block:
        return []
    text = block.group(1)
    teams = re.findall(r"\d+\.\s*([^–\-]+?)\s*[–\-]\s*\d+\s*pkt", text, flags=re.I)
    return [re.sub(r"\s+", " ", t).strip() for t in teams]


def skip_team(norm: str) -> bool:
    if "barbarians" in norm:
        return True
    if "polska u18" in norm:
        return True
    if re.search(r"\bii\b", norm):
        return True
    if norm.endswith(" ii"):
        return True
    return False


def match_clubs(team_name: str) -> set[str]:
    norm = normalize(team_name)
    if skip_team(norm):
        return set()
    parts = [p.strip() for p in re.split(r"/", norm) if p.strip()]
    found: set[str] = set()
    for part in parts:
        for club_id, patterns in CLUB_PATTERNS:
            for pat in patterns:
                if normalize(pat) in part:
                    found.add(club_id)
                    break
    return found


def season_key(league: str, season: str) -> tuple[str, str]:
    return league, season


def resolve_teams(spec: dict, html: str) -> list[str]:
    parser = spec.get("parser", "tabela")
    if parser == "static_teams":
        return list(spec.get("teams") or [])
    if parser == "article_div":
        return teams_article_div_rows(html)
    if parser == "pzrugby_table":
        legacy_url = spec.get("parser_url") or spec["url"]
        return teams_legacy_table_rows(fetch(legacy_url))
    if parser == "plr7_snapshot":
        return teams_plr7_snapshot(html)
    if parser == "pdf_standings":
        return teams_pdf_standings(pdf_text(spec["url"]))
    if parser == "tabela":
        return teams_tabela(html)
    if parser in ("klasyfikacja",):
        return teams_klasyfikacja(html)
    if parser == "tabela_w_toku":
        return teams_tabela(html)
    return []


def evidence_for(spec: dict) -> str:
    if spec.get("evidence_type"):
        return spec["evidence_type"]
    return PARSER_EVIDENCE.get(spec.get("parser", ""), "final_table")


def apply_teams_to_clubs(
    spec: dict,
    teams: list[str],
    club_index: dict,
    report: dict[str, list[str]],
) -> None:
    key = f"{spec['league']} {spec['season']}"
    mapped: set[str] = set()
    for team in teams:
        ids = match_clubs(team)
        for cid in ids:
            mapped.add(cid)
            club = club_index[cid]
            sk = season_key(spec["league"], spec["season"])
            existing = {(s["league"], s["season"]) for s in club["seasons"]}
            if sk in existing:
                continue
            entry = {
                "league": spec["league"],
                "season": spec["season"],
                "status": spec["status"],
                "source_url": spec["url"],
                "evidence_type": evidence_for(spec),
            }
            if spec.get("supplemental_urls"):
                entry["supplemental_urls"] = spec["supplemental_urls"]
            if spec.get("status") == "w_toku":
                entry["as_of"] = WINDOW_CUTOFF
            club["seasons"].append(entry)
    report[key] = sorted(mapped)
    print(f"{key}: {len(teams)} teams parsed, {len(mapped)} clubs mapped ({evidence_for(spec)})")


def main() -> None:
    with JSON_PATH.open(encoding="utf-8") as fh:
        payload = json.load(fh)

    club_index = {c["club_id"]: c for c in payload["clubs"]}
    for club in payload["clubs"]:
        if club.get("historic"):
            continue
        club["seasons"] = []

    report: dict[str, list[str]] = {}

    all_specs = LEGACY_SEASON_SPECS + SEASON_PAGES
    for spec in all_specs:
        html = fetch(spec["url"]) if spec.get("parser") != "static_teams" else ""
        teams = resolve_teams(spec, html)
        apply_teams_to_clubs(spec, teams, club_index, report)

    payload["window"] = "2016-10-21 to 2026-10-21"
    payload["season_source_note"] = (
        "Season rows from PZR tables (sync_club_seasons.py). "
        "PLR7 2025/26 and 2026/27 not invented — see docs/planning/afc-rugby-map-sources.md."
    )
    with JSON_PATH.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("Wrote", JSON_PATH)


if __name__ == "__main__":
    main()
