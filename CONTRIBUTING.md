# Contributing to Walery Portfolio

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Virtual environment support

### Local Setup

**Option 1: Using Make (recommended)**

```bash
git clone https://github.com/draprar/django_portfolio-walery.git
cd django_portfolio-walery
make setup
python manage.py createsuperuser
make serve
```

**Option 2: Manual setup**

```bash
git clone https://github.com/draprar/django_portfolio-walery.git
cd django_portfolio-walery
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/` and `/admin/` with your superuser credentials.

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/) for clear, structured commit history.

### Format

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **test**: Adding or updating tests
- **chore**: Maintenance, dependencies, tooling
- **refactor**: Code restructuring (no functional change)
- **security**: Security-related fixes
- **perf**: Performance improvements

### Scope

The scope should specify which app or component is affected:
- `core` - Landing page & contact
- `tonguetwister` - Language practice app
- `docdiff` - Document comparison
- `gallery` - Image gallery
- `rugby` - Blog section
- `config` - Project configuration
- `analytics` - Analytics module
- `tests` - Test suite
- `ci` - CI/CD pipeline

### Examples

```
feat(tonguetwister): add chatbot feature flag with input limits
fix(auth): prevent password reset user enumeration
security(docdiff): validate file signatures and MIME types
docs(readme): update deployment instructions
test(gallery): add tests for category filtering
chore(deps): bump Django to 5.2.13
refactor(core): extract email logic to separate module
```

## Code Standards

Before submitting a pull request, ensure your code meets these standards:

### 1. Linting (Ruff)

```bash
make lint
# or
ruff check .
```

Must pass without errors.

### 2. Type Checking (MyPy)

```bash
make type
# or
mypy config core tonguetwister gallery docdiff rugby analytics \
  --ignore-missing-imports --disable-error-code=import-untyped
```

Must pass without errors.

### 3. Testing (Pytest)

```bash
make test
# or
pytest -q --cov=. --cov-report=term-missing --cov-fail-under=60
```

Must achieve ≥60% coverage.

### 4. Code Quality Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Line length: max 120 characters (configured in `ruff.toml`)
- Use type hints where possible
- Add docstrings to classes and public methods
- Avoid duplicating code - use utility functions
- Prefer explicit imports over wildcard imports

### 5. Django Best Practices

- Use Django ORM (no raw SQL)
- Use class-based views where appropriate
- Keep business logic in models/services, not views
- Use form validation for input sanitization
- Add database indexes for frequently queried fields
- Use select_related/prefetch_related to prevent N+1 queries

## Testing

### Running Tests

```bash
# All tests
make test

# Specific app
pytest tonguetwister/tests/ -v

# Specific test file
pytest tonguetwister/tests/test_api.py -v

# Specific test function
pytest tonguetwister/tests/test_api.py::test_token_obtain_success -v

# With coverage
pytest --cov=. --cov-report=html
# Open htmlcov/index.html
```

### Writing Tests

New features must include tests. Follow this pattern:

```python
# tonguetwister/tests/test_my_feature.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from tonguetwister.models import Twister


class MyFeatureTest(TestCase):
    """Tests for my new feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
    
    def test_feature_works_correctly(self):
        """Test that feature works as expected."""
        # Arrange
        twister = Twister.objects.create(text="Test twister")
        
        # Act
        response = self.client.get('/tonguetwister/')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test twister")
```

### Test Organization

Tests are organized by app in `app_name/tests/` directory:
- `test_models.py` - Model tests
- `test_views.py` - View tests
- `test_api.py` - API endpoint tests
- `test_forms.py` - Form validation tests
- `test_urls.py` - URL routing tests

## Pull Request Process

1. **Fork and branch**
   ```bash
   git checkout -b feat/my-feature
   ```

2. **Make your changes**
   - Implement feature/fix
   - Add tests
   - Update documentation

3. **Run quality checks**
   ```bash
   make lint && make type && make test
   ```

4. **Commit with meaningful messages**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feat/my-feature
   ```

6. **Open a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Explain motivation and design decisions
   - Include screenshots for UI changes

7. **Address feedback**
   - Respond to code review comments
   - Make requested changes
   - Re-run tests to confirm fixes

8. **Merge**
   - Maintainer will merge after approval
   - Usually uses squash merge for clean history

## Documentation

### Updating README

If adding a new feature or changing functionality, update `README.md`:
- Add feature description
- Update relevant sections
- Include setup/usage instructions

### Code Documentation

Add docstrings to new functions/classes:

```python
class MyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing my resources.
    
    Provides CRUD operations for resources.
    Only authenticated users can create/update/delete.
    """
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        """
        List all resources.
        
        Returns paginated results (10 per page).
        Optional filters:
        - category: Filter by category ID
        """
        return super().list(request, *args, **kwargs)
```

## Security Considerations

- **Never commit secrets**: Use `.env` file, not `.env.example`
- **Validate user input**: Use forms and serializers
- **Escape user content**: Use Django's template escaping
- **Rate limit endpoints**: Use `@ratelimit` decorator for public endpoints
- **Validate file uploads**: Check extensions, MIME types, file signatures
- **Use HTTPS**: All production environments must use HTTPS
- **Keep dependencies updated**: Regularly run `pip-audit`

## Performance Guidelines

- Use `select_related()` for foreign key fields
- Use `prefetch_related()` for reverse relations and M2M
- Add database indexes for frequently queried fields
- Cache expensive operations using Redis
- Profile code before optimizing (use Django Debug Toolbar)
- Avoid N+1 queries

## Questions or Issues?

- Check existing [GitHub Issues](https://github.com/draprar/django_portfolio/issues)
- Review [README.md](README.md) for project overview

---

**Thank you for contributing! 🙏**

Your efforts help make this project better for everyone.

