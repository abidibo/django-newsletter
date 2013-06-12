# coding=utf-8
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from newsletter.models import SubscriptionCtg, Subscription, Settings, Newsletter, Job, JobDispatch, Dispatch

admin.site.register(SubscriptionCtg)

class SubscriptionAdmin(admin.ModelAdmin):
  list_display = ('email', 'firstname', 'lastname','date', 'get_categories', 'notes',)
  list_filter = ('date','categories',)

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Settings)
admin.site.register(Newsletter)



class JobAdmin(admin.ModelAdmin):
  list_display = ('creation_date', 'newsletter', 'get_categories', 'uncategorized',)
  list_filter = ('creation_date','categories',)
  actions = ['send_job', 'send_job_test',]

  def send_job(self, request, queryset):
    tot = queryset.count()
    print tot
    if tot > 1:
      messages.error(request, _('selezionare una sola programmazione per l\'invio'))
    else:
      job = queryset[0]
      result = job.send()
      if result:
        self.message_user(request, _(u"la newsletter è stata correttamente inviata"))
      else:
        messages.error(request, _(u'Alcune o tutte le mail non sono state inviate correttamente, controllare nella sezione \'Invio sottoscrizioni\''))

  send_job.short_description = "Invia la newsletter"

  def send_job_test(self, request, queryset):
    tot = queryset.count()
    print tot
    if tot > 1:
      messages.error(request, _('selezionare una sola programmazione per l\'invio'))
    else:
      job = queryset[0]
      result = job.send_test()
      if result:
        self.message_user(request, _(u"la newsletter è stata correttamente inviata all'indirizzo email di test"))
      else:
        messages.error(request, _(u'si è verificato un errore nell\'invio della newsletter all\'indirizzo email di test'))
  send_job_test.short_description = _(u"Invia la newsletter all'indirizzo email di test")

admin.site.register(Job, JobAdmin)

class JobDispatchAdmin(admin.ModelAdmin):
  #actions = None
  list_display = ('date', 'job',)
  list_filter = ('date',)

  def __init__(self, *args, **kwargs):
    super(JobDispatchAdmin, self).__init__(*args, **kwargs)
    self.list_display_links = (None, )

  def has_add_permission(self, request):
    return False

admin.site.register(JobDispatch, JobDispatchAdmin)

class DispatchAdmin(admin.ModelAdmin):
  #actions = None
  list_display = ('job_dispatch', 'subscription', 'success',)
  list_filter = ('success','job_dispatch',)

  def __init__(self, *args, **kwargs):
    super(DispatchAdmin, self).__init__(*args, **kwargs)
    self.list_display_links = (None, )

  def has_add_permission(self, request):
    return False

admin.site.register(Dispatch, DispatchAdmin)

