"""Views."""

import logging
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

logger = logging.getLogger(__name__)

@login_required
@permission_required("killstory.basic_access")
def index(request):
    """Render index view."""
    logger.info("Index view accessed by user %s", request.user)
    context = {"text": "Hello, World!"}
    return render(request, "killstory/index.html", context)
