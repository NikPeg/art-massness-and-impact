#!/usr/bin/env python3
"""Build compact English or Russian GWI charts from the project's transcribed observations."""

from pathlib import Path
import html
from figure_i18n import cli_language, save
from figure_captions import caption
import xml.etree.ElementTree as ET

from build_figures import ROOT, table_with

OUT = ROOT / "figures/gwi"
LABELS = {
    "short_video": "Короткие видео",
    "long_video": "Длинные онлайн-видео",
    "music": "Музыкальный стриминг",
    "games": "Видеоигры",
    "games_mobile": "Видеоигры: мобильные",
    "games_pc_console": "Видеоигры: ПК и консоли",
    "series": "ТВ-стриминг: весь контент",
}


def build(lang="en"):
    OUT.mkdir(parents=True, exist_ok=True)
    rows = table_with(ROOT / "data/media_use_2026.md", "weekly_reach_percent")
    panels = []
    configs = [
        ("reach", "Недельный охват медиа", "weekly_reach_percent", 100, 20, "Охват, %", "%"),
        ("time", "Время потребления медиа", "weekly_minutes", 500, 100, "Минут в неделю", " мин"),
        ("frequency", "Частота потребления медиа", "days_per_week", 7, 1, "Дней в неделю", ""),
    ]
    for stem, title, key, maximum, step, axis, suffix in configs:
        selected = [r for r in rows if r[key] != "NA"]
        if key == "days_per_week":
            # Keep device-specific observations separate; no all-game mean is available.
            games = next(r for r in selected if r["category"] == "games")
            selected = [r for r in selected if r["category"] != "games"] + [
                {**games, "category": "games_mobile"},
                {**games, "category": "games_pc_console", "days_per_week": games["additional_days_per_week"]},
            ]
        selected.sort(key=lambda r: float(r[key]), reverse=True)
        bottom = 146 + len(selected) * 64
        height = bottom + 70
        body = []

        def text(x, y, value, size=17, weight=400, anchor="start"):
            body.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
                        f'font-weight="{weight}">{html.escape(str(value))}</text>')

        text(30, 43, title, 27, 700)
        text(30, 76, "II квартал 2026 · Интернет-пользователи 16+ · GWI", 16)
        left, plot_width = 345, 560
        for tick in range(0, maximum + 1, step):
            x = left + tick / maximum * plot_width
            body.append(f'<line x1="{x}" y1="108" x2="{x}" y2="{bottom}" stroke="#e3e8ee"/>')
            text(x, bottom+24, tick, 13, anchor="middle")
        for i, row in enumerate(selected):
            value = float(row[key])
            y = 145 + i*64
            length = value / maximum * plot_width
            is_short = row["category"] == "short_video"
            text(30, y+6, LABELS[row["category"]], 17, 700 if is_short else 400)
            color = "#1768b5" if is_short else "#8b9bad"
            body.append(f'<rect data-category="{row["category"]}" data-value="{value}" x="{left}" '
                        f'y="{y-18}" width="{length}" height="32" rx="3" fill="{color}"/>')
            label = f"{value:g}".replace(".", ",") + suffix
            if key == "weekly_minutes":
                label = f"{int(value)//60}:{int(value)%60:02}"
            text(left+length+12, y+5, label, 17, 600)
        text(left+plot_width, bottom+54, axis + (" · подписи Ч:ММ" if key == "weekly_minutes" else ""), 14, anchor="end")
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="{height}" '
               f'viewBox="0 0 1040 {height}" role="img" aria-labelledby="title desc" xml:lang="ru">'
               f'<title id="title">{title}</title><desc id="desc">Оценки GWI по измеренным категориям. '
               'Источники, легенда и ограничения находятся в соседнем TXT.</desc>'
               '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#253247;font-variant-numeric:tabular-nums}</style>'
               '<rect width="100%" height="100%" fill="white"/>' + "".join(body) + '</svg>\n')
        ET.fromstring(svg)
        save(OUT / f"{stem}.svg", svg, lang, source_lang="ru")
        save(OUT / f"{stem}.txt", caption("gwi-" + stem, lang), lang, source_lang=lang)
        panels.append(f'<section><img src="{stem}.svg" alt="{title}"><a href="{stem}.txt">Пояснение, источники и легенда</a></section>')
    panels.append('<section><img src="../media-growth-h1-2026.svg" alt="Рост потребления медиа: первое полугодие 2026">'
                  '<a href="../media-growth-h1-2026.txt">Пояснение, источники и легенда</a></section>')
    page = ('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Медиа: данные GWI</title><style>body{max-width:1040px;margin:24px auto;padding:0 16px;font-family:system-ui;line-height:1.5}'
            'img{width:100%;height:auto}section{margin:32px 0}a{color:#1768b5}</style>'
            '<h1>Медиа: данные GWI</h1><p>Охват, время и частота — II квартал 2026; рост — первое полугодие 2026. '
            'Источники и ограничения указаны в пояснениях к каждому графику.</p>' + "".join(panels) + '</html>\n')
    save(OUT / "index.html", page, lang, source_lang="ru")


if __name__ == "__main__":
    build(cli_language())
