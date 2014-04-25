from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

register = template.Library()


@register.inclusion_tag('admin/request_submit_line.html', takes_context=True)
def submit_affiliate_row(context):
    return submit_row(context)
