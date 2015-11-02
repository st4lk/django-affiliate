# -*- coding: utf-8 -*-
from django.conf import settings
from decimal import Decimal as D


AFFILIATE_MODEL = settings.AFFILIATE_AFFILIATE_MODEL  # mandatory, must be set
PARAM_NAME = getattr(settings, 'AFFILIATE_PARAM_NAME', 'aid')
REWARD_AMOUNT = getattr(settings, 'AFFILIATE_REWARD_AMOUNT', 10)
REWARD_PERCENTAGE = getattr(settings, 'AFFILIATE_REWARD_PERCENTAGE', True)
SAVE_IN_SESSION = getattr(settings, 'AFFILIATE_SAVE_IN_SESSION', True)
SESSION_AGE = getattr(settings, 'AFFILIATE_SESSION_AGE', 5 * 24 * 60 * 60)
DEFAULT_LINK = getattr(settings, 'AFFILIATE_DEFAULT_LINK', '/')
REMOVE_PARAM_AND_REDIRECT = getattr(settings, 'AFFILIATE_REMOVE_PARAM_AND_REDIRECT', False)
# deprecated
BANNER_FOLDER = getattr(settings, 'AFFILIATE_BANNER_PATH', 'affiliate')
START_AID = getattr(settings, 'AFFILIATE_START_AID', "1000")
DEFAULT_CURRENCY = getattr(settings, 'AFFILIATE_DEFAULT_CURRENCY', "USD")
MIN_REQUEST_AMOUNT = getattr(settings, 'AFFILIATE_MIN_BALANCE_FOR_REQUEST', D('1.0'))
