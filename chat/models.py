from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Dialog(models.Model):
	participants = models.ManyToManyField(User)
	last_message = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
	dialog = models.ForeignKey('Dialog', related_name='messages')
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey('auth.User')

def update_last_message(sender, instance, created, **kwargs):
	if created:
		Dialog.objects.filter(pk=instance.dialog.pk).update(
			last_message = instance.date
		)

post_save.connect(update_last_message, sender=Message)
