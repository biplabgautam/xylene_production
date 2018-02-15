from django import forms
from .models import TempSubsection, TempSAQ, TempNumerical, TempSubsectionImage

from pagedown.widgets import PagedownWidget

class TempSubsectionForm(forms.ModelForm):
	content = forms.CharField(widget = PagedownWidget)
	class Meta:
		model = TempSubsection
		fields = [
			'subsection_serial',
			'title',
			'subtopic',
			'content',
			'remarks',
		]

	def __init__(self, chapter, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subtopic'].queryset = \
		self.fields['subtopic'].queryset.filter(chapter=chapter)

class TempSAQForm(forms.ModelForm):
	question = forms.CharField(widget=PagedownWidget)
	answer = forms.CharField(widget=PagedownWidget)

	class Meta:
		model = TempSAQ
		fields = [
			'question_serial',
			'question',
			'answer',
			'important',
			'remarks',
			'subtopic',
			'display_image',
			'image_caption',
		]

	def __init__(self, chapter, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subtopic'].queryset = \
		self.fields['subtopic'].queryset.filter(chapter=chapter)

class TempNumericalForm(forms.ModelForm):
	question = forms.CharField(widget=PagedownWidget)
	answer = forms.CharField(widget=PagedownWidget)
	class Meta:
		model = TempNumerical
		fields = [
			'numerical_serial',
			'question',
			'answer',
			'important',
			'remarks',
			'subtopic',
			'display_image',
			'image_caption',
		]

	def __init__(self, chapter, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subtopic'].queryset = \
		self.fields['subtopic'].queryset.filter(chapter=chapter)

class TempSubsectionImageForm(forms.ModelForm):
	class Meta:
		model = TempSubsectionImage
		fields = [
			'image_serial',
			'image',
			'caption',
			'subsection',
	]
	def __init__(self, subtopic, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subsection'].queryset = \
		self.fields['subsection'].queryset.filter(subtopic=subtopic)