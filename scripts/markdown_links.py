"""Offline checks for local Markdown links and GitHub-style heading fragments.

Supports inline and reference links, ATX/setext headings and explicit HTML
anchors. Fenced code and HTML comments are excluded. This is a small checker
for the repository's Markdown conventions, not a complete CommonMark renderer.
"""

import html
from html.parser import HTMLParser
import re
import unicodedata
from urllib.parse import unquote, urlsplit


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is not None and (name == "id" or (tag == "a" and name == "name")):
                self.anchors.add(value)


def prose(text):
    """Mask comments and fenced blocks while preserving line numbers."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
    result, fence = [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            result.append("\n" if line.endswith("\n") else "")
        elif marker:
            fence = marker[1]
            result.append("\n" if line.endswith("\n") else "")
        else:
            result.append(line)
    return "".join(result)


def heading_slug(heading):
    heading = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = re.sub(r"<[^>]*>", "", heading)
    heading = html.unescape(heading).replace("`", "").replace("*", "")
    heading = re.sub(r"(?<!\w)(__?)(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", heading)
    # Preserve literal underscores and hyphens, including in code identifiers.
    heading = "".join(c for c in heading.lower()
                      if c in "_- " or unicodedata.category(c)[0] in "LNM")
    return heading.replace(" ", "-")


def markdown_anchors(text):
    text = prose(text)
    parser = AnchorParser()
    parser.feed(re.sub(r"(`+).*?\1", "", text))
    anchors, used = set(parser.anchors), set()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        atx = re.match(r"^ {0,3}#{1,6}(?:[ \t]+(.*?)|[ \t]*)$", line)
        if atx:
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", atx[1] or "")
        elif (i + 1 < len(lines) and line.strip() and not line.startswith(("    ", "\t"))
              and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", lines[i + 1])):
            heading = line.strip()
        else:
            continue
        base = heading_slug(heading)
        slug, suffix = base, 0
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        anchors.add(slug)
    return anchors


DESTINATION = r'<([^>\n]*)>|((?:[^\s()]+|\([^()]*\))+)'
INLINE_LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(?:' + DESTINATION + r')(?:\s+[\'\"][^\n]*?[\'\"])?\s*\)')
DEFINITION = re.compile(r'^ {0,3}\[([^\]]+)\]:\s*(?:' + DESTINATION + r')', re.M)


def markdown_links(text):
    text = prose(text)
    text = re.sub(r'(`+).*?\1', lambda m: " " * len(m[0]), text)
    normalize = lambda label: " ".join(label.split()).casefold()
    definitions = {normalize(m[1]): m[2] if m[2] is not None else m[3]
                   for m in DEFINITION.finditer(text)}
    for match in INLINE_LINK.finditer(text):
        yield text.count("\n", 0, match.start()) + 1, match[1] if match[1] is not None else match[2]
    # Mask inline links and definitions before finding full/collapsed/shortcut refs.
    remaining = INLINE_LINK.sub(lambda m: " " * len(m[0]), text)
    remaining = DEFINITION.sub(lambda m: " " * len(m[0]), remaining)
    for match in re.finditer(r'!?\[([^\]\n]+)\](?:\[([^\]\n]*)\])?', remaining):
        label = normalize(match[2] or match[1])
        if label in definitions:
            yield text.count("\n", 0, match.start()) + 1, definitions[label]


def check_local_links(root):
    """Return source file, line, destination and reason for each broken link."""
    errors, cache = [], {}
    for path in sorted(root.rglob("*.md")):
        for line, target in markdown_links(path.read_text(encoding="utf-8")):
            url = urlsplit(html.unescape(target))
            if url.scheme or url.netloc:
                continue
            destination = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
            reason = None
            if not destination.exists():
                reason = "file does not exist"
            elif url.fragment:
                if destination not in cache:
                    content = destination.read_text(encoding="utf-8")
                    if destination.suffix.lower() in {".md", ".markdown"}:
                        cache[destination] = markdown_anchors(content)
                    else:
                        parser = AnchorParser()
                        parser.feed(content)
                        cache[destination] = parser.anchors
                if unquote(url.fragment) not in cache[destination]:
                    reason = "anchor does not exist"
            if reason:
                errors.append((str(path.relative_to(root)), line, target, reason))
    return errors
