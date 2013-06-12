# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from newsletter.models import Subscription

class SubscriptionForm(forms.ModelForm):
  required_css_class = 'required'
  class Meta:
    model = Subscription
    required_css_class = 'required'
    exclude = ['categories','code','notes',]
