#!/usr/bin/env python3
"""Render the transcribed GMI26 chart in English or Russian, without dependencies/network."""

import html
from figure_i18n import cli_language, save
from figure_captions import caption
from pathlib import Path

from build_figures import table_with

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
STEM = "media-growth-h1-2026"


def build(lang="en"):
    rows = table_with(ROOT / "data/media_growth_h1_2026.md", "change_percent")
    rows = sorted(rows, key=lambda r: float(r["change_percent"]), reverse=True)
    width, height, zero, scale = 1120, 880, 850, 36
    parts = []

    def text(x, y, value, size=16, weight=400, anchor="start", color="#253247"):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                     f'text-anchor="{anchor}" fill="{color}">{html.escape(str(value))}</text>')

    parts.append('<rect width="1120" height="880" fill="#ffffff"/>')
    text(36, 48, "Рост времени потребления медиа", 29, 700)
    text(36, 80, "Первое полугодие 2026 · Годовое изменение, по данным GWI", 16)
    text(36, 130, "Категория", 15, 600)
    text(525, 130, "Ч:ММ / неделю", 15, 600, "end")
    text(850, 130, "Изменение времени, %", 15, 600, "middle")
    for tick in (-6, -4, -2, 0, 2, 4, 6):
        x = zero + tick * scale
        parts.append(f'<line x1="{x}" y1="150" x2="{x}" y2="820" stroke="{("#8794a5" if tick == 0 else "#e5eaf0")}"/>')
        text(x, 850, str(tick).replace("-", "−"), 13, anchor="middle")
    for i, r in enumerate(rows):
        y = 180 + 55 * i
        value = float(r["change_percent"])
        if r["category"] == "short_video":
            parts.append(f'<rect x="24" y="{y-28}" width="1072" height="48" rx="8" fill="#eaf3ff"/>')
        text(36, y+3, r["label_ru"], 18, 700 if i == 0 else 400)
        text(525, y+3, r["weekly_hhmm"], 18, 600, "end")
        end = zero + value * scale
        color = "#1768b5" if value > 0 else "#6b7788"
        label = ("+" if value > 0 else "−" if value < 0 else "") + f"{abs(value):.1f}".replace(".", ",") + "%"
        parts.append(f'<rect data-category="{r["category"]}" data-value="{value}" x="{min(zero,end)}" '
                     f'y="{y-20}" width="{abs(value)*scale}" height="30" rx="3" fill="{color}"/>')
        text(end + (9 if value >= 0 else -9), y+3, label, 16, 600, "start" if value >= 0 else "end")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="880" viewBox="0 0 1120 880" '
           'role="img" aria-labelledby="growth-title growth-desc" xml:lang="ru">'
           '<title id="growth-title">Рост времени потребления медиа, первое полугодие 2026</title>'
           '<desc id="growth-desc">Короткие видео: +5,2%, мобильные игры: +4,2%. '
           'Рейтинг оценок GWI по 12 категориям; статистическая значимость различий не установлена.</desc>'
           '<style>text{font-family:Arial,Helvetica,sans-serif;font-variant-numeric:tabular-nums}</style>'
           + "".join(parts) + '</svg>\n')
    OUT.mkdir(exist_ok=True)
    save(OUT / f"{STEM}.svg", svg, lang, source_lang="ru")
    save(OUT / f"{STEM}.txt", caption("growth", lang), lang, source_lang=lang)
    page = ('<!doctype html><html lang="ru"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Рост потребления медиа — первое полугодие 2026</title>'
            '<style>body{max-width:1120px;margin:20px auto;padding:0 12px;font-family:system-ui}img{width:100%;height:auto}</style>'
            f'<img src="{STEM}.svg" alt="Рост времени потребления 12 категорий медиа">'
            f'<p><a href="{STEM}.txt">Данные, источники и ограничения</a> · '
            '<a href="../data/media_growth_h1_2026.md">Исходная таблица</a></p></html>\n')
    save(OUT / f"{STEM}.html", page, lang, source_lang="ru")


if __name__ == "__main__":
    build(cli_language())
