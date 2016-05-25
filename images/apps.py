from django.apps import AppConfig

class ImagesConfig(AppConfig):
	name = 'images'
	verbose_name = 'Image bookmarked'

	def ready(self):
		import images.signals