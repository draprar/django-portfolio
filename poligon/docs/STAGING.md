# Staging and the content pipeline

Ćwiczba stays in this Django project. Staging is a second database and a second set of environment variables, not a new application.

Before a content release:

1. `python manage.py validate_poligon_content`
2. `python manage.py diff_poligon_content` — published practice rows that would be added, removed, or whose English prompt changed
3. `python manage.py migrate`
4. `python manage.py seed_poligon`
5. `python manage.py smoke_poligon`

Production settings for that environment: `DEBUG=False`, the secret from the environment, HTTPS, secure cookies, a content security policy, and a database backup. Account export and deletion are on the account page (`/cwiczba/konto/`), which is required before any audio upload. Audio upload is not enabled; see `RETENTION.md`.

Product events stored for an account: `exercise_started`, `exercise_completed`, `exercise_abandoned`, `placement_started`, `placement_completed`, `account_created`, `flashcard_reviewed`, `language_changed`. A guest still writes nothing.
