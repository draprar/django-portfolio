# Walery Portfolio (Django)
![CI](https://github.com/draprar/django-portfolio/actions/workflows/ci.yaml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Code style](https://img.shields.io/badge/code%20style-ruff-261230)

🌐 Live: [walery.site](https://walery.site)

A full-stack Django portfolio by an engineer-turned-developer — 8 integrated apps covering language tooling, document diffing, image galleries and more. Built to demonstrate real production patterns, not just CRUD.

> Split view architecture · async views · DRF + SimpleJWT · AI heuristics · 94% test coverage

## What's inside?

| App               | Purpose | Stack highlights |
|-------------------|---------|-----------------|
| **tonguetwister** | Language practice platform | async views · DRF + SimpleJWT · chatbot · email auth |
| **docdiff**       | Document comparison engine | AI semantic scoring · MIME/signature validation · HTML reports |
| **gallery**       | Image gallery with categories | CRUD · DRF · Instagram feed integration |
| **core**          | Landing page, contact form | rate limiting · honeypot · Brevo email · i18n |
| **rugby**         | Rugby team archive | static content |
| **bies**          | Slavic Wheel of the Year | static content |
| **analytics**     | Stubs — tracking disabled | — |
| **config**        | Global settings, URLs, ASGI/WSGI | — |

## Code highlights

| Pattern | Where | Detail                                                   |
|---------|-------|----------------------------------------------------------|
| Split view architecture | `tonguetwister/views_*.py` | CRUD · auth · API · main logic in separate modules       |
| Async views | `tonguetwister/views_main.py` | chatbot with `asyncio.wait_for` timeout + Sentry capture |
| DRF + SimpleJWT | `tonguetwister/views_api.py` | read-only ViewSets, per-endpoint auth, 5 min cache       |
| AI heuristics | `docdiff/heuristics_ai.py` | semantic scoring on paragraph-level diffs                |
| File security | `docdiff/views.py` | extension + MIME + magic-byte signature validation       |
| Rate limiting | `core/`, `tonguetwister/` | `django-ratelimit` per-IP on all mutation endpoints      |
| Email auth flow | `tonguetwister/views_auth.py` | token-based activation + password reset via Brevo        |
| Test coverage | project-wide | 95% — pytest + coverage, CI threshold at 80%             |

## Quick start (5 min)

```bash
# 1. Clone & venv
git clone https://github.com/draprar/django-portfolio.git
cd django-portfolio
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
- Chatbot feature-flagged for controlled rollout (disabled by default)
- JWT token auth with 24h expiry
- CSRF protection + CORS validated

## License

MIT