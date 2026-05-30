import html
import json
import logging
import re
from difflib import SequenceMatcher
from typing import Any, Dict, List

from .heuristics_ai import analyze_change, generate_ai_summary

_LOGGER = logging.getLogger(__name__)

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600;700&display=swap');

/* ── Design tokens — dark gold system ── */
:root {
  --bg:           #0f1117;
  --surface:      #1a1e27;
  --surface2:     #22273a;
  --border:       rgba(255,255,255,0.07);
  --border-gold:  rgba(196,146,42,0.35);
  --text:         #e0e0e0;
  --muted:        #8a8f9a;
  --gold:         #c4922a;
  --gold-light:   #e0b060;
  --added-bg:     rgba(34,90,50,0.35);
  --added-border: rgba(52,168,83,0.5);
  --added-text:   #7edd9a;
  --deleted-bg:   rgba(100,28,28,0.35);
  --deleted-border:rgba(220,38,38,0.5);
  --deleted-text: #fca5a5;
  --changed-bg:   rgba(90,70,15,0.3);
  --changed-border:rgba(196,146,42,0.4);
  --changed-text: #f1e0a0;
  --unchanged-bg: transparent;
  --del-bg:       rgba(120,30,30,0.55);
  --del-color:    #ffb0b0;
  --ins-bg:       rgba(25,80,45,0.55);
  --ins-color:    #90f0b0;
}

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: 'Montserrat', sans-serif;
  font-weight: 300;
  background: var(--bg);
  color: var(--text);
  line-height: 1.65;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.container {
  max-width: 1060px;
  margin: 0 auto;
  padding: 2rem 1.5rem 5rem;
}

/* ── Top bar ── */
.report-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.back-link {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--gold);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: letter-spacing 0.25s ease, color 0.2s;
}
.back-link:hover { color: var(--gold-light); letter-spacing: 2px; }

.topbar-right { display: flex; align-items: center; gap: 0.6rem; }

/* ── Report header ── */
.report-header { margin-bottom: 2.5rem; }

.report-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 700;
  color: var(--text);
  margin: 0 0 0.2rem;
  display: inline-block;
}

.report-title::after {
  content: '';
  display: block;
  width: 52px;
  height: 3px;
  background: linear-gradient(90deg, var(--gold), var(--gold-light));
  margin: 10px 0 1rem;
  border-radius: 2px;
}

.report-meta {
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 400;
}

/* ── Chips / buttons ── */
.chip {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: 1px solid var(--border-gold);
  padding: 6px 14px;
  border-radius: 20px;
  margin: 3px;
  cursor: pointer;
  display: inline-block;
  background: var(--surface2);
  color: var(--text);
  transition: all 0.2s ease;
  user-select: none;
}
.chip:hover {
  border-color: var(--gold);
  color: var(--gold);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(196,146,42,0.15);
}
.chip.active {
  background: linear-gradient(90deg, var(--gold), var(--gold-light));
  border-color: transparent;
  color: #0f1117;
}

/* ── Cards ── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
  transition: border-color 0.2s;
}
.card:hover { border-color: var(--border-gold); }

.card.added    { border-left: 3px solid var(--added-border);   background: var(--added-bg); }
.card.deleted  { border-left: 3px solid var(--deleted-border); background: var(--deleted-bg); }
.card.changed  { border-left: 3px solid var(--changed-border); background: var(--changed-bg); }
.card.unchanged { opacity: 0.55; }
.card.unchanged:hover { opacity: 0.8; }

/* ── Score pills ── */
.score {
  font-weight: 700;
  font-size: 0.78rem;
  padding: 3px 8px;
  border-radius: 10px;
  margin-left: 6px;
  letter-spacing: 0.5px;
}
.score.low  { background: rgba(34,90,50,0.5);  color: var(--added-text); }
.score.med  { background: rgba(90,70,15,0.5);  color: var(--changed-text); }
.score.high { background: rgba(100,28,28,0.5); color: var(--deleted-text); }

/* ── Badges ── */
.badge {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 3px 8px;
  border-radius: 6px;
  background: var(--surface2);
  border: 1px solid var(--border-gold);
  color: var(--gold);
  margin-right: 5px;
}

/* ── Meta row ── */
.meta {
  font-size: 0.82rem;
  color: var(--muted);
  margin-bottom: 0.75rem;
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

/* ── Text sizes ── */
.small { font-size: 0.9rem; color: var(--text); }

/* ── AI section ── */
.ai-section {
  background: var(--surface2);
  border-left: 3px solid var(--gold);
  padding: 0.75rem 1rem;
  border-radius: 0 8px 8px 0;
  margin: 0.75rem 0;
  font-size: 0.85rem;
}

/* ── Inline diff ── */
del {
  background: var(--del-bg);
  color: var(--del-color);
  text-decoration: line-through;
  padding: 0 3px;
  border-radius: 3px;
}
ins {
  background: var(--ins-bg);
  color: var(--ins-color);
  text-decoration: none;
  padding: 0 3px;
  border-radius: 3px;
}

pre.diff {
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 1rem;
  border-radius: 8px;
  overflow: auto;
  font-size: 0.85rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0.5rem 0 0;
}

/* ── Tables ── */
table { border-collapse: collapse; margin-bottom: 0.75rem; width: 100%; }
td, th {
  border: 1px solid var(--border);
  padding: 8px 10px;
  vertical-align: top;
  font-size: 0.85rem;
}
tr:hover td { background: rgba(196,146,42,0.04); }

/* ── TOC ── */
.toc { line-height: 2; }
.toc a {
  text-decoration: none;
  margin-right: 6px;
  color: var(--gold);
  font-size: 0.82rem;
  font-weight: 600;
  transition: color 0.2s;
}
.toc a:hover { color: var(--gold-light); }

/* ── Controls bar ── */
.controls { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-gold); }

/* ── Mobile ── */
@media (max-width: 600px) {
  .container { padding: 1.2rem 1rem 4rem; }
  .report-topbar { flex-direction: column; align-items: flex-start; }
}
</style>
"""


# -------------------------
# Statistics and scoring
# -------------------------
def compute_stats_and_scores(block_diffs: List[Dict[str, Any]]) -> Dict[str, Any]:
    stats: Dict[str, Any] = {"added": 0, "deleted": 0, "changed": 0, "unchanged": 0, "by_type": {}}
    scored: List[tuple] = []

    for idx, b in enumerate(block_diffs):
        ch = b.get("change", "unknown")
        stats[ch] = stats.get(ch, 0) + 1

        typ = b.get("type") or (b.get("new", {}).get("type") or b.get("old", {}).get("type") or "unknown")
        stats["by_type"].setdefault(typ, {"added": 0, "deleted": 0, "changed": 0, "unchanged": 0})
        cat = ch if ch in ("added", "deleted", "changed", "unchanged") else "changed"
        stats["by_type"][typ][cat] += 1

        # scoring
        score = 0.0
        if ch in ("added", "deleted"):
            score += 2.5
        if ch == "changed":
            old_text = (b.get("old", {}).get("text") or "")
            new_text = (b.get("new", {}).get("text") or "")
            ratio = SequenceMatcher(None, old_text, new_text).ratio()
            score += (1.0 - ratio) * 6.0
            combined = (old_text + " " + new_text)
            if re.search(r"\d", combined):
                score += 0.8
            if re.search(r"\b(kg|m|mm|cm|%|km|PLN|EUR|kW)\b", combined, re.I):
                score += 0.8
            if re.search(r"\b(19|20)\d{2}\b", combined):
                score += 0.6
        if typ in ("image", "table"):
            score += 2.0

        score = round(max(0.0, min(10.0, score)), 2)
        b["_score"] = score
        scored.append((score, idx))

    # sort descending by score, TOC will later be sorted by AI semantic score if available
    scored.sort(reverse=True)
    stats["top_changes"] = [i for _, i in scored if block_diffs[i].get("change") in ("changed", "added", "deleted")]
    return stats


# -------------------------
# Render helpers
# -------------------------
def _render_ai_info(f, b: Dict[str, Any]):
    """AI section — rendered if data is present."""
    labels = b.get("_ai_labels") or []
    sem = b.get("_ai_sem_score", None)
    typ = b.get("_ai_type", "")
    conf = b.get("_ai_conf", None)

    # if none present, render nothing
    if not (labels or sem is not None or typ or conf):
        return

    f.write("<div class='ai-section'><b>🧠 <span data-i18n='ai_summary'>AI Summary</span>:</b> ")
    if labels:
        f.write(" ".join(f"<span class='badge'>{html.escape(label)}</span>" for label in labels))
    if typ:
        f.write(f"<span class='badge'><span data-i18n='type'>Type</span>: {html.escape(typ)}</span>")
    if sem is not None:
        f.write(f" <span class='badge'><span data-i18n='relevance'>Relevance</span>: {sem}/10</span>")
    if conf is not None:
        f.write(f" <span class='badge'><span data-i18n='confidence'>Confidence</span>: {conf}</span>")
    f.write("</div>")


def _render_paragraph(f, b, cls):
    _render_ai_info(f, b)

    if b.get("change") == "changed":
        oldt = html.escape(b.get("old", {}).get("text", "") or "")
        newt = html.escape(b.get("new", {}).get("text", "") or "")
        f.write(f"<p class='small'><b><span data-i18n='old'>Przed</span>:</b> {oldt}</p>")
        f.write(f"<p class='small'><b><span data-i18n='new'>Po</span>:</b> {newt}</p>")
        inline = b.get("inline_html")
        if inline:
            f.write(f"<div class='small'><b><span data-i18n='inline'>Różnice</span>:</b>"
                    f"<pre class='diff'>{inline}</pre></div>")
    else:
        text = html.escape(b.get("text") or b.get("old", {}).get("text") or "")
        f.write(f"<p class='small'>{text}</p>")


def _render_table(f, b, cls):
    _render_ai_info(f, b)

    table_changes = b.get("table_changes")
    if table_changes:
        rows = table_changes
    else:
        rows = b.get("table") or b.get("new", {}).get("table") or []

    f.write("<table>")
    for row in rows:
        f.write("<tr>")
        for cell in row:
            if isinstance(cell, dict):
                if cell.get("type") == "same":
                    f.write(f"<td>{html.escape(cell.get('text',''))}</td>")
                else:
                    f.write(f"<td>{cell.get('inline_html','')}</td>")
            else:
                f.write(f"<td>{html.escape(str(cell))}</td>")
        f.write("</tr>")
    f.write("</table>")


def _render_image(f, b, cls):
    sha = b.get("sha1") or b.get("new", {}).get("sha1") or ""
    _render_ai_info(f, b)
    f.write(f"<p class='small'>SHA1: {html.escape((sha or '')[:12])}…</p>")

# -------------------------
# Main render
# -------------------------
def generate_html_report(block_diffs: List[Dict[str, Any]], output_path: str = "report.html") -> None:
    # 1) basic statistics and scoring
    stats = compute_stats_and_scores(block_diffs)

    # 2) AI analysis (for "changed") — fills _ai_* fields
    for b in block_diffs:
        if b.get("change") == "changed":
            try:
                ai = analyze_change(b)
                b["_ai_labels"] = ai.get("labels")
                b["_ai_sem_score"] = ai.get("semantic_score")
                b["_ai_type"] = ai.get("change_type")
                b["_ai_conf"] = ai.get("confidence")
            except Exception:
                _LOGGER.exception("AI analyze_change error", exc_info=True)
                b["_ai_labels"] = []
                b["_ai_sem_score"] = None
                b["_ai_type"] = ""
                b["_ai_conf"] = None

    # 3) prepare TOC sorted by ai_score (fallback to _score)
    # We want the most significant first
    indexed = list(range(len(block_diffs)))

    def sort_key(i):
        ai_s = block_diffs[i].get("_ai_sem_score")
        score = block_diffs[i].get("_score", 0)
        # if ai_s is None -> use score * 0.6 to still include
        if ai_s is None:
            return score * 0.6
        return ai_s + (score * 0.1)

    # filter to include only changed/added/deleted
    toc_items = [i for i in indexed if block_diffs[i].get("change") in ("changed", "added", "deleted")]
    toc_items.sort(key=sort_key, reverse=True)

    summary_html = generate_ai_summary(block_diffs)

    # 4) generate file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html lang='pl'><head>")
        f.write("<meta charset='utf-8'>")
        f.write("<meta name='viewport' content='width=device-width,initial-scale=1'>")
        f.write("<title data-i18n='title'>Raport porównania dokumentów</title>")
        f.write(STYLE)

        # ── i18n dictionary + lang switcher logic ──
        f.write("""
        <script>
        const I18N = {
          pl: {
            added:          "dodane",
            deleted:        "usunięte",
            changed:        "zmienione",
            unchanged:      "bez zmian",
            paragraph:      "Akapit",
            table:          "Tabela",
            image:          "Obraz",
            score:          "Wynik",
            back:           "Powrót do DocDiff",
            title:          "Raport porównania dokumentów",
            total:          "Łączna liczba bloków",
            ai_summary:     "Podsumowanie AI",
            toc:            "Najistotniejsze zmiany",
            hide_unchanged: "Ukryj niezmienione",
            show_unchanged: "Pokaż niezmienione",
            change:         "zmiana",
            old:            "Przed",
            new:            "Po",
            inline:         "Różnice",
            relevance:      "Istotność",
            confidence:     "Pewność",
            type:           "Typ",
            filter_change:  "Filtruj zmianę:",
            filter_type:    "Filtruj typ:"
          },
          en: {
            added:          "added",
            deleted:        "deleted",
            changed:        "changed",
            unchanged:      "unchanged",
            paragraph:      "Paragraph",
            table:          "Table",
            image:          "Image",
            score:          "Score",
            back:           "Back to DocDiff",
            title:          "Document Comparison Report",
            total:          "Total blocks",
            ai_summary:     "AI Summary",
            toc:            "Most Significant Changes",
            hide_unchanged: "Hide unchanged",
            show_unchanged: "Show unchanged",
            change:         "change",
            old:            "Before",
            new:            "After",
            inline:         "Inline diff",
            relevance:      "Relevance",
            confidence:     "Confidence",
            type:           "Type",
            filter_change:  "Filter by change:",
            filter_type:    "Filter by type:"
          }
        };

        let CURRENT_LANG = "pl";

        function setLang(lang) {
          CURRENT_LANG = lang;
          document.documentElement.lang = lang;
          document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.dataset.i18n;
            if (I18N[lang][key] !== undefined) el.textContent = I18N[lang][key];
          });
          // update document title
          document.title = I18N[lang].title;
          // update collapse button
          const cb = document.querySelector(".collapse-toggle");
          if (cb) {
            cb.textContent = cb.dataset.state === "hidden"
              ? I18N[lang].show_unchanged
              : I18N[lang].hide_unchanged;
          }
          // mark active lang button
          document.querySelectorAll(".lang-btn").forEach(b => {
            b.classList.toggle("active", b.dataset.lang === lang);
          });
        }
        </script>
        """)

        # ── filter + collapse + scroll JS ──
        f.write("""
        <script defer>
        function filterBy() {
          document.querySelectorAll("[data-change]").forEach(function(n) {
            const ch  = n.dataset.change;
            const typ = n.dataset.type;
            let show = true;
            if (window.filterChange.length && !window.filterChange.includes(ch))  show = false;
            if (window.filterType.length   && !window.filterType.includes(typ))   show = false;
            n.style.display = show ? "" : "none";
          });
        }

        document.addEventListener("DOMContentLoaded", function () {
          window.filterChange = [];
          window.filterType   = [];

          // chip filters
          document.querySelectorAll(".chip.change").forEach(function(c) {
            c.addEventListener("click", function() {
              c.classList.toggle("active");
              const v = c.dataset.val;
              if (c.classList.contains("active")) window.filterChange.push(v);
              else window.filterChange = window.filterChange.filter(x => x !== v);
              filterBy();
            });
          });
          document.querySelectorAll(".chip.type").forEach(function(c) {
            c.addEventListener("click", function() {
              c.classList.toggle("active");
              const v = c.dataset.val;
              if (c.classList.contains("active")) window.filterType.push(v);
              else window.filterType = window.filterType.filter(x => x !== v);
              filterBy();
            });
          });

          // lang buttons
          document.querySelectorAll(".lang-btn").forEach(function(btn) {
            btn.addEventListener("click", function() { setLang(this.dataset.lang); });
          });

          // collapse unchanged
          const collBtn = document.querySelector(".collapse-toggle");
          if (collBtn) {
            collBtn.addEventListener("click", function() {
              const unchanged = Array.from(document.querySelectorAll(".unchanged"));
              const anyVisible = unchanged.some(x => x.style.display !== "none");
              unchanged.forEach(x => x.style.display = anyVisible ? "none" : "");
              this.dataset.state = anyVisible ? "hidden" : "shown";
              this.textContent = anyVisible
                ? I18N[CURRENT_LANG].show_unchanged
                : I18N[CURRENT_LANG].hide_unchanged;
            });
          }

          // smooth TOC scroll
          document.querySelectorAll(".toc a").forEach(function(a) {
            a.addEventListener("click", function(e) {
              e.preventDefault();
              const el = document.getElementById(this.getAttribute("href").slice(1));
              if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
            });
          });

          // init language
          setLang(CURRENT_LANG);
        });
        </script>
        """)

        # ── body open ──
        f.write("</head><body><div class='container'>")

        # ── top bar: back link + lang switcher ──
        f.write("""
        <div class='report-topbar'>
          <a href='/docdiff/' class='back-link'>&#8592; <span data-i18n='back'>Powrót do DocDiff</span></a>
          <div class='topbar-right'>
            <button class='chip lang-btn' data-lang='pl'>PL</button>
            <button class='chip lang-btn' data-lang='en'>EN</button>
          </div>
        </div>
        """)

        # ── report header ──
        f.write("<div class='report-header'>")
        f.write("<h1 class='report-title' data-i18n='title'>Raport porównania dokumentów</h1>")
        f.write(f"<div class='report-meta'><span data-i18n='total'>Łączna liczba bloków</span>: {len(block_diffs)}"
                f" &nbsp;|&nbsp; "
                f"<span style='color:var(--added-text)'>+{stats.get('added',0)}</span>"
                f" &nbsp;"
                f"<span style='color:var(--deleted-text)'>-{stats.get('deleted',0)}</span>"
                f" &nbsp;"
                f"<span style='color:var(--changed-text)'>&#9654; {stats.get('changed',0)}</span>"
                f"</div>")
        f.write("</div>")

        # ── AI summary card ──
        safe_summary = html.escape(summary_html)
        f.write(f"""
        <div class='card' style='margin-bottom:1.5rem;'>
          <div class='ai-section' style='margin:0;border-radius:8px;'>
            <b>&#129504; <span data-i18n='ai_summary'>Podsumowanie AI</span>:</b>
            <div class='small' style='margin-top:0.4rem;'>{safe_summary}</div>
          </div>
        </div>
        """)

        # ── filter controls ──
        f.write("<div class='card controls' style='margin-bottom:1rem;gap:8px;'>")
        f.write("<span style='font-size:0.78rem;font-weight:600;text-transform:uppercase;"
                "letter-spacing:1px;color:var(--muted);' data-i18n='filter_change'>Filtruj zmianę:</span>")
        for ch in ("added", "deleted", "changed", "unchanged"):
            f.write(f"<span class='chip change' data-val='{ch}' data-i18n='{ch}'>{ch}</span>")
        if stats["by_type"]:
            f.write("<span style='font-size:0.78rem;font-weight:600;text-transform:uppercase;"
                    "letter-spacing:1px;color:var(--muted);margin-left:0.5rem;' data-i18n='filter_type'>Filtruj typ:</span>")
            for t in stats["by_type"]:
                f.write(f"<span class='chip type' data-val='{html.escape(t)}' data-i18n='{html.escape(t)}'>{html.escape(t)}</span>")
        f.write("</div>")

        # ── TOC ──
        f.write("<div class='toc card' style='margin-bottom:1rem;'>")
        f.write("<b data-i18n='toc'>Najistotniejsze zmiany</b>:<br>")
        for i in toc_items[:200]:
            b = block_diffs[i]
            name  = html.escape(str(b.get("type") or "blk"))
            aisc  = b.get("_ai_sem_score")
            score = b.get("_score", 0)
            label = f"{aisc}/10" if aisc is not None else f"{score}"
            f.write(f"<a href='#blk{i}'>#{i}&thinsp;({name})&thinsp;{label}</a>")
        f.write("</div>")

        # ── collapse toggle ──
        f.write("<div style='margin-bottom:1.5rem;'>")
        f.write("<button class='collapse-toggle chip' data-state='shown' data-i18n='hide_unchanged'>Ukryj niezmienione</button>")
        f.write("</div>")

        # render blocks
        for i, b in enumerate(block_diffs):
            ch = str(b.get("change", "unknown"))
            typ = b.get("type") or b.get("new", {}).get("type") or b.get("old", {}).get("type") or "unknown"
            typ = str(typ)
            score = b.get("_score", 0)
            score_cls = "low" if score < 3 else ("med" if score < 6 else "high")

            f.write(f"<div id='blk{i}' class='card {html.escape(ch)}' "
                    f"data-change='{html.escape(ch)}' data-type='{html.escape(typ)}'>")

            # meta row
            f.write("<div class='meta'>")
            f.write(f"<span class='badge' data-i18n='{html.escape(typ)}'>{html.escape(typ).upper()}</span>")
            f.write(f"<span class='badge' data-i18n='{html.escape(ch)}'>{html.escape(ch)}</span>")
            f.write(f"<span class='score {score_cls}'>{score}</span>")
            f.write("</div>")

            # render content by type (no extra wrapping card — already inside one)
            if typ == "paragraph":
                _render_paragraph(f, b, html.escape(ch))
            elif typ == "table":
                _render_table(f, b, html.escape(ch))
            elif typ == "image":
                _render_image(f, b, html.escape(ch))
            else:
                f.write(f"<pre class='diff'>{html.escape(str(b))}</pre>")

            f.write("</div>")

        # footer / close
        f.write("</div></body></html>")


# -------------------------
# JSON export
# -------------------------
def generate_json_report(block_diffs: List[Dict[str, Any]], output_path: str = "report.json") -> None:
    """Save the comparison report as JSON."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(block_diffs, f, ensure_ascii=False, indent=2)
    except Exception:
        _LOGGER.exception("Error while writing JSON report")
        raise