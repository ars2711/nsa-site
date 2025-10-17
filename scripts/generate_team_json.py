"""Parse team_raw.csv and emit structured team.json for the NSA site."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INPUT_CSV = DATA_DIR / "team_raw.csv"
OUTPUT_JSON = DATA_DIR / "team.json"

POSITION_REMAP = {
    "treasure": "Treasurer",
    "treasure ": "Treasurer",
    "treasurer": "Treasurer",
    "dd": "Deputy Director",
    "dd(tentative)": "Deputy Director (Tentative)",
}

INVISIBLE_TRANSLATION = {ord(ch): None for ch in "\u200b\u200c\u200d\u200e\u200f\ufeff"}
NAME_TRIM_CHARS = " '\"\u201c\u201d\u2018\u2019"


def strip_invisible(value: str) -> str:
    return value.translate(INVISIBLE_TRANSLATION)


def clean_scalar(value: str) -> str:
    compact = strip_invisible(value or "")
    return compact.strip()


def clean_name(raw: str) -> str:
    cleaned = strip_invisible(raw or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(NAME_TRIM_CHARS)
    return cleaned


def clean_email(raw: str) -> str:
    cleaned = strip_invisible(raw or "")
    cleaned = cleaned.replace(" ", "")
    return cleaned.lower()


def clean_position(raw: str) -> str:
    value = clean_scalar(raw)
    if not value:
        return "Member"
    normalized = re.sub(r"\s+", " ", value)
    key = normalized.lower()
    if key in POSITION_REMAP:
        return POSITION_REMAP[key]
    # Handle partial matches like "Director" with trailing punctuation
    normalized = normalized.replace("Treasure", "Treasurer")
    return normalized


def add_unique(seq: List[str], item: str) -> None:
    if item and item not in seq:
        seq.append(item)


def main() -> None:
    if not INPUT_CSV.exists():
        raise SystemExit(f"Missing source CSV: {INPUT_CSV}")

    members: Dict[str, Dict[str, object]] = {}
    section = ""
    subteam = ""

    with INPUT_CSV.open(encoding="utf-8") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if len(row) < 5:
                row.extend([""] * (5 - len(row)))
            cells = [clean_scalar(value) for value in row]
            if not any(cells):
                continue

            header_candidate = cells[0].lower()

            # Section headers live entirely in column 0.
            if cells[0] and all(not value for value in cells[1:]):
                section = cells[0]
                subteam = ""
                continue

            # Skip column headings.
            if header_candidate == "name":
                continue

            # Sub-team headers show up in column 1 with no name.
            if not cells[0] and cells[1] and all(not value for value in cells[2:]):
                subteam = cells[1]
                continue

            name = clean_name(row[0])
            if not name:
                # Ignore placeholder rows without a name.
                continue

            dept = clean_scalar(row[1])
            email = clean_email(row[3])
            position = clean_position(row[4])

            key = name.lower()
            entry = members.get(key)
            if entry is None:
                entry = {
                    "name": name,
                    "dept": dept,
                    "email": email,
                    "roles": [],
                    "focus": [],
                }
                members[key] = entry
            else:
                if dept and not entry["dept"]:
                    entry["dept"] = dept
                if email and not entry["email"]:
                    entry["email"] = email

            focus: List[str] = entry["focus"]  # type: ignore[assignment]
            add_unique(focus, section)
            add_unique(focus, subteam)

            # Include the full position and its leading keyword for filtering.
            add_unique(focus, position)
            lead_word = position.split()[0]
            add_unique(focus, lead_word)

            roles: List[str] = entry["roles"]  # type: ignore[assignment]
            add_unique(roles, position)

    # Materialise ordered list sorted by section->role->name for readability.
    def sort_key(item: Dict[str, object]) -> tuple:
        focus_values = item.get("focus", [])
        section = focus_values[0] if focus_values else "ZZZ"
        role = item.get("role", "")
        return (section, role, item.get("name", ""))

    output: List[Dict[str, object]] = []
    for data in members.values():
        roles = data.pop("roles")  # type: ignore[assignment]
        role = " / ".join(roles) if roles else "Member"
        entry = {
            "name": data["name"],
            "role": role,
            "dept": data.get("dept", ""),
            "focus": [item for item in data["focus"] if item],
            "bio": "",
            "email": data.get("email", ""),
            "links": {},
        }
        output.append(entry)

    output.sort(key=sort_key)

    OUTPUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(output)} members to {OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":  # pragma: no cover
    main()
