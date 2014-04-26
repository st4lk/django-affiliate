from django.conf import settings


def common(request):
    return {"default_currency": settings.DEFAULT_CURRENCY}
