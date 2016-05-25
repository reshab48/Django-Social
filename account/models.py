from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

CITY = (
	('SLG', 'Siliguri'),
	('JPG', 'Jalpaiguri')
	)

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	city = models.CharField(max_length=3,choices=CITY)
	landmark = models.CharField(max_length=80)
	location = models.CharField(blank=True, max_length=500)
	mobile_no = models.CharField(max_length=10)
	photo = models.ImageField(upload_to="users/%y/%m/%d")


class Contact(models.Model):
	user_from = models.ForeignKey(User, related_name='rel_from_set')
	user_to = models.ForeignKey(User, related_name='rel_to_set')
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)

	def __unicode__(self):
		return "{} follows {}".format(self.user_from, self.user_to)

User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))

