from urlshortener.models import URLModel
from django.contrib.auth.hashers import make_password


def generate_alias(to_hash):
    hashed_url = make_password(to_hash)[-20:-9]

    try:
        if URLModel.objects.get(alias=hashed_url):
            return generate_alias(hashed_url)
    except URLModel.DoesNotExist:
        return hashed_url
