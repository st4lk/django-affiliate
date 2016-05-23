django-affiliate release notes
==============================

v0.4.0 (2016-05-24)
-------------------
- django 1.9 support
- python 3.5 support

Issues: #12

v0.3.3 (2016-04-10)
-------------------
- Don't raise exception in case of bad aid code type

Issues: #10

v0.3.2 (2016-11-29)
-------------------
- if AFFILIATE_REMOVE_PARAM_AND_REDIRECT is True, perform redirect only in case of GET request method

v0.3.1 (2015-11-29)
-------------------
- add setting AFFILIATE_REMOVE_PARAM_AND_REDIRECT, that allows to remove affiliate param from url and redirect

v0.2.1 (2015-10-29)
-------------------
- add translations to pypi

v0.2.0 (2015-10-29)
-------------------
- only affiliate model defined by package
- request now have lazy `affiliate` property, returns Affiliate instance (if exists)
- django 1.7, 1.8 support
- python 3.4 support
- tests are added
- backwards incompatible

Issues: #1, #3, #4, #6, #8

v0.1.1 (2015-01-15)
-------------------
- uploaded to pypi
- small bug fixes


v0.1.0 (2014-04-29)
-------------------

- affiliate model
- statistics models
- means for withdraw request
