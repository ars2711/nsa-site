from flask import Flask, render_template
import os
import json
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

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
            "links": {"linkedin": "#"},
        },
        {
            "name": "Tech Director",
            "role": "Director, Engineering",
            "dept": "SMME",
            "focus": ["Systems", "AI"],
            "bio": "Shipping pipelines and infra.",
            "links": {"github": "#"},
        },
    ]

    members = load_json('team.json', fallback_team)
    normalized = []
    for m in members:
        if not isinstance(m, dict):
            continue
        focus = m.get("focus") or []
        if isinstance(focus, str):
            focus = [t.strip() for t in focus.split(',') if t.strip()]
        normalized.append({
            "name": m.get("name", "Member"),
            "role": m.get("role", ""),
            "dept": m.get("dept", ""),
            "focus": focus,
            "bio": m.get("bio", ""),
            "links": m.get("links", {}),
        })

    tracks = sorted({t for m in normalized for t in (m.get("focus") or [])})
    return render_template('team.html', members=normalized, tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)
