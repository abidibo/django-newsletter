# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from shared.models import Thematism
from django.contrib.sites.models import Site
from django.core.mail import send_mail, get_connection
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import get_current_site
from django.template.loader import get_template
from django.template import Context

class SubscriptionCtg(models.Model):
  name = models.CharField(_('nome'), max_length=128)
  description = models.TextField(_('descrizione'), null=True, blank=True)

  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name = _('categoria di sottoscrizioni')
    verbose_name_plural = _('categorie di sottoscrizioni')

class Subscription(models.Model):
  date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('data di sottoscrizione'))
  categories = models.ManyToManyField(SubscriptionCtg, verbose_name=_('categorie'), null=True, blank=True)
  firstname = models.CharField(_('nome'), max_length=128, null=True, blank=True)
  lastname = models.CharField(_('cognome'), max_length=128, null=True, blank=True)
  cap = models.CharField(_('cap'), max_length=5, null=True, blank=True)
  email = models.EmailField(_('email'), max_length=128, blank=False, null=False, unique=True)
  code = models.CharField(_('codice sottoscrizione'), max_length=128)
  notes = models.TextField(_('note'), null=True, blank=True)

  def __unicode__(self):
    return self.email

  def get_categories(self):
    return ', '.join([x.name for x in self.categories.all()])
  get_categories.short_description = _('Categorie')

  def send_confirmation_email(self):
    subject = _(u'Conferma sottoscrizione alla newsletter di Vallesusa Tesori')
    message = _('Ti ringraziamo per esserti iscritto alla newsletter di Vallesusa Tesori.\r\nPuoi disiscriverti in qualunque momento visitando la seguente pagina: \r\n %s ') % self.unsubscription_url()
    send_mail(subject, message, 'noreply@vallesusa-tesori.it', [self.email], fail_silently=False)

  def unsubscription_url(self):
    request = None
    full_url = ''.join(['http://', get_current_site(request).domain, '/newsletter/cancellazione/' + self.code])
    return full_url

  class Meta:
    verbose_name = _('sottoscrizione')
    verbose_name_plural = _('sottoscrizioni')

class Settings(models.Model):
  label = models.CharField(_('etichetta impostazione'), max_length=128)
  from_name = models.CharField(_('nome campo from'), max_length=128)
  from_email = models.EmailField(_('email campo from'), max_length=128)
  to_name = models.CharField(_('nome campo to'), max_length=128)
  to_email = models.EmailField(_('email campo to'), max_length=128)
  return_path = models.CharField(_('envelope sender email'), max_length=128, help_text=_('dove i computer devono rispondere in caso di messaggi di ritorno o errori'))
  test_email = models.EmailField(_('email di test'), help_text=_(u'ogni newsletter verrà inviata anche a questo indirizzo'), max_length=128)

  def __unicode__(self):
    return str(self.label)

  class Meta:
    verbose_name = _('impostazioni')
    verbose_name_plural = _('impostazioni')

class Newsletter(models.Model):
  creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('creazione'))
  last_edit_date = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name=_('ultima modifica'))
  subject = models.CharField(_('oggetto'), max_length=255)
  text = models.TextField(_('testo'))
  public = models.BooleanField(verbose_name=_('pubblica'))

  def __unicode__(self):
    return self.subject

  class Meta:
    verbose_name = _('articolo newsletter')
    verbose_name_plural = _('articoli newsletter')

class Job(models.Model):
  creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('creazione'))
  newsletter = models.ForeignKey(Newsletter)
  settings = models.ForeignKey(Settings)
  categories = models.ManyToManyField(SubscriptionCtg, verbose_name=_('categorie di sottoscrizioni'))
  uncategorized = models.BooleanField(verbose_name=_(u'invia a iscritti non categorizzati'))

  def __unicode__(self):
    return u'%s (%s)' % (str(self.newsletter), str(self.creation_date)) 

  def get_categories(self):
    return ', '.join([x.name for x in self.categories.all()])
  get_categories.short_description = _('Categorie di sottoscrizioni')

  def send(self):

    final_result = True

    connection = get_connection()
    connection.open()

    plaintext = get_template('newsletter/newsletter.txt')
    htmly     = get_template('newsletter/newsletter.html')

    job_dispatch = JobDispatch(job=self)
    job_dispatch.save()

    for sub in Subscription.objects.filter(categories__in=self.categories.all()):
      d = Context({ 'title': _('Vallesusa Tesori'), 'text': self.newsletter.text, 'unsubscribe': sub.unsubscription_url() })
      subject = self.newsletter.subject
      from_email = self.settings.from_email
      to = self.settings.to_email
      bcc = sub.email
      text_content = plaintext.render(d)
      html_content = htmly.render(d)
      msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
      msg.attach_alternative(html_content, "text/html")
      result = msg.send()
      if not result:
        final_result = False
      dispatch = Dispatch(job_dispatch=job_dispatch, subscription=sub, success=(True if result else False))
      dispatch.save()

    connection.close()
    return final_result

  def send_test(self):
    plaintext = get_template('newsletter/newsletter.txt')
    htmly     = get_template('newsletter/newsletter.html')
    d = Context({ 'title': _('Vallesusa Tesori'), 'text': self.newsletter.text })
    subject = self.newsletter.subject
    from_email = self.settings.from_email
    to = self.settings.to_email
    bcc = self.settings.test_email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

  class Meta:
    verbose_name = _('programmazione')
    verbose_name_plural = _('programmazioni')

class JobDispatch(models.Model):
  date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('data invio'))
  job = models.ForeignKey(Job, verbose_name=_('programmazione'))

  def __unicode__(self):
    return str(self.date) + ' - ' + str(self.job)

  class Meta:
    verbose_name = _('log invio programmazione')
    verbose_name_plural = _('log invio programmazioni')


class Dispatch(models.Model):
  job_dispatch = models.ForeignKey(JobDispatch, verbose_name=_('invio programmazione'))
  subscription = models.ForeignKey(Subscription, verbose_name=_('sottoscrizione'))
  success = models.BooleanField(_('successo'))

  def __unicode__(self):
    return str(self.subscription) + ' - ' + str(self.job_dispatch)

  class Meta:
    verbose_name = _('log invio sottoscrizione')
    verbose_name_plural = _('log invio sottoscrizioni')

