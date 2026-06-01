# Walery Portfolio (Django)
![CI](https://github.com/draprar/django-portfolio/actions/workflows/ci.yaml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Code style](https://img.shields.io/badge/code%20style-ruff-261230)

🌐 Live: [walery.site](https://walery.site)

**Combined Django project** integrating 8 full-stack applications into a unified portfolio. Demonstrates modern Django patterns: split view architecture, async views, REST APIs, AI integration, and clean layering.

## What's inside?

| App | Purpose                                                         |
|-----|-----------------------------------------------------------------|
| **tonguetwister** | Language practice platform with chatbot + REST API + auth flows |
| **docdiff** | Document comparison engine with AI analysis + HTML/JSON reports |
| **gallery** | Image gallery with categories and full CRUD                     |
| **core** | Landing page, contact form, user profiles                       |
| **rugby** | Archive of rugby team                                           |
| **bies** | Static pages integration                                        |
| **analytics** | Stubs (tracking disabled)                                       |
| **config** | Global Django settings, URLs, ASGI/WSGI                         |

## Quick start (5 min)

```bash
# 1. Clone & venv
git clone https://github.com/draprar/django_portfolio-walery.git
cd django_portfolio-walery
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate

# 2. Install & setup
pip install --upgrade pip
pip install -r requirements-dev.txt  # includes pytest, mypy, ruff
cp .env.example .env
python manage.py migrate

# 3. Run
python manage.py runserver
# → http://127.0.0.1:8000/
```

## Dev workflows

**Tests:**
```bash
pytest -q
# or: pytest -q --cov=. --cov-report=term-missing
```

**Type checking:**
```bash
mypy config core tonguetwister gallery docdiff rugby bies analytics
```

**Linting:**
```bash
ruff check .
```

## Code highlights

- **Split view architecture** (`tonguetwister/views_*.py`) — CRUD, auth, API, main logic separated
- **Async views** — chatbot with timeout handling
- **DRF + SimpleJWT** — full REST API with token auth
- **AI heuristics** — document analysis with semantic scoring
- **Bootstrap 5 + i18n** — responsive frontend with Polish/English
- **94% test coverage** — pytest + coverage tracking

## Requirements structure

| File | Purpose |
|------|---------|
| `requirements.txt` | → Production runtime (→ requirements-prod.txt) |
| `requirements-dev.txt` | Development: prod + pytest, mypy, ruff, pip-audit |
| `requirements-prod.lock.txt` | Pinned snapshot for reproducible CI/CD |

**CI/CD pipeline** (GitHub Actions):
- Django checks + migrations drift detection
- Type checks (mypy), linting (ruff), security audit (pip-audit)
- Tests with 60% coverage threshold

## Environment setup

For local development, `.env.example` contains sensible defaults. Optional features:

**S3 storage setup:**
```
USE_S3=True
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_STORAGE_BUCKET_NAME=<bucket>
```

**DocDiff limits:**
```
DOCDIFF_MAX_FILE_MB=10
DOCDIFF_MAX_UNCOMPRESSED_MB=120
```

## Security features

- Rate limiting on contact endpoints + honeypot fields
- File validation (extension, MIME, signature) in DocDiff
- Chatbot feature-flagged and disabled by default
- JWT token auth with 24h expiry
- CSRF protection + CORS validated

## License

MIT

