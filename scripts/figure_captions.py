"""Short research-style captions; detailed data stay in the source documents."""

REPORT = "https://datareportal.com/reports/digital-2027-global-overview-report"


def caption(kind, lang="en"):
    if lang not in ("en", "ru"):
        raise ValueError("Language must be en or ru")
    ru = lang == "ru"
    if kind.startswith("radar"):
        source = (
            "Источник: авторские оценки, subjective_scores_2026.md; основания: score_rationales.md. "
            "Шкала от 0 до 10 отражает субъективные суждения, а не измеренные эффекты. "
            "Разные границы учёта ограничивают сравнение; научного обоснования точных баллов влияния на жизнь нет."
            if ru else
            "Source: author ratings in subjective_scores_2026.md; rationales in score_rationales.md. "
            "The 0–10 scale represents subjective judgments, not measured effects. "
            "Mixed scope limits comparison; the exact Life impact scores have no established research basis."
        )
        key = ("Круг: числовая опора; пустой ромб: качественное обоснование. "
               "Оба типа баллов субъективны; площадь не означает общий рейтинг."
               if ru else
               "Circle: numeric anchor; hollow diamond: qualitative rationale. "
               "Both types are subjective; area does not represent an overall ranking.")
        if kind == "radar-overview":
            key += (" Оси от верхней по часовой стрелке: охват, время, частота, коммерческий масштаб, "
                    "узнаваемость, влияние на жизнь. Порядок профилей алфавитный."
                    if ru else
                    " Axes clockwise from the top: Reach, Time, Frequency, Money, Recognition, Life impact. "
                    "Profiles are ordered alphabetically.")
        if kind in ("radar-music", "radar-overview"):
            key += (" Музыка: синий профиль включает встроенный звук; оранжевый пунктир показывает "
                    "только стриминг. Это разные границы контакта, а не измеренная прибавка."
                    if ru else
                    " Music: blue includes embedded sound; orange dashed shows streaming only. "
                    "These are different exposure definitions, not a measured increase.")
        return source + "\n\n" + key + "\n"
    if kind == "growth":
        return ((
            "Источник: GWI, август 2026; EMARKETER, график 573622. Первое полугодие 2026; "
            "интернет-пользователи 16–64 лет. Данные: ../data/media_growth_h1_2026.md.\n\n"
            "Столбцы: годовое изменение времени, %; подписи Ч:ММ: текущее время в неделю. "
            "Синий означает рост, серый — снижение. Годовое сравнение следует из обсуждения авторов; "
            "базовый период на исходном графике не указан. Самоотчёты; погрешности не опубликованы, "
            "значимость различий не установлена. Категории пересекаются.\n"
        ) if ru else (
            "Source: GWI, August 2026; EMARKETER chart 573622. H1 2026; internet users aged 16–64. "
            "Data: ../data/media_growth_h1_2026.md.\n\n"
            "Bars: year-on-year time change, %; HH:MM labels: current weekly time. "
            "Blue indicates growth, grey decline. Year-on-year comparison follows the authors' discussion; "
            "the source chart does not label the base period. Self-reports; uncertainty is unpublished "
            "and differences have not been tested for significance. Categories overlap.\n"
        ))
    gwi = kind.startswith("gwi-")
    metric = kind[4:] if gwi else kind
    pages = {"reach": "38", "time": "40", "frequency": "39", "scatter": "38, 40"}[metric]
    path = "../../data/media_use_2026.md" if gwi else "../data/media_use_2026.md"
    source = (f"Источник: GWI, II квартал 2026; DataReportal, Digital 2027, стр. {pages}. "
              f"Интернет-пользователи 16+ в охваченных рынках; Россия исключена. Данные: {path}."
              if ru else
              f"Source: GWI Q2 2026; DataReportal, Digital 2027, pp. {pages}. "
              f"Internet users aged 16+ in covered markets; Russia excluded. Data: {path}.")
    metrics = {
        "reach": ("Охват: заявленное использование за неделю, % опрошенных.",
                  "Reach: reported weekly use, % of respondents."),
        "time": (("Время: минуты в неделю; подписи в часах и минутах." if gwi else
                  "Время: минуты в день, полученные делением недельного времени на 7."),
                 ("Time: minutes per week; labels in hours and minutes." if gwi else
                  "Time: minutes per day, calculated as weekly time divided by seven.")),
        "frequency": ("Частота: среднее число дней использования в неделю, а не сеансов.",
                      "Frequency: average days of use per week, not sessions."),
        "scatter": ("Оси: недельный охват, % опрошенных, и минуты в неделю. Линии соединяют смещённые подписи с точными координатами.",
                    "Axes: weekly reach, % of respondents, and minutes per week. Lines connect displaced labels to exact points."),
    }
    notes = metrics[metric][0 if ru else 1]
    notes += (" Музыка — только стриминг; ТВ-стриминг включает фильмы и другие программы. "
              "Короткие и длинные видео не выделяют ориентацию. Для отдельных фильмов, цифровых книг "
              "и изображений нет сопоставимых данных. Самоотчёты; аудитории пересекаются, пропуски не равны нулю."
              if ru else
              " Music is streaming only; TV streaming includes films and other programmes. "
              "Short/long videos do not isolate orientation. Standalone films, digital books and pictures "
              "lack comparable data. Self-reports; audiences overlap and missing values are not zeros.")
    if metric == "frequency":
        notes += ((" Игры исключены: источник даёт частоту по устройствам, а не по всем играм."
                   if gwi else " Игры: круг — мобильные устройства; пустой ромб — ПК/консоли. Группы нельзя складывать.")
                  if ru else
                  (" Games are omitted: the source reports device-specific, not all-game frequency."
                   if gwi else " Games: circle = mobile; hollow diamond = PC/console. Do not add these overlapping groups."))
    if gwi:
        notes += (" Синий: короткие видео; серый: остальные категории." if ru else
                  " Blue: short videos; grey: other categories.")
    if metric == "scatter":
        notes += (" Различия не проверены на статистическую значимость." if ru else
                  " Differences have not been tested for statistical significance.")
    return source + "\n" + REPORT + "\n\n" + notes + "\n"
