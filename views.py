from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse

from newsletter.models import Subscription
from newsletter.forms import SubscriptionForm

import hashlib

def subscribe(request):

  result = False

  if request.method == 'POST':
    form = SubscriptionForm(request.POST)
    if form.is_valid():
      subscription = form.save()
      subscription.code = hashlib.md5(subscription.email).hexdigest()
      subscription.save()
      subscription.send_confirmation_email()
      result = True
  else:
    form = SubscriptionForm()

  return render_to_response('newsletter/subscribe.html', {'form': form, 'result': result}, context_instance=RequestContext(request))

def unsubscribe(request, code):
  subscription = get_object_or_404(Subscription, code=code)
  result = subscription.delete()

  return render_to_response('newsletter/unsubscribe.html', {'result': result}, context_instance=RequestContext(request))

