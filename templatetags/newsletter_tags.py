from django import template
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

register = template.Library()

@register.inclusion_tag('newsletter/registration.html', takes_context=True)
def newsletter_registration(context, next = None):
  return {}
