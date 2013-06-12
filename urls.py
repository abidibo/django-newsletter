from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('newsletter.views',

  url(r'^iscrizione/$', 'subscribe', name='newsletter_subscribe'),
  url(r'^cancellazione/(?P<code>[\d\w]+)/?$', 'unsubscribe', name='newsletter_unsubscribe'),

)
