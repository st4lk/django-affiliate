Affiliate system for django
===========================

Allows to track affiliate code. So it is possible to log this code at needed moment, for example when payments are made.


Requirements
-----------

- python (2.7)
- django (1.5, 1.6)


Quick start
-----------

1. Install this package to your python distribution

2. Add 'affiliate' to INSTALLED_APP in your settings.py:

        INSTALLED_APPS = [
            # ...
            'affiliate',
        ]

3. Add 'affiliate.context_processors.common' to TEMPLATE_CONTEXT_PROCESSORS in your settings.py:

        TEMPLATE_CONTEXT_PROCESSORS = (
            # ...
            'affiliate.context_processors.common',
        )

4. In your template load 'affiliate_urls' tags:

        {% load affiliate_urls %}

5. In your template use 'url_aff' instead of 'url' template tag:

        <a href="{% url_aff 'home' %}">Home</a>
