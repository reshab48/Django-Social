from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class Image(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="images_created")
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True)
	image_file = models.FileField(upload_to='images/%y/%m/%d')
	description = models.TextField(blank=True)
	created = models.DateField(auto_now_add=True, db_index=True)
	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
	total_likes = models.PositiveIntegerField(db_index=True, default=0)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('images:detail', args=[self.id, self.slug])

	def get_absolute_url2(self):
		return reverse('images:edit', args=[self.id, self.slug])
