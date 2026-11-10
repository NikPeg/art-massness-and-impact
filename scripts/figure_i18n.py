"""Localize rendered text only; never alter chart coordinates or source tables."""

import argparse
import html
import json
from functools import lru_cache
from pathlib import Path
import re

PAIRS = json.loads(Path(__file__).with_name("figure_translations.json").read_text(encoding="utf-8"))


def cli_language():
    parser = argparse.ArgumentParser(description="Generate charts in English or Russian")
    parser.add_argument("--lang", choices=("en", "ru"), default="en")
    return parser.parse_args().lang


def localized_path(path, lang):
    path = Path(path)
    if lang not in ("en", "ru"):
        raise ValueError(f"Unsupported language: {lang}")
    if lang == "ru" and not path.stem.endswith("-ru"):
        return path.with_name(path.stem + "-ru" + path.suffix)
    return path


@lru_cache(maxsize=2)
def _catalog(lang):
    mapping = dict(PAIRS if lang == "ru" else ((ru, en) for en, ru in PAIRS))
    pattern = re.compile("|".join(
        (r"(?<!\w)" if key[0].isalnum() else "") + re.escape(key)
        + (r"(?!\w)" if key[-1].isalnum() else "")
        for key in sorted(mapping, key=len, reverse=True)))
    return mapping, pattern


def translate(value, lang, source_lang="en"):
    if lang not in ("en", "ru") or source_lang not in ("en", "ru"):
        raise ValueError("Language must be en or ru")
    if lang == source_lang:
        return value
    mapping, pattern = _catalog(lang)
    value = pattern.sub(lambda match: mapping[match.group()], value)
    # Decimal punctuation belongs to displayed numbers, not SVG attributes or URLs.
    if re.fullmatch(r"[+−-]?\d+[.,]\d+(?:%| мин)?", value):
        value = value.replace(".", ",") if lang == "ru" else value.replace(",", ".")
    return value


def save(path, content, lang="en", source_lang="en"):
    """Write one language variant, with matching language-specific asset links."""
    path = Path(path)
    if path.suffix in (".svg", ".html"):
        # Keep markup, styles and numeric geometry byte-for-byte intact.
        parts = re.split(r"(<[^>]+>)", content)
        in_style = False
        for i, part in enumerate(parts):
            if part.startswith("<"):
                if part.startswith("<style"):
                    in_style = True
                elif part.startswith("</style"):
                    in_style = False
                part = re.sub(r'((?:xml:)?lang=")[^"]*(")', rf'\g<1>{lang}\2', part)
                if part.startswith("<svg") and "xml:lang=" not in part:
                    part = part.replace("<svg ", f'<svg xml:lang="{lang}" ', 1)
                part = re.sub(r'(alt=")([^"]*)(")', lambda m: m[1] + html.escape(
                    translate(html.unescape(m[2]), lang, source_lang), quote=True) + m[3], part)
                def link(match):
                    target = match[2]
                    if not re.match(r"(?:https?:|#)", target) and (
                            Path(target).suffix in (".svg", ".txt") or Path(target).name == "index.html"):
                        target = localized_path(target, lang).as_posix()
                    return match[1] + target + match[3]
                part = re.sub(r'((?:src|href)=")([^"]*)(")', link, part)
                parts[i] = part
            elif not in_style:
                parts[i] = html.escape(translate(html.unescape(part), lang, source_lang), quote=False)
        content = "".join(parts)
    else:
        content = translate(content, lang, source_lang)
    target = localized_path(path, lang)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
