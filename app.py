from collections import Counter
from datetime import datetime
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, Response, render_template, url_for

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

PUBLIC_BASE_URL = "https://nust-nsa.web.app"

app = Flask(__name__)


from copy import deepcopy
from collections import Counter
from datetime import datetime
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from flask import Flask, Response, render_template, url_for

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

PUBLIC_BASE_URL = "https://nust-nsa.web.app"

app = Flask(__name__)


PROJECTS_FALLBACK = [
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

TEAM_FALLBACK = [
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

HOME_FALLBACK = {
    "timeline": [
        {
            "title": "Rolling Recruitment Windows",
            "period": "All year",
            "description": "Submit your profile and we will route it to the right wing in under 72 hours.",
            "icon": "bi-rocket-takeoff",
            "cta": {
                "label": "Start Application",
                "url": "https://forms.gle/d8rLMELNKLbSxPNc7",
            },
        },
        {
            "title": "Squad Conversations",
            "period": "Weekly cohorts",
            "description": "Meet wing leads for focused chats about your skills, goals, and preferred teams.",
            "icon": "bi-people",
            "cta": None,
        },
        {
            "title": "Shadow Sprints",
            "period": "First month",
            "description": "Join active missions with mentors so you can learn the operating rhythm on the job.",
            "icon": "bi-lightning-charge",
            "cta": None,
        },
        {
            "title": "Launch Reviews",
            "period": "Quarterly",
            "description": "Showcase progress, ship demos, and plan the next wave of projects with the core council.",
            "icon": "bi-bar-chart",
        },
    ],
    "impact": [
        {
            "value": 78,
            "title": "Members publish research",
            "description": "More than three quarters of active researchers submit work to journals, conferences, or tech blogs every season.",
        },
        {
            "value": 62,
            "title": "Ship production code",
            "description": "Engineers push code that reaches real users inside and outside the campus within their first two quarters.",
        },
        {
            "value": 48,
            "title": "Lead major events",
            "description": "Event specialists own flagship conferences, hackathons, and workshops with cross-campus partners.",
        },
    ],
    "faq": [
        {
            "title": "Recruitment & Eligibility",
            "icon": "bi-person-check",
            "questions": [
                {
                    "question": "When does recruitment close?",
                    "answer": "NSA operates on rolling cohorts now. Submit whenever you're ready and expect an update from the council within 72 hours.",
                },
                {
                    "question": "Do I need to be a CS student to join NSA?",
                    "answer": "NSA welcomes students from every NUST school. Diverse disciplines strengthen our AI work, so engineering, business, design, and biosciences students are encouraged to apply.",
                },
                {
                    "question": "Can first-year students participate?",
                    "answer": "Yes. We actively recruit freshmen and sophomores so they can learn, contribute, and grow into leadership roles throughout their time at NUST.",
                },
            ],
        },
        {
            "title": "Life Inside NSA",
            "icon": "bi-lightning-charge",
            "questions": [
                {
                    "question": "What's the selection process?",
                    "answer": "Submit the Google Form, pass a skills and motivation screening, complete a 15-20 minute interview, and receive results within 48 hours of the conversation.",
                },
                {
                    "question": "What do NSA members work on?",
                    "answer": "Members ship AI products, run research experiments, craft design systems, and lead operations for large-scale events and partnerships across NUST.",
                },
            ],
        },
    ],
    "directorates": [
        {
            "name": "Engineering Directorate",
            "icon": "bi-cpu",
            "description": "Transforms ambitious briefs into resilient products, services, and tools.",
            "roles": ["Web and App Development", "ML Engineering", "DevOps and Infrastructure"],
        },
        {
            "name": "Research Directorate",
            "icon": "bi-flask",
            "description": "Runs experimentation pipelines, model evaluations, and technical write-ups.",
            "roles": ["NLP and LLMs", "ML Research", "Academic Publications"],
        },
        {
            "name": "Design Directorate",
            "icon": "bi-palette2",
            "description": "Crafts the visual language for every product, deck, and experience.",
            "roles": ["Product Design", "Brand Identity", "Creative Direction"],
        },
        {
            "name": "Marketing Directorate",
            "icon": "bi-megaphone",
            "description": "Amplifies missions, leads campaigns, and nurtures community stories.",
            "roles": ["Growth Strategy", "Content Planning", "Community Programs"],
        },
        {
            "name": "Operations Directorate",
            "icon": "bi-diagram-3",
            "description": "Keeps logistics, security, and event execution aligned with the mission clock.",
            "roles": ["Security", "Logistics", "Admin Operations"],
        },
        {
            "name": "Strategy Directorate",
            "icon": "bi-compass",
            "description": "Aligns resources, partnerships, and long-term roadmaps for every wing.",
            "roles": ["Strategic Planning", "Sponsorships", "Leadership Coordination"],
        },
    ],
    "portfolios": [
        {
            "name": "Team Human Resources",
            "icon": "bi-person-hearts",
            "description": "Builds culture, onboarding, and member growth journeys.",
        },
        {
            "name": "Team Security and Logistics",
            "icon": "bi-shield-lock",
            "description": "Protects venues, manages access, and aligns on-ground execution.",
        },
        {
            "name": "Team Event Management",
            "icon": "bi-calendar3",
            "description": "Designs unforgettable experiences from brief to breakdown.",
        },
        {
            "name": "Team Admin Events",
            "icon": "bi-clipboard-data",
            "description": "Owns permissions, space bookings, and partner coordination.",
        },
        {
            "name": "Team Liaison",
            "icon": "bi-diagram-2",
            "description": "Connects NSA squads with external mentors, startups, and partners.",
        },
        {
            "name": "Team Publications",
            "icon": "bi-journal-text",
            "description": "Documents wins, research, and member spotlights for the network.",
        },
        {
            "name": "Team Graphics",
            "icon": "bi-brush",
            "description": "Turns complex ideas into expressive visuals and motion.",
        },
        {
            "name": "Team Media",
            "icon": "bi-camera-reels",
            "description": "Captures moments, produces recaps, and runs post-event storytelling.",
        },
        {
            "name": "Team SMM",
            "icon": "bi-hash",
            "description": "Curates social conversations and sparks interest across channels.",
        },
        {
            "name": "Team ER and Sponsorship",
            "icon": "bi-handshake",
            "description": "Unlocks resources and long-term alliances for missions.",
        },
        {
            "name": "Team Finance",
            "icon": "bi-cash-stack",
            "description": "Balances budgets, reimbursements, and transparent reporting.",
        },
        {
            "name": "Team Decor",
            "icon": "bi-stars",
            "description": "Shapes immersive atmospheres that match the energy of each launch.",
        },
        {
            "name": "Team Marketing",
            "icon": "bi-broadcast",
            "description": "Keeps the NSA story consistent across every touchpoint.",
        },
        {
            "name": "Unit Software Development",
            "icon": "bi-code-slash",
            "description": "Ships full-stack products, internal tools, and integrations.",
        },
        {
            "name": "Unit Computer Vision",
            "icon": "bi-eye",
            "description": "Builds perception systems, pipelines, and applied CV demos.",
        },
        {
            "name": "Unit Deep Learning",
            "icon": "bi-cpu-fill",
            "description": "Runs model training, optimization, and evaluators.",
        },
        {
            "name": "Unit Enthusiasts",
            "icon": "bi-lightbulb",
            "description": "Hosts discovery circles, reading groups, and labs for new members.",
        },
        {
            "name": "Unit Gen AI",
            "icon": "bi-robot",
            "description": "Prototype agents, assistants, and content intelligence systems.",
        },
        {
            "name": "Unit R and D",
            "icon": "bi-graph-up",
            "description": "Maps long-term AI investments, grants, and research collaborations.",
        },
    ],
    "social": [
        {
            "name": "Instagram",
            "handle": "@nsa.nust",
            "url": "https://www.instagram.com/nsa.nust/",
            "icon": "bi-instagram",
        },
        {
            "name": "WhatsApp Community",
            "handle": "Join the HQ channel",
            "url": "https://chat.whatsapp.com/BOCZkgf8vYb5fhpXW8o7Vh",
            "icon": "bi-whatsapp",
        },
        {
            "name": "Email",
            "handle": "hello@nsa.pk",
            "url": "mailto:mafzal.bscs24seecs@seecs.edu.pk",
            "icon": "bi-envelope",
        },
        {
            "name": "GitHub Org",
            "handle": "github.com/nsa-nust",
            "url": "https://github.com/nsa-nust",
            "icon": "bi-github",
        },
        {
            "name": "Twitter",
            "handle": "@nsa_nust",
            "url": "https://twitter.com/nsa_nust",
            "icon": "bi-twitter-x",
        },
    ],
    "social_widgets": {
        "instagram_embed": "https://www.instagram.com/p/Cx0mSbmJ0_k/embed/",
        "instagram_profile": "https://www.instagram.com/nsa.nust/",
        "whatsapp_link": "https://chat.whatsapp.com/BOCZkgf8vYb5fhpXW8o7Vh",
        "whatsapp_qr": "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://chat.whatsapp.com/BOCZkgf8vYb5fhpXW8o7Vh",
        "email_address": "mafzal.bscs24seecs@seecs.edu.pk",
        "email_note": "Your note arrives directly in the NSA inbox. Expect a reply within 24 hours.",
        "github_org": "https://github.com/nsa-nust",
        "github_note": "Open-source drops are staged. Watch this space for launch repos.",
        "twitter_profile": "https://twitter.com/nsa_nust",
        "twitter_note": "Follow for live event coverage, callouts, and member spotlights.",
    },
}

AI_FALLBACK = {
    "battles": [
        {
            "name": "Build vs Break",
            "brief": "Two squads race. Builders ship a working demo in 90 minutes while breakers stress-test and score stability.",
            "focus": "Product engineering",
        },
        {
            "name": "Vision Gauntlet",
            "brief": "Computer vision teams classify obscure datasets under latency limits. Highest accuracy with real-time feedback wins.",
            "focus": "Computer vision",
        },
        {
            "name": "Prompt Arena",
            "brief": "Gen AI crews craft prompts to solve real campus problems. Judges score creativity, safety, and outputs.",
            "focus": "Generative AI",
        },
    ],
    "challenges": [
        {
            "title": "Agent in a Day",
            "duration": "6 hours",
            "description": "Spin up an assistant that books venues, notifies squads, and posts updates to Discord using existing APIs.",
            "tags": ["Automation", "Integrations", "LLMs"],
        },
        {
            "title": "Research Sprint",
            "duration": "48 hours",
            "description": "Reproduce a recent conference paper with NSA data and present the deltas to the research guild.",
            "tags": ["Research", "Reproducibility", "Evaluation"],
        },
        {
            "title": "Responsible Release",
            "duration": "24 hours",
            "description": "Audit an AI feature for bias and privacy, then publish a mitigation playbook for ship-ready teams.",
            "tags": ["Policy", "Safety", "DX"],
        },
    ],
    "faqs": [
        {
            "question": "How do AI battles work?",
            "answer": "Each battle spans a single evening. Teams form on the spot, receive the mission brief, and deliver a demo or report before midnight.",
        },
        {
            "question": "Can newcomers join AI challenges?",
            "answer": "Yes. We pair first-timers with mentors, publish starter kits, and score progress as much as final output.",
        },
        {
            "question": "Where can I find datasets?",
            "answer": "The NSA data guild curates anonymized datasets in our GitHub organization along with documentation and baselines.",
        },
    ],
    "resources": [
        {
            "title": "NSA Model Playground",
            "url": "https://github.com/nsa-nust/playground",
            "description": "Shared notebooks for quick experiments, deployed demos, and inference recipes.",
        },
        {
            "title": "AI Safety Checklist",
            "url": "https://github.com/nsa-nust/ai-safety",
            "description": "Step-by-step release checklist covering privacy, fairness, and monitoring.",
        },
        {
            "title": "Battle Archive",
            "url": "https://github.com/nsa-nust/ai-battles",
            "description": "Past challenges, winning strategies, and scoring sheets.",
        },
    ],
}

TEAM_STRUCTURE_SPEC = [
    {
        "name": "Presidential Wing",
        "aliases": ["presidential wing", "presidential", "obs"],
        "lead": "Presidential Council",
        "lead_note": "Wing oversight by the presidential council.",
        "default_subteam": "Council Projects",
        "subteams": [
            {
                "name": "Team Human Resources",
                "aliases": ["team human resources", "human resources", "hr"],
            }
        ],
    },
    {
        "name": "General Secretary Wing",
        "aliases": ["general secretary wing", "gs wing", "gs"],
        "lead": "Reem Saleha",
        "lead_note": "Wing lead: Reem Saleha",
        "default_subteam": "General Projects",
        "subteams": [
            {
                "name": "Team Security and Logistics",
                "aliases": ["security", "logistics", "security and logistics"],
            },
            {
                "name": "Team Event Management",
                "aliases": ["event management"],
            },
            {
                "name": "Team Admin Events",
                "aliases": ["admin events"],
            },
            {
                "name": "Team Liaison",
                "aliases": ["liaison"],
            },
        ],
    },
    {
        "name": "Press Wing",
        "aliases": ["press wing", "ps wing", "press", "ps"],
        "lead": "Areeba Shakeel",
        "lead_note": "Wing lead: Areeba Shakeel",
        "default_subteam": "Press Projects",
        "subteams": [
            {
                "name": "Team Publications",
                "aliases": ["publications", "team publications"],
            },
            {
                "name": "Team Graphics",
                "aliases": ["graphics"],
            },
            {
                "name": "Team Media",
                "aliases": ["media"],
            },
            {
                "name": "Team SMM",
                "aliases": ["smm", "social media"],
            },
        ],
    },
    {
        "name": "Treasure Wing",
        "aliases": ["treasure wing", "treasury", "finance wing"],
        "lead": "Hafsa Faizan",
        "lead_note": "Wing lead: Hafsa Faizan",
        "default_subteam": "Finance Projects",
        "subteams": [
            {
                "name": "Team ER and Sponsorship",
                "aliases": ["er and sponsorship", "sponsorship"],
            },
            {
                "name": "Team Finance",
                "aliases": ["finance"],
            },
            {
                "name": "Team Decor",
                "aliases": ["decor"],
            },
            {
                "name": "Team Marketing",
                "aliases": ["marketing"],
            },
        ],
    },
    {
        "name": "Tech Wing",
        "aliases": ["tech wing", "tech"],
        "lead": "Ali Zain",
        "lead_note": "Wing lead: Ali Zain",
        "default_subteam": "Tech Projects",
        "subteams": [
            {
                "name": "Unit Software Development",
                "aliases": ["software development", "web and app development"],
            },
            {
                "name": "Unit Computer Vision",
                "aliases": ["computer vision", "cv", "executive dl/cv"],
            },
            {
                "name": "Unit Deep Learning",
                "aliases": ["deep learning", "ml/dl", "director ml/dl"],
            },
            {
                "name": "Unit Enthusiasts",
                "aliases": ["tech enthusiasts", "enthusiasts"],
            },
            {
                "name": "Unit Gen AI",
                "aliases": ["gen ai", "genai", "executive genai"],
            },
            {
                "name": "Unit R and D",
                "aliases": ["r and d", "research", "executive ai"],
            },
        ],
    },
]

ROLE_ORDER = [
    "President",
    "General Secretary",
    "Director",
    "Director, Engineering",
    "Director ML/DL",
    "Treasurer",
    "Deputy Director",
    "Deputy Director (Tentative)",
    "Deputy",
    "Executive",
    "Executive AI",
    "Executive DL/CV",
    "Executive GenAI",
    "Member",
    "GS",
    "Tech",
]

ROLE_PRIORITY = {role: index for index, role in enumerate(ROLE_ORDER)}


def load_json(filename: str, fallback: Any) -> Any:
    path = DATA_DIR / filename
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                if data:
                    return data
        except Exception as exc:  # pragma: no cover - log and fallback
            app.logger.error("Failed to load %s: %s", filename, exc)
    return deepcopy(fallback)


def normalise_list(raw: Any) -> List[str]:
    if isinstance(raw, list):
        items: Iterable[Any] = raw
    elif isinstance(raw, str):
        items = re.split(r"[,\n]", raw)
    else:
        items = []
    seen: List[str] = []
    for item in items:
        if not isinstance(item, str):
            continue
        value = item.strip()
        if value and value not in seen:
            seen.append(value)
    return seen


def normalise_links(raw: Any) -> Dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    cleaned: Dict[str, str] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, str):
            continue
        key_clean = key.strip()
        value_clean = value.strip()
        if key_clean and value_clean:
            cleaned[key_clean.lower()] = value_clean
    return cleaned


SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    base = value.lower()
    base = SLUG_PATTERN.sub("-", base)
    return base.strip("-") or "item"


def build_team_indexes() -> Tuple[Dict[str, str], Dict[str, Tuple[str, str]], Dict[str, str], Dict[str, Dict[str, Any]]]:
    wing_alias_index: Dict[str, str] = {}
    subteam_alias_index: Dict[str, Tuple[str, str]] = {}
    wing_defaults: Dict[str, str] = {}
    wing_lookup: Dict[str, Dict[str, Any]] = {}
    for position, wing in enumerate(TEAM_STRUCTURE_SPEC):
        canonical = wing["name"]
        wing_lookup[canonical] = {**wing, "order": position}
        wing_alias_index[canonical.lower()] = canonical
        for alias in wing.get("aliases", []):
            wing_alias_index[alias.lower()] = canonical
        if wing.get("default_subteam"):
            wing_defaults[canonical] = wing["default_subteam"]
        for sub_pos, subteam in enumerate(wing.get("subteams", [])):
            sub_canonical = subteam["name"]
            subteam_alias_index[sub_canonical.lower()] = (canonical, sub_canonical)
            for alias in subteam.get("aliases", []):
                subteam_alias_index[alias.lower()] = (canonical, sub_canonical)
            subteam_alias_index.setdefault(sub_canonical.lower(), (canonical, sub_canonical))
    return wing_alias_index, subteam_alias_index, wing_defaults, wing_lookup


WING_ALIAS_INDEX, SUBTEAM_ALIAS_INDEX, WING_DEFAULT_SUBTEAM, WING_LOOKUP = build_team_indexes()
WING_ORDER = {spec["name"]: index for index, spec in enumerate(TEAM_STRUCTURE_SPEC)}
SUBTEAM_ORDER: Dict[str, int] = {}
for wing_index, wing_spec in enumerate(TEAM_STRUCTURE_SPEC):
    for sub_index, sub_spec in enumerate(wing_spec.get("subteams", [])):
        SUBTEAM_ORDER[sub_spec["name"]] = (wing_index * 100) + sub_index


def resolve_focus(raw_focus: Any) -> Tuple[List[str], List[str]]:
    focus_labels: List[str] = []
    tokens: List[str] = []
    for item in normalise_list(raw_focus):
        key = item.lower()
        canonical: Optional[str] = None
        if key in SUBTEAM_ALIAS_INDEX:
            _, canonical = SUBTEAM_ALIAS_INDEX[key]
        elif key in WING_ALIAS_INDEX:
            canonical = WING_ALIAS_INDEX[key]
        else:
            canonical = item
        if canonical and canonical not in focus_labels:
            focus_labels.append(canonical)
            tokens.append(canonical.lower())
    return focus_labels, tokens


def classify_member(focus: List[str]) -> Tuple[Optional[str], Optional[str]]:
    wing_name: Optional[str] = None
    subteam_name: Optional[str] = None
    for label in focus:
        key = label.lower()
        if key in SUBTEAM_ALIAS_INDEX:
            wing_name, subteam_name = SUBTEAM_ALIAS_INDEX[key]
            break
    if not wing_name:
        for label in focus:
            key = label.lower()
            if key in WING_ALIAS_INDEX:
                wing_name = WING_ALIAS_INDEX[key]
                break
    if wing_name and not subteam_name:
        subteam_name = WING_DEFAULT_SUBTEAM.get(wing_name)
    return wing_name, subteam_name


def enrich_member(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not isinstance(entry, dict):
        return None
    name = (entry.get("name") or "NSA Member").strip()
    role = (entry.get("role") or "Member").strip() or "Member"
    dept = (entry.get("dept") or "").strip()
    focus, focus_tokens = resolve_focus(entry.get("focus"))
    wing_name, subteam_name = classify_member(focus)
    links = normalise_links(entry.get("links"))
    bio = (entry.get("bio") or "").strip()
    email = (entry.get("email") or "").strip()
    role_priority = ROLE_PRIORITY.get(role, len(ROLE_PRIORITY) + 1)
    wing_order = WING_ORDER.get(wing_name, len(WING_ORDER) + 1)
    return {
        "name": name,
        "role": role,
        "dept": dept,
        "focus": focus,
        "focus_tokens": focus_tokens,
        "wing": wing_name,
        "subteam": subteam_name,
        "bio": bio,
        "email": email,
        "links": links,
        "role_priority": role_priority,
        "wing_priority": wing_order,
        "slug": slugify(name),
    }


def normalise_team_members(raw: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw, list):
        raw = TEAM_FALLBACK
    members: List[Dict[str, Any]] = []
    for item in raw:
        enriched = enrich_member(item)
        if enriched:
            members.append(enriched)
    members.sort(
        key=lambda member: (
            member["wing_priority"],
            member["role_priority"],
            member["name"].lower(),
        )
    )
    return members


def group_team_members(members: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for wing in TEAM_STRUCTURE_SPEC:
        grouped[wing["name"]] = {
            "meta": wing,
            "members": [],
            "subteams": {sub["name"]: [] for sub in wing.get("subteams", [])},
        }
    unassigned = {
        "meta": {
            "name": "Unassigned",
            "lead": None,
            "lead_note": "Members awaiting wing assignment.",
            "default_subteam": None,
        },
        "members": [],
        "subteams": {},
    }
    for member in members:
        wing_name = member.get("wing")
        target = grouped.get(wing_name) if wing_name in grouped else unassigned
        target["members"].append(member)
        sub_name = member.get("subteam")
        if sub_name:
            target["subteams"].setdefault(sub_name, []).append(member)
    result: List[Dict[str, Any]] = []
    for wing in TEAM_STRUCTURE_SPEC:
        data = grouped[wing["name"]]
        members_sorted = sorted(
            data["members"],
            key=lambda m: (m["role_priority"], m["name"].lower()),
        )
        unassigned_members = [member for member in members_sorted if not member.get("subteam")]
        subteams_payload: List[Dict[str, Any]] = []
        for subteam in wing.get("subteams", []):
            entries = data["subteams"].get(subteam["name"], [])
            if not entries:
                continue
            subteams_payload.append(
                {
                    "name": subteam["name"],
                    "members": sorted(
                        entries,
                        key=lambda m: (m["role_priority"], m["name"].lower()),
                    ),
                    "slug": slugify(subteam["name"]),
                }
            )
        result.append(
            {
                "name": wing["name"],
                "lead": wing.get("lead"),
                "lead_note": wing.get("lead_note"),
                "default_subteam": wing.get("default_subteam"),
                "members": members_sorted,
                "subteams": subteams_payload,
                "unassigned": unassigned_members,
                "slug": slugify(wing["name"]),
            }
        )
    if unassigned["members"]:
        result.append(
            {
                "name": "Unassigned",
                "lead": None,
                "lead_note": unassigned["meta"]["lead_note"],
                "default_subteam": None,
                "members": sorted(
                    unassigned["members"],
                    key=lambda m: (m["role_priority"], m["name"].lower()),
                ),
                "subteams": [],
                "slug": "unassigned",
            }
        )
    return result


def build_track_filters(members: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counter: Counter[str] = Counter()
    for member in members:
        for label in member.get("focus", []):
            counter[label] += 1
    filters: List[Dict[str, Any]] = []
    for label, count in counter.items():
        filters.append({
            "label": label,
            "count": count,
            "slug": slugify(label),
        })

    def sort_key(item: Dict[str, Any]) -> Tuple[int, int, str]:
        label = item["label"]
        if label in WING_ORDER:
            return (0, WING_ORDER[label], label.lower())
        if label in SUBTEAM_ORDER:
            return (1, SUBTEAM_ORDER[label], label.lower())
        return (2, len(label), label.lower())

    filters.sort(key=sort_key)
    return filters


def build_structured_people(members: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    structured: List[Dict[str, Any]] = []
    for member in members:
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
        structured.append(person)
    return structured


def load_team_data() -> Dict[str, Any]:
    members = normalise_team_members(load_json("team.json", TEAM_FALLBACK))
    wings = group_team_members(members)
    filters = build_track_filters(members)
    structured_people = build_structured_people(members)
    return {
        "members": members,
        "wings": wings,
        "filters": filters,
        "structured_people": structured_people,
    }


def load_projects_data() -> List[Dict[str, Any]]:
    raw = load_json("projects.json", PROJECTS_FALLBACK)
    if not isinstance(raw, list):
        raw = PROJECTS_FALLBACK
    projects: List[Dict[str, Any]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        tags = normalise_list(entry.get("tags"))
        projects.append(
            {
                "title": (entry.get("title") or "Untitled Initiative").strip(),
                "summary": (entry.get("summary") or "Description coming soon.").strip(),
                "tags": tags,
                "status": (entry.get("status") or "Scoping").strip(),
                "lead": (entry.get("lead") or "NSA Core").strip(),
                "link": (entry.get("link") or "#").strip() or "#",
                "slug": slugify(entry.get("title") or "project"),
            }
        )
    projects.sort(key=lambda item: item["title"].lower())
    return projects


def load_home_data() -> Dict[str, Any]:
    raw = load_json("home.json", HOME_FALLBACK)
    if not isinstance(raw, dict):
        raw = deepcopy(HOME_FALLBACK)
    raw.setdefault("timeline", [])
    raw.setdefault("impact", [])
    raw.setdefault("faq", [])
    raw.setdefault("directorates", [])
    raw.setdefault("portfolios", [])
    raw.setdefault("social", [])
    raw.setdefault("social_widgets", {})
    if not isinstance(raw["social_widgets"], dict):
        raw["social_widgets"] = {}
    return raw


def load_ai_data() -> Dict[str, Any]:
    raw = load_json("ai.json", AI_FALLBACK)
    if not isinstance(raw, dict):
        raw = deepcopy(AI_FALLBACK)
    raw.setdefault("battles", [])
    raw.setdefault("challenges", [])
    raw.setdefault("faqs", [])
    raw.setdefault("resources", [])
    return raw


EVENT_SUBTEAMS = {
    "Team Event Management",
    "Team Admin Events",
    "Team Decor",
    "Team Liaison",
    "Team Security and Logistics",
}

EVENT_FOCUS_TOKENS = {label.lower() for label in EVENT_SUBTEAMS}

RESEARCH_SUBTEAMS = {
    "Unit R and D",
    "Unit Deep Learning",
    "Unit Gen AI",
    "Unit Computer Vision",
    "Research Directorate",
}

RESEARCH_FOCUS_TOKENS = {
    "unit r and d",
    "unit deep learning",
    "unit gen ai",
    "unit computer vision",
    "executive ai",
    "executive dl/cv",
    "executive genai",
    "director ml/dl",
    "research",
}

HOME_STATS_LAYOUT = [
    {
        "key": "active_members",
        "label": "Active Members",
        "icon": "bi-people",
        "description": "Builders, researchers, and operators currently engaged across wings.",
        "endpoint": "team",
        "fragment": "team-directory",
    },
    {
        "key": "active_projects",
        "label": "Active Projects",
        "icon": "bi-kanban",
        "description": "Missions shipping code, events, or research this season.",
        "endpoint": "projects",
    },
    {
        "key": "research_outputs",
        "label": "Research Tracks",
        "icon": "bi-journal-code",
        "description": "Members contributing to papers, evaluations, and technical write-ups.",
        "endpoint": "team",
        "fragment": "tech-wing",
    },
    {
        "key": "events_hosted",
        "label": "Events Crew",
        "icon": "bi-calendar-event",
        "description": "Specialists ready to deploy large-scale experiences and logistics.",
        "endpoint": "team",
        "fragment": "team-event-management",
    },
]


def derive_home_stats(members: List[Dict[str, Any]], projects: List[Dict[str, Any]]) -> Dict[str, int]:
    events_capacity = 0
    research_contributors = 0
    for member in members:
        focus_tokens = set(member.get("focus_tokens", []))
        if member.get("subteam") in EVENT_SUBTEAMS or focus_tokens.intersection(EVENT_FOCUS_TOKENS):
            events_capacity += 1
        if member.get("subteam") in RESEARCH_SUBTEAMS or focus_tokens.intersection(RESEARCH_FOCUS_TOKENS):
            research_contributors += 1

    active_projects = len(projects)
    return {
        "active_members": len(members),
        "active_projects": active_projects,
        "research_outputs": max(research_contributors, max(1, active_projects // 2)),
        "events_hosted": max(events_capacity, max(1, active_projects)),
    }


def compose_home_stat_cards(values: Dict[str, int]) -> List[Dict[str, Any]]:
    cards: List[Dict[str, Any]] = []
    for spec in HOME_STATS_LAYOUT:
        raw_value = values.get(spec["key"], 0)
        href = spec.get("href")
        if not href:
            endpoint = spec.get("endpoint")
            if endpoint:
                href = url_for(endpoint)
                fragment = spec.get("fragment")
                if fragment:
                    href = f"{href}#{fragment}"
        card_payload = {
            key: value
            for key, value in spec.items()
            if key not in {"key", "endpoint", "fragment", "href"}
        }
        card_payload["value"] = max(raw_value, 1)
        card_payload["href"] = href
        cards.append(card_payload)
    return cards


@app.route("/")
def index() -> str:
    home = load_home_data()
    projects = load_projects_data()
    team_data = load_team_data()
    stats = derive_home_stats(team_data["members"], projects)
    return render_template(
        "index.html",
        home=home,
        projects=projects[:6],
        stats_cards=compose_home_stat_cards(stats),
        structured_people=team_data["structured_people"],
    )


@app.route("/projects")
def projects() -> str:
    projects = load_projects_data()
    tags = sorted({tag for project in projects for tag in project["tags"]})
    return render_template("projects.html", projects=projects, tags=tags)


@app.route("/team")
def team() -> str:
    team_data = load_team_data()
    return render_template(
        "team.html",
        members=team_data["members"],
        wings=team_data["wings"],
        filters=team_data["filters"],
        structured_people=team_data["structured_people"],
    )


@app.route("/ai")
def ai_page() -> str:
    ai_data = load_ai_data()
    return render_template("ai.html", ai=ai_data)


@app.route("/styleguide")
def styleguide() -> str:
    """Render the internal design system reference page."""
    return render_template("styleguide.html")


@app.route("/robots.txt")
def robots_txt() -> Response:
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {PUBLIC_BASE_URL}/sitemap.xml",
        ]
    )
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml() -> Response:
    lastmod = datetime.utcnow().date().isoformat()
    routes = [
        ("/", "1.0"),
        ("/projects", "0.9"),
        ("/team", "0.9"),
        ("/ai", "0.7"),
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


if __name__ == "__main__":
    app.run(debug=True)
