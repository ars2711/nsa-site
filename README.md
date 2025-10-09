# NSA Command Center

Official web hub for the **NUST Society of Artificial Intelligence**. Built as a futuristic "AI terminal" that mirrors NSA’s launch series and anchors the society’s identity, work, and future trajectory.

## 🔭 Vision

- Present NSA as Pakistan’s premier student-led AI collective.
- Showcase the three pillars of the society: **Who We Are**, **What We Do**, **Where We're Going**.
- Provide a high-impact call to action for new members to join the revolution.

## 🧠 Tech Stack

- **Backend**: Flask (Python 3.10+)
- **Frontend**: HTML, Bootstrap 5, custom neon/glassmorphism CSS, particles.js
- **State & Interactions**: Vanilla JS (theme toggle, scroll animations, CTA integration)

## 🗂 Project Structure

```text
nsa-site/
│   └── favicon.svg         # Vector favicon (drop in more assets as needed)
└── templates/
    ├── layout.html         # Base template (nav, footer, scripts)
    ├── index.html          # Command-center landing page
    ├── projects.html       # Projects portfolio with filters
    └── team.html           # Team roster with filters

data/
    ├── projects.json           # Editable projects data (title, summary, tags, status, lead, link)
   └── team.json               # Editable team roster
```

## 🚀 Running Locally

## Intake Links

Recruitment now happens directly through Google Forms. The two primary entry points are surfaced in the navbar and hero section:

- Recruitment Intake: <https://forms.gle/d8rLMELNKLbSxPNc7>
- PhD Applicants Portal: <https://forms.gle/fsUwK4bLwuXGMHmM9>

No server-side proxy is required—the site links out to Google Forms immediately when a visitor clicks a CTA.

```powershell
# 1. Create & activate a virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Flask dev server
python app.py
```

- **Hero Command Console**: Holographic intro, gradient copy, mission CTA pair.
- **9 Intel Cards**: Animated grid covering identity, culture, and strategic direction.
- **Recruitment & PhD CTAs**: Navbar buttons linking to the [Recruitment Intake](https://forms.gle/d8rLMELNKLbSxPNc7) and [PhD Applicants](https://forms.gle/fsUwK4bLwuXGMHmM9) Google Forms.
- **Google Form Intake**: Default flow uses Google Forms. A native on-site form can also forward responses directly to Google Forms (details below).
- **Dark / Light Modes**: Persistent theme toggle with particle system recoloring.
- **Projects Portfolio**: JSON-driven projects page with focus filters (e.g., CV, NLP, GenAI). Update `data/projects.json` to change content.

## 🛠 Development Notes

- Particle effects auto-reinitialise on theme changes.
- Scroll-triggered animations leverage `IntersectionObserver` (no heavy frameworks).
- Membership intake defaults to Google Forms. Enable the proxy endpoint if you need Flask to forward submissions quietly.

### Projects data model

Projects are rendered from `data/projects.json` if present; otherwise, a small fallback list is used. Each item supports:

```json
{
  "title": "Project Nebula",
  "summary": "Short 1–2 line description.",
  "tags": ["CV", "Robotics", "Generative AI"],
  "status": "Recruiting contributors",
  "lead": "Jane Doe",
  "link": "https://example.com/brief"
}
```

- `tags` may be a list or a comma-separated string; they are normalized.
- The filters shown at the top of `/projects` are derived from the union of all tags.
- An empty or `#` link will render a disabled "Brief uploading soon" pill.

To add or edit projects:

1. Open `data/projects.json`.
2. Add, edit, or remove objects as needed.
3. Refresh `/projects` — no server restart is required unless you’re running with aggressive caching.

Tip: Keep tags short (e.g., "LLM", "Web", "Security").

## � Google Form Proxy (Optional)

If you want Flask to forward form data directly to Google (instead of redirecting visitors):

1. Open your Google Form, view the page source, and copy the `action` attribute from the `<form>` tag (the URL ending in `formResponse`).
2. Export the value before starting Flask:

   ```powershell
   setx GOOGLE_FORM_ACTION "https://docs.google.com/forms/u/2/d/e/1FAIpQLSe-g3B4G6VBhCmB6Z6A_2ZMWH7MRCuq8n206H3DXdcvXHM7Qw/formResponse"
   # Restart your shell so the new environment variable is picked up.
   ```

3. Ensure any custom form inputs use Google’s field keys (e.g., `entry.123456789`).
4. POST submissions to `/submit-google-form`. The app will forward them with the `requests` library and redirect back to the join section.

## �📦 Deploying

1. Create a production-ready configuration (e.g., `gunicorn`, `waitress`, or Render/Heroku).
2. Set `FLASK_ENV=production` (or disable debug) before deploying live.
3. Add HTTPS, caching headers, and monitoring according to your hosting provider.

> For static hosting or CDN offloading, consider pre-rendering pages via Flask or migrating to a hybrid stack (e.g., Next.js) while keeping this as the canonical design prototype.

## 🧭 Roadmap

- Dynamic project portfolio with category filters (Web, CV, NLP, DL, GenAI).
- Team roster (Directorates, Executives) with hover bios.
- Events timeline & registration (Google/Firebase forms or internal endpoints).
- Resource/blog module for research drops and AI news.
- Secure admin dashboard (Firebase Auth + CRUD) to manage content.

## 🤝 Contributing

Pull requests and issue reports are welcome. Stay aligned with NSA’s design system: futuristic, minimal, accessible.

---

**Learn. Build. Evolve.** — Join the revolution and help define Pakistan’s AI frontier.
