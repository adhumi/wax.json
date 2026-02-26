#!/usr/bin/env python3
"""Generate index.html from glide_wax.json."""

import json
import html
from pathlib import Path

LABELS = {
    "format_type": {
        "block_hot": "Bloc (fer)",
        "block_rub_roto": "Bloc (frottement/roto)",
        "block_rub": "Bloc (frottement)",
        "liquid": "Liquide",
        "liquid_spray": "Spray",
        "powder_hot": "Poudre (fer)",
        "powder": "Poudre",
        "paste_rub": "Pâte",
    },
    "level": {
        "beginner": "Débutant",
        "sport": "Sport",
        "expert": "Expert",
    },
    "role": {
        "base_prep": "Préparation base",
        "base": "Base",
        "day_wax": "Fart du jour",
        "top_coat": "Couche finale",
        "universal": "Universel",
        "cleaner": "Nettoyant",
        "additive": "Additif",
    },
    "snow_type": {
        "heavy_new": "Neige lourde neuve",
        "artificial": "Artificielle",
        "fresh_falling": "Neige tombante",
        "fine_fresh": "Fine fraîche",
        "mixed_new_dirty_base": "Mixte neuve/sale",
        "compact": "Compacte",
        "compact_glazed": "Compacte glacée",
        "compact_dirty": "Compacte sale",
        "transformed": "Transformée",
        "wet": "Mouillée",
        "dry_grain": "Grain sec",
        "wet_grain": "Grain humide",
    },
}


def fmt(val):
    """Escape a value for HTML."""
    if val is None:
        return "—"
    return html.escape(str(val))


def fmt_temp_range(p):
    tmin = p.get("temp_min_c")
    tmax = p.get("temp_max_c")
    if tmin is None and tmax is None:
        return "—"
    parts = []
    if tmin is not None:
        parts.append(f"{tmin}")
    if tmax is not None:
        parts.append(f"{tmax}")
    return " / ".join(parts) + " °C"


def fmt_humidity(p):
    hmin = p.get("humidity_min")
    hmax = p.get("humidity_max")
    if hmin is None and hmax is None:
        return "—"
    if hmin is not None and hmax is not None:
        return f"{hmin}–{hmax} %"
    if hmin is not None:
        return f"≥ {hmin} %"
    return f"≤ {hmax} %"


def fmt_list(values, category):
    mapping = LABELS.get(category, {})
    return ", ".join(mapping.get(v, v) for v in values)


def badge_level(level):
    cls = {"beginner": "lvl-beg", "sport": "lvl-spo", "expert": "lvl-exp"}.get(
        level, ""
    )
    label = LABELS["level"].get(level, level)
    return f'<span class="badge {cls}">{html.escape(label)}</span>'


def badge_bool(val, label_true, label_false):
    if val:
        return f'<span class="badge badge-yes">{label_true}</span>'
    return f'<span class="badge badge-no">{label_false}</span>'


def generate_html(data):
    meta = data["metadata"]
    products = data["products"]

    brands = sorted({p["brand"] for p in products})
    brand_options = "\n".join(
        f'        <option value="{html.escape(b)}">{html.escape(b)}</option>'
        for b in brands
    )

    rows = []
    for p in products:
        comment_fr = ""
        if p.get("comment"):
            comment_fr = p["comment"].get("fr_FR", "") or ""

        img_url = html.escape(p.get('image_url', ''))
        img_tag = f'<img class="thumb" src="{img_url}" alt="{fmt(p["name"])}" loading="lazy">' if img_url else '—'

        row = f"""      <tr data-brand="{html.escape(p['brand'])}">
        <td>{img_tag}</td>
        <td><strong>{fmt(p['name'])}</strong></td>
        <td>{fmt(p['brand'])}</td>
        <td>{fmt(p.get('product_line'))}</td>
        <td>{LABELS['format_type'].get(p['format_type'], p['format_type'])}</td>
        <td>{fmt_temp_range(p)}</td>
        <td>{fmt(p.get('iron_temp_c', '—'))} {('°C' if p.get('iron_temp_c') is not None else '')}</td>
        <td>{fmt_humidity(p)}</td>
        <td class="snow-col">{fmt_list(p.get('snow_type', []), 'snow_type')}</td>
        <td>{badge_level(p['level'])}</td>
        <td>{fmt_list(p.get('role', []), 'role')}</td>
        <td>{badge_bool(p['eco'], 'Éco', '—')}</td>
        <td class="comment-col">{html.escape(comment_fr)}</td>
      </tr>"""
        rows.append(row)

    rows_html = "\n".join(rows)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(meta['title'])}</title>
  <style>
    :root {{
      --bg: #f8f9fa;
      --card: #fff;
      --border: #dee2e6;
      --accent: #2563eb;
      --text: #212529;
      --muted: #6c757d;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 1.5rem;
    }}
    header {{
      max-width: 1600px;
      margin: 0 auto 1.5rem;
    }}
    header h1 {{
      font-size: 1.6rem;
      margin-bottom: .25rem;
    }}
    header p {{
      color: var(--muted);
      font-size: .9rem;
    }}
    .toolbar {{
      max-width: 1600px;
      margin: 0 auto 1rem;
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      align-items: center;
    }}
    .toolbar input, .toolbar select {{
      padding: .4rem .6rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: .9rem;
    }}
    .toolbar input {{ width: 260px; }}
    .count {{
      color: var(--muted);
      font-size: .85rem;
      margin-left: auto;
    }}
    .table-wrap {{
      max-width: 1600px;
      margin: 0 auto;
      overflow-x: auto;
      background: var(--card);
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: .85rem;
    }}
    thead {{
      position: sticky;
      top: 0;
      z-index: 2;
    }}
    th {{
      background: #e9ecef;
      text-align: left;
      padding: .55rem .6rem;
      white-space: nowrap;
      border-bottom: 2px solid var(--border);
      cursor: pointer;
      user-select: none;
    }}
    th:hover {{ background: #dde1e5; }}
    td {{
      padding: .45rem .6rem;
      border-bottom: 1px solid #f0f0f0;
      vertical-align: top;
    }}
    tr:hover td {{ background: #f1f5ff; }}
    .thumb {{ width: 40px; height: 40px; object-fit: contain; border-radius: 4px; background: #f8f9fa; }}
    .snow-col {{ max-width: 180px; }}
    .comment-col {{ max-width: 260px; font-size: .8rem; color: var(--muted); }}
    .badge {{
      display: inline-block;
      padding: .15rem .45rem;
      border-radius: 4px;
      font-size: .75rem;
      font-weight: 600;
    }}
    .lvl-beg {{ background: #d1fae5; color: #065f46; }}
    .lvl-spo {{ background: #dbeafe; color: #1e40af; }}
    .lvl-exp {{ background: #fde68a; color: #92400e; }}
    .badge-yes {{ background: #d1fae5; color: #065f46; }}
    .badge-no {{ background: #f3f4f6; color: #9ca3af; }}
    footer {{
      max-width: 1600px;
      margin: 1.5rem auto 0;
      text-align: center;
      font-size: .8rem;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <header>
    <h1>Catalogue de farts de glisse</h1>
    <p>Version {html.escape(meta['version'])} — {html.escape(meta['compilation_date'])} — {len(products)} produits</p>
  </header>

  <div class="toolbar">
    <input type="text" id="search" placeholder="Rechercher un fart…">
    <select id="brandFilter">
      <option value="">Toutes les marques</option>
{brand_options}
    </select>
    <span class="count" id="count">{len(products)} produits</span>
  </div>

  <div class="table-wrap">
    <table id="waxTable">
      <thead>
        <tr>
          <th></th>
          <th>Nom</th>
          <th>Marque</th>
          <th>Gamme</th>
          <th>Format</th>
          <th>Température</th>
          <th>Fer</th>
          <th>Humidité</th>
          <th>Neige</th>
          <th>Niveau</th>
          <th>Rôle</th>
          <th>Éco</th>
          <th>Commentaire</th>
        </tr>
      </thead>
      <tbody>
{rows_html}
      </tbody>
    </table>
  </div>

  <footer>
    Généré à partir de <code>glide_wax.json</code> v{html.escape(meta['version'])}
    — Sources\u00a0: {', '.join(html.escape(s) for s in meta['sources'])}
  </footer>

  <script>
    const table = document.getElementById('waxTable');
    const tbody = table.querySelector('tbody');
    const searchInput = document.getElementById('search');
    const brandSelect = document.getElementById('brandFilter');
    const countSpan = document.getElementById('count');

    function filterRows() {{
      const q = searchInput.value.toLowerCase();
      const brand = brandSelect.value;
      let visible = 0;
      for (const row of tbody.rows) {{
        const text = row.textContent.toLowerCase();
        const matchSearch = !q || text.includes(q);
        const matchBrand = !brand || row.dataset.brand === brand;
        const show = matchSearch && matchBrand;
        row.style.display = show ? '' : 'none';
        if (show) visible++;
      }}
      countSpan.textContent = visible + ' produit' + (visible !== 1 ? 's' : '');
    }}

    searchInput.addEventListener('input', filterRows);
    brandSelect.addEventListener('change', filterRows);

    // Simple column sort
    table.querySelectorAll('th').forEach((th, idx) => {{
      let asc = true;
      th.addEventListener('click', () => {{
        const rows = Array.from(tbody.rows);
        rows.sort((a, b) => {{
          const av = a.cells[idx].textContent.trim();
          const bv = b.cells[idx].textContent.trim();
          return asc ? av.localeCompare(bv, 'fr', {{numeric: true}}) : bv.localeCompare(av, 'fr', {{numeric: true}});
        }});
        rows.forEach(r => tbody.appendChild(r));
        asc = !asc;
      }});
    }});
  </script>
</body>
</html>"""


def main():
    src = Path(__file__).parent / "glide_wax.json"
    dest = Path(__file__).parent / "index.html"

    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    html_content = generate_html(data)

    with open(dest, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated {dest} ({len(data['products'])} products)")


if __name__ == "__main__":
    main()
