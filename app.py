from datetime import datetime
from flask import Flask, Response, render_template
import os
import json
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

PUBLIC_BASE_URL = "https://nust-nsa.web.app"

app = Flask(__name__)


def load_json(filename, fallback):
    path = DATA_DIR / filename
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                if data:
                    return data
        except Exception as exc:  # pragma: no cover - log and fallback
            app.logger.error("Failed to load %s: %s", filename, exc)
    return fallback

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/projects')
def projects():
    fallback_projects = [
        {
            "title": "Project Nebula",
            "summary": "Autonomous drone swarm trained on synthetic data to secure disaster zones.",
            "tags": ["CV", "Robotics", "Generative AI"],
            "status": "In flight-testing",
            "lead": "Aisha Khan",
            "link": "#",
        },
        {
            "title": "EchoSense",
            "summary": "Voice biometrics for multilingual campus security powered by federated learning.",
            "tags": ["Audio", "Security", "Research"],
            "status": "Recruiting contributors",
            "lead": "Umair Rehman",
            "link": "#",
        },
        {
            "title": "Atlas Mentor",
            "summary": "LLM-driven mentor that maps NSA member growth paths and suggests opportunities.",
            "tags": ["LLM", "Product", "Education"],
            "status": "MVP shipping Q1",
            "lead": "Sara Yousaf",
            "link": "#",
        },
    ]

    projects = load_json('projects.json', fallback_projects)
    # Normalise entries
    normalised = []
    for item in projects:
        if not isinstance(item, dict):
            continue
        tags = item.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        normalised.append(
            {
                "title": item.get("title", "Untitled Initiative"),
                "summary": item.get("summary", "Description coming soon."),
                "tags": tags,
                "status": item.get("status", "Scoping"),
                "lead": item.get("lead", "NSA Core"),
                "link": item.get("link", "#"),
            }
        )

    tag_set = {tag for proj in normalised for tag in proj["tags"]}
    sorted_tags = sorted(tag_set)

    return render_template('projects.html', projects=normalised, tags=sorted_tags)


@app.route('/team')
def team():
    fallback_team = [
        {
            "name": "Executive Lead",
            "role": "President",
            "dept": "SEECS",
            "focus": ["Leadership", "Partnerships"],
            "bio": "Driving NSA's vision and execution.",
            "email": "",
            "links": {"linkedin": "#"},
        },
        {
            "name": "Tech Director",
            "role": "Director, Engineering",
            "dept": "SMME",
            "focus": ["Systems", "AI"],
            "bio": "Shipping pipelines and infra.",
            "email": "",
            "links": {"github": "#"},
        },
    ]

    members = load_json('team.json', fallback_team)
    normalized = []
    for m in members:
        if not isinstance(m, dict):
            continue
        focus_raw = m.get("focus") or []
        if isinstance(focus_raw, str):
            focus_raw = [t.strip() for t in focus_raw.split(',') if t.strip()]
        focus = []
        for item in focus_raw:
            value = (item or "").strip()
            if value and value not in focus:
                focus.append(value)
        focus_tokens = [token.lower() for token in focus]
        links = m.get("links") or {}
        if not isinstance(links, dict):
            links = {}
        normalized.append({
            "name": (m.get("name") or "Member").strip(),
            "role": (m.get("role") or "").strip(),
            "dept": (m.get("dept") or "").strip(),
            "focus": focus,
            "focus_tokens": focus_tokens,
            "bio": (m.get("bio") or "").strip(),
            "email": (m.get("email") or "").strip(),
            "links": links,
        })

    track_candidates = {tag for member in normalized for tag in member.get("focus", [])}
    wing_order = [
        "Presidential Wing",
        "GS Wing",
        "PS Wing",
        "Treasure Wing",
        "Tech Wing",
    ]
    wing_priority = {name: index for index, name in enumerate(wing_order)}
    role_order = [
        "President",
        "Vice President",
        "Director",
        "Deputy Director",
        "Deputy Director (Tentative)",
        "Deputy",
        "Treasurer",
        "GS",
        "Tech",
        "Executive / Deputy Director",
        "Executive",
        "Member",
    ]
    role_priority = {name: index for index, name in enumerate(role_order)}

    def track_sort_key(tag: str) -> tuple:
        if tag in wing_priority:
            return (0, wing_priority[tag], tag.lower())
        if tag in role_priority:
            return (1, role_priority[tag], tag.lower())
        return (2, tag.lower())

    tracks = sorted(track_candidates, key=track_sort_key)

    structured_people = []
    for member in normalized:
        person: Dict[str, Any] = {
            "@type": "Person",
            "name": member["name"],
            "affiliation": "NUST Society of Artificial Intelligence",
            "url": f"{PUBLIC_BASE_URL}/team",
        }
        if member.get("role"):
            person["jobTitle"] = member["role"]
        if member.get("focus"):
            person["knowsAbout"] = member["focus"]
        if member.get("bio"):
            person["description"] = member["bio"]
        if member.get("email"):
            person["email"] = member["email"]
        structured_people.append(person)

    return render_template('team.html', members=normalized, tracks=tracks, structured_people=structured_people)


@app.route('/robots.txt')
def robots_txt() -> Response:
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {PUBLIC_BASE_URL}/sitemap.xml",
        ]
    )
    return Response(content, mimetype="text/plain")


@app.route('/sitemap.xml')
def sitemap_xml() -> Response:
    lastmod = datetime.utcnow().date().isoformat()
    routes = [
        ("/", "1.0"),
        ("/projects", "0.9"),
        ("/team", "0.9"),
    ]
    url_entries = []
    for path, priority in routes:
        loc = f"{PUBLIC_BASE_URL}{'' if path == '/' else path}"
        url_entries.append(
            "    <url>\n"
            f"      <loc>{loc}</loc>\n"
            f"      <lastmod>{lastmod}</lastmod>\n"
            "      <changefreq>weekly</changefreq>\n"
            f"      <priority>{priority}</priority>\n"
            "    </url>"
        )
    xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )
    return Response(xml, mimetype="application/xml")


if __name__ == '__main__':
    app.run(debug=True)
