from __future__ import annotations

import base64
import mimetypes
from functools import lru_cache
from html import escape
from pathlib import Path
from typing import List, Optional

from app.config import APP_DESCRIPTION, APP_TITLE, DOCS_URL, GITHUB_URL, REPO_ROOT
from app.partners import get_partner_organizations

LOGO_PATH = "images/logo.png"

TAGLINE = "Drug repositioning research workspace"

def _header_links_html() -> str:
    links = []
    if GITHUB_URL:
        links.append(
            f"<a class='header-link' href='{escape(GITHUB_URL, quote=True)}' target='_blank' "
            "rel='noopener noreferrer'>Project</a>"
        )
    if DOCS_URL:
        links.append(
            f"<a class='header-link' href='{escape(DOCS_URL, quote=True)}' target='_blank' "
            "rel='noopener noreferrer'>Guide</a>"
        )
    return "<div class='header-links-content'>" + "<span class='header-link-divider' aria-hidden='true'>|</span>".join(links) + "</div>" if links else ""


HEADER_LINKS_HTML = _header_links_html()


@lru_cache(maxsize=32)
def inline_image_src(path_value: str) -> Optional[str]:
    '''`path_value` as a data URI, or None when the file is missing.

    Parameters:
    ---------
    path_value (str): the image to inline.

    Returns:
    ----------
    src (str): the file as a data URI, or None when it is missing — a strict CSP means nothing loads from disk at render time.
    '''

    path = Path(path_value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists():
        return None
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    mime, _ = mimetypes.guess_type(str(path))
    return f"data:{mime or 'image/png'};base64,{data}"


def logo_html() -> str:
    source = inline_image_src(LOGO_PATH)
    if not source:
        return ""
    return f"<img src='{source}' alt='{escape(APP_TITLE, quote=True)} logo' class='app-logo-img' />"


def title_html() -> str:
    return (
        f"<div class='app-title-text'>{escape(APP_TITLE)}</div>"
        f"<div class='app-tagline'>{escape(TAGLINE)}</div>"
    )


def intro_markdown() -> str:
    return APP_DESCRIPTION


def partner_logos_html() -> str:
    cards: List[str] = []
    for organization in get_partner_organizations():
        source = inline_image_src(organization["logo"])
        url = organization.get("url")
        if not source or not url:
            continue
        name = organization.get("name") or "Partner"
        extra = " partner-logo-card--xl" if (organization.get("size") or "").lower() == "xl" else ""
        cards.append(
            (
                "<a class='partner-logo-card{extra}' href='{href}' target='_blank' "
                "rel='noopener noreferrer' title='{title}'>"
                "<img src='{src}' alt='{alt}' /></a>"
            ).format(
                extra=extra,
                href=escape(url, quote=True),
                title=escape(name, quote=True),
                src=escape(source, quote=True),
                alt=escape(f"{name} logo", quote=True),
            )
        )
    if not cards:
        return ""
    return (
        "<div class='partner-slider' data-partner-slider='1'>"
        "<div class='partner-slider__viewport'>"
        f"<div class='partner-slider__track'>{''.join(cards)}</div>"
        "</div>"
        "<div class='partner-slider__dots' role='tablist' "
        "aria-label='Partner carousel controls'></div>"
        "</div>"
    )


__all__ = [
    "HEADER_LINKS_HTML",
    "LOGO_PATH",
    "TAGLINE",
    "inline_image_src",
    "intro_markdown",
    "logo_html",
    "partner_logos_html",
    "title_html",
]
