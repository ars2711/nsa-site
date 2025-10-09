"""Generate a static version of the Flask site for Firebase Hosting."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable, Union

from flask import render_template

from app import app, projects as projects_view, team as team_view

ROOT = Path(__file__).parent.resolve()
OUTPUT_DIR = ROOT / "public"
STATIC_DIR = ROOT / "static"


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
        pages = {
            "index.html": ("/", lambda: render_template("index.html")),
            "projects/index.html": ("/projects", projects_view),
            "team/index.html": ("/team", team_view),
        }
        for relative_path, (request_path, handler) in pages.items():
            with app.test_request_context(request_path):
                html = render_route(handler)
            write_page(relative_path, html)

    # Copy root-level favicon for convenience.
    favicon_source = STATIC_DIR / "favicon.svg"
    if favicon_source.exists():
        shutil.copy2(favicon_source, OUTPUT_DIR / "favicon.svg")


if __name__ == "__main__":
    main()
