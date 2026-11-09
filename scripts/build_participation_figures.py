#!/usr/bin/env python3
"""Render selected participation surveys as SVGs with adjacent TXT annotations."""

from build_figures import ROOT, OUT, tables, text, line, mark, svg_doc, write, annotation

DATA = ROOT / "data/participation_and_breadth.md"
FIGURES = [
    ("Active artistic participation, EU27", "active-participation-eu-2025.svg"),
    ("Social differences in arts participation, England", "social-breadth-england-2024-25.svg"),
]


def observations(column):
    matches = [rows for header, rows in tables(DATA) if column in header]
    if len(matches) != 1:
        raise ValueError(f"Expected one participation table containing {column}")
    rows = matches[0]
    for row in rows:
        value = float(row["participation_percent"])
        if not 0 <= value <= 100:
            raise ValueError(f"Participation outside 0-100%: {row}")
    return rows


def frame(title, bottom, left=310):
    width, height, right = 960, bottom + 74, 70
    x = lambda value: left + value / 100 * (width - left - right)
    body = text(24, 30, title, size=21, weight=500)
    for value in range(0, 101, 20):
        body += line(x(value), 60, x(value), bottom)
        body += text(x(value), bottom + 23, value, "middle")
    body += text(left, bottom + 49, "Population share (%)")
    return width, height, x, body


def active_participation():
    rows = observations("activity")
    totals = [r for r in rows if r["activity"] == "Any listed artistic activity"]
    if len(totals) != 1 or any(r["source"] != "EB25" for r in rows):
        raise ValueError("Expected an EB25 total and selected EB25 activities")
    activities = sorted((r for r in rows if r not in totals),
                        key=lambda r: float(r["participation_percent"]), reverse=True)
    display = totals + activities
    bottom = 126 + len(activities) * 44
    title = "Active artistic participation | EU27, 2025"
    width, height, x, body = frame(title, bottom)
    labels = {
        "Any listed artistic activity": "Any artistic activity",
        "Singing": "Singing",
        "Playing a musical instrument": "Playing an instrument",
        "Making films or doing photography": "Film / photography",
        "Writing poems, essays, novels, etc.": "Creative writing / essays",
    }
    for i, row in enumerate(display):
        y = 82 if i == 0 else 134 + (i - 1) * 44
        value = float(row["participation_percent"])
        body += text(294, y + 4, labels.get(row["activity"], row["activity"]), "end")
        body += line(x(0), y, x(value), y)
        body += mark(x(value), y, "#383e45" if i == 0 else "#2463ad")
        body += text(x(value) + 10, y + 4, f"{value:g}%")
    filename = FIGURES[0][1]
    write(filename, svg_doc(width, height, title, body,
          "; ".join(f'{r["activity"]}: {r["participation_percent"]}%' for r in display)))
    annotation(filename, title, [
        "Source: European Commission, Special Eurobarometer 562 (EB25), QA3, report pp. 43-44. Fieldwork: 18 February-16 March 2025; preceding-12-month recall. Total survey sample: 26,319; EU27 resident EU citizens aged 15+ under survey nationality rules. Weighted estimates, not counts.",
        "https://europa.eu/eurobarometer/surveys/detail/3364\nOriginal report copy: https://www.euskadi.eus/contenidos/informacion/keb_ber_argitalpenak_portada/eu_def/adjuntos/web01-keb_europeans_attitudes_towards_culture_SP562_report_en.pdf",
        "The separated dark total includes activities omitted from this selection. Blue points are selected activities; multiple responses overlap and must not be added. Film and photography retain a combined source category. Writing includes essays.",
        "Creation/performance is distinct from audience consumption and life impact. This is not a 2026 global ranking of the eight art categories. No uncertainty intervals were calculated. Fixed 0-100% axis.",
        "Data: ../data/participation_and_breadth.md\nSource register: ../sources/source_register.md",
    ])


def social_breadth():
    rows = observations("group")
    measures = [("Physical arts engagement", "Physical participation"),
                ("Digital arts engagement", "Digital participation")]
    groups = ["Most deprived areas, IMD decile 1", "Least deprived areas, IMD decile 10"]
    title = "Arts participation by area deprivation | England, 2024/25"
    width, height, x, body = frame(title, 230, left=245)
    description, comparisons = [], []
    for i, (measure, label) in enumerate(measures):
        values = []
        for group in groups:
            selected = [r for r in rows if r["measure"] == measure and r["group"] == group]
            if len(selected) != 1 or selected[0]["source"] != "PS25":
                raise ValueError(f"Expected one PS25 observation for {measure}, {group}")
            values.append(float(selected[0]["participation_percent"]))
        y = 96 + i * 84
        comparisons.append(f"{label}: {values[0]:g}% vs {values[1]:g}% "
                           f"({values[1] - values[0]:g} percentage points).")
        body += text(229, y + 4, label, "end")
        body += line(x(values[0]), y, x(values[1]), y, "#9da9b5", 2)
        for j, value in enumerate(values):
            # Distinct shapes remain readable in grayscale; legend is in TXT.
            body += mark(x(value), y, "#2463ad" if j == 0 else "#b96216", diamond=j == 1)
            body += text(x(value), y - 13 if j == 0 else y + 25, f"{value:g}%", "middle")
            description.append(f"{label}, {groups[j]}: {value:g}%")
    filename = FIGURES[1][1]
    write(filename, svg_doc(width, height, title, body, "; ".join(description)))
    annotation(filename, title, [
        "Source: DCMS Participation Survey 2024/25 (PS25), section 2, Figure 2.14. England, adults 16+. Fieldwork April 2024-March 2025; each respondent reports the preceding 12 months. Final survey sample: 34,378; subgroup bases are smaller. Weighted percentages within each group.",
        "https://www.gov.uk/government/statistics/participation-survey-2024-25-annual-publication/main-report-for-the-participation-survey-april-2024-to-march-2025",
        "Legend: blue filled circle = most deprived areas (IMD decile 1). Orange hollow diamond = least deprived areas (IMD decile 10). Connecting lines compare area groups; they are not time trends or uncertainty intervals.",
        " ".join(comparisons) + " Physical engagement includes attendance and personal activities such as reading. Area deprivation is not individual income. Physical and digital participation can overlap.",
        "Broad arts aggregates, not eight separate art categories or 2026 observations. The source reports significant deprivation contrasts; no new tests or uncertainty intervals were calculated here. Fixed 0-100% axis. The two selected regional observations are not plotted.",
        "Data: ../data/participation_and_breadth.md\nSource register: ../sources/source_register.md",
    ])


def build():
    OUT.mkdir(exist_ok=True)
    active_participation()
    social_breadth()
    return FIGURES


if __name__ == "__main__":
    build()
    print("Generated 2 participation SVG figures and adjacent TXT annotations")
