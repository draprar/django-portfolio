# Walery Portfolio (Django)

🌐 [walery.site](https://walery.site)

Personal Django-based portfolio that integrates multiple previously standalone apps into one project.

## Stack

- Backend: Django 5, Django REST Framework, SimpleJWT
- Frontend: Bootstrap 5
- Storage: local media by default, optional Supabase S3-compatible backend
- Caching: LocMem (default), optional Redis
- Deployment: Render + GitHub Actions

## Apps in this repository

- `config` - global project configuration (settings, URLs, WSGI/ASGI)
- `core` - landing page and main contact flow
- `tonguetwister` - language practice app + API + auth flows
- `docdiff` - document comparison and diff reports
- `gallery` - image gallery and categories
- `rugby` - blog-like section for rugby posts
- `bies` - lightweight static app integrated into portfolio
- `analytics` - compatibility stubs (tracking intentionally disabled)

### Tonguetwister view architecture

The app uses a split view layout to keep responsibilities isolated:

- `tonguetwister/views_main.py` - homepage, chatbot endpoint, load-more endpoints, user-content and add/remove actions
- `tonguetwister/views_crud.py` - admin CRUD views for content models
- `tonguetwister/views_auth.py` - auth, activation, password reset, contact form
- `tonguetwister/views_api.py` - DRF viewsets, token endpoint, API health endpoint
- `tonguetwister/views.py` - compatibility facade for existing imports and URLs

## Local setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/draprar/django_portfolio-walery.git
cd django_portfolio-walery
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 2. Install dependencies

**For production (only runtime dependencies):**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**For development (includes pytest, mypy, ruff, pip-audit, etc.):**
```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

**Requirements structure:**
- `requirements.txt` → `requirements-prod.txt` — entry file for production
- `requirements-prod.txt` — pinned production dependencies
- `requirements-prod.lock.txt` — reproducible deployment snapshot (for production CI/CD)
- `requirements-dev.txt` — development tools + all production deps (for local dev + CI quality gates)

### 3. Configure environment

```bash
cp .env.example .env
```

For development, defaults from `.env.example` are enough. Keep `USE_S3=False` unless you provide full S3/Supabase credentials.

### 4. Run migrations and start server

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Tests

```bash
pytest -q
```

If tests fail because dependencies are missing, install from `requirements.txt` in your project virtualenv.

## CI quality gates

GitHub Actions pipeline:
- **Install:** `pip install -r requirements-dev.txt` (includes all dev tools)
- **Checks:**
  - Django system checks
  - migration drift check (`makemigrations --check --dry-run`)
  - linting (`ruff`)
  - type checks (`mypy`)
  - tests with coverage threshold
  - dependency audit (`pip-audit`)

**Production Render deploy:**
- **Install:** `pip install -r requirements.txt` (only runtime deps, faster & smaller)
- build runs deploy checks and collectstatic
- migrations run in pre-deploy command

Minimal required environment variables for production deploy:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY=<long-random-secret>`
- `DJANGO_ALLOWED_HOSTS=walery.onrender.com,walery.site`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://walery.onrender.com,https://walery.site`
- `CORS_ALLOWED_ORIGINS=https://walery.onrender.com,https://walery.site`

Optional storage setup:

- Keep `USE_S3=False` to use local media storage.
- If `USE_S3=True`, you must provide full S3/Supabase credentials:
  `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `SUPABASE_PROJECT_REF`.

Optional DocDiff hardening overrides:
- `DOCDIFF_MAX_FILE_MB` (default `10`)
- `DOCDIFF_MAX_ARCHIVE_ENTRIES` (default `3000`)
- `DOCDIFF_MAX_UNCOMPRESSED_MB` (default `120`)
- `DOCDIFF_MAX_COMPRESSION_RATIO` (default `80.0`)

## Security notes

- Contact endpoints use rate limiting and honeypot fields.
- DocDiff upload flow validates extension, MIME type and file signature.
- Chatbot is feature-flagged and disabled by default.

## License

MIT

