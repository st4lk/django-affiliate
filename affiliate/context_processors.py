# -*- coding: utf-8 -*-
from affiliate.tools import get_affiliate_param_name


def common(request):
    aff_param_name = get_affiliate_param_name()
    affiliate_code = request.GET.get(aff_param_name, None)
    return {'affiliate_code': affiliate_code}
