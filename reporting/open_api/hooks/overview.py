import os

from django.conf import settings


def populate(result, generator, request, public):
    path = os.path.join(settings.BASE_DIR, "reporting/open_api/schema/overview.md")

    with open(path, "r") as overview:
        result["info"]["description"] = overview.read()

    return result
