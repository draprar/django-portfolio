# Thin compatibility facade.
# Keep public symbols here so `from . import views` keeps working.

from .views_api import ProgressView  # noqa: F401
from .views_auth import (  # noqa: F401
    account,
    activate,
    login_view,
    logout_view,
    password_set_view,
    password_view,
    register_view,
)
from .views_main import (  # noqa: F401
    dashboard,
    exercise,
    grade_review,
    home,
    last_result,
    placement,
    policy,
    practice,
    result,
    reviews,
    settings_view,
    start,
    tables,
)
