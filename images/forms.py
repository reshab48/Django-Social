from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'image_file', 'description')
		widgets = {
        'image_file': forms.FileInput(attrs={'id':'inputFile'})
		}

	def save(self, force_insert=False, force_update=False, commit=True):
		image_file = super(ImageCreateForm, self).save(commit=False)
		if commit:
			image_file.save()
		return image_file

class ImageEditForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'description')