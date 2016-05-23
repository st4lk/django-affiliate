from __future__ import unicode_literals
from django.template import Library, TemplateSyntaxError
from django.template.base import kwarg_re
from django.template.defaulttags import URLNode
from affiliate.utils import add_affiliate_code

register = Library()


class AffiliateURLNode(URLNode):
    def render(self, context, *args, **kwargs):
        url = super(AffiliateURLNode, self).render(context, *args, **kwargs)
        aid_code = context.get('affiliate_code', None)
        if aid_code:
            url = add_affiliate_code(url, aid_code)
        return url


@register.tag
def url_aff(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    try:
        viewname = parser.compile_filter(bits[1])
    except TemplateSyntaxError as exc:
        exc.args = (exc.args[0] + ". "
                "The syntax of 'url' changed in Django 1.5, see the docs."),
        raise
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return AffiliateURLNode(viewname, args, kwargs, asvar)
