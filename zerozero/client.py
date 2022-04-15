from django.conf import settings
from zerozero_pilot.client import build_client

build_client(
    settings.ZEROZERO_API_ENDPOINT,
    settings.ZEROZERO_API_TOKEN,
    __name__,
)
