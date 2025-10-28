"""Generate a static version of the Flask site for Firebase Hosting."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

from flask import render_template

from app import (
    PUBLIC_BASE_URL,
    app,
    index as index_view,
    projects as projects_view,
    team as team_view,
)

ROOT = Path(__file__).parent.resolve()
OUTPUT_DIR = ROOT / "public"
STATIC_DIR = ROOT / "static"
BASE_URL = PUBLIC_BASE_URL


def ensure_empty_directory(path: Path) -> None:
    """Remove an existing directory tree and recreate an empty folder."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_page(relative_path: str, content: str) -> None:
    """Write rendered HTML to the public folder."""
    destination = OUTPUT_DIR / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def render_route(handler: Callable[[], Union[str, bytes]]) -> str:
    """Execute a Flask view handler and coerce the response to a string."""
    rendered = handler()
    if hasattr(rendered, "get_data"):
        return rendered.get_data(as_text=True)
    if isinstance(rendered, bytes):
        return rendered.decode("utf-8")
    return str(rendered)


def main() -> None:
    ensure_empty_directory(OUTPUT_DIR)

    # Copy static assets (CSS, JS, media) directly.
    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")

    # Render dynamic templates into static HTML pages.
    with app.app_context():
        pages: Dict[str, Tuple[str, Callable[[], Union[str, bytes]]]] = {
            "index.html": ("/", index_view),
            "projects/index.html": ("/projects", projects_view),
            "team/index.html": ("/team", team_view),
        }
        for relative_path, (request_path, handler) in pages.items():
            with app.test_request_context(request_path):
                html = render_route(handler)
            write_page(relative_path, html)

    # Generate sitemap.xml
    lastmod = datetime.utcnow().date().isoformat()
    sitemap_entries: List[str] = []
    sitemap_targets = [
        ("index.html", "/", "1.0"),
        ("projects/index.html", "/projects", "0.9"),
        ("team/index.html", "/team", "0.9"),
    ]
    for _, path, priority in sitemap_targets:
        loc = f"{BASE_URL}{'' if path == '/' else path}"
        sitemap_entries.append(
            "    <url>\n"
            f"      <loc>{loc}</loc>\n"
            f"      <lastmod>{lastmod}</lastmod>\n"
            "      <changefreq>weekly</changefreq>\n"
            f"      <priority>{priority}</priority>\n"
            "    </url>"
        )

    sitemap_content = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        + "\n".join(sitemap_entries)
        + "\n</urlset>\n"
    )
    write_page("sitemap.xml", sitemap_content)

    # Generate robots.txt
    robots_content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )
    write_page("robots.txt", robots_content)

    # Copy root-level favicon for convenience.
    favicon_source = STATIC_DIR / "favicon.svg"
    if favicon_source.exists():
        shutil.copy2(favicon_source, OUTPUT_DIR / "favicon.svg")


if __name__ == "__main__":
    main()
